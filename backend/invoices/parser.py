"""Conservative OCR-text parsing. Printed evidence only; ambiguity stays null."""
import re
from datetime import datetime
from decimal import Decimal
from .rules import FIELDS

LABELS = {
    'supplier_name': r'(?:supplier|seller)(?!\s+gstin\b)(?:\s+name)?',
    'buyer_name': r'(?:buyer|recipient|customer)(?!\s+gstin\b)(?:\s+name)?',
    'supplier_gstin': r'(?:supplier|seller)\s+gstin',
    'buyer_gstin': r'(?:buyer|recipient|customer)\s+gstin',
    'invoice_number': r'(?:invoice|inv\.?)\s*(?:number|no\.?|#)',
    'invoice_date': r'(?:invoice\s+date|dated|date)',
    'description': r'(?:goods\s+description|description|goods)',
    'place_of_supply': r'place\s+of\s+supply',
    'taxable_value': r'(?:total\s+taxable\s*(?:value|amount)|taxable\s*(?:value|amount)|sub[ -]?total)',
    'cgst': r'cgst(?:\s+amount)?', 'sgst': r'sgst(?:\s+amount)?', 'igst': r'igst(?:\s+amount)?',
    'tax_rate': r'(?:printed\s+)?(?:gst|tax)\s+rate(?:\s*\(%\))?',
    'round_off': r'(?:stated\s+)?round[ -]?(?:off|ing)',
    'total': r'(?:grand\s+total|invoice\s+total|total\s+amount|amount\s+payable|net\s+payable|total)',
}
NUMERIC = {'taxable_value', 'cgst', 'sgst', 'igst', 'tax_rate', 'total', 'round_off'}
START = re.compile(r'^\s*(?:' + '|'.join(LABELS.values()) + r')(?=\s|[:=]|$)', re.I)
NUMBER = re.compile(r'(?<![\w.,])[-+]?(?:\d{1,3}(?:,\d{2,3})+|\d+)(?:\.\d+)?(?![\w.,])')

def numeric_value(text, rate=False):
    text = text.replace('−', '-').replace('₹', ' ').strip()
    text = re.sub(r'\b(?:INR|Rs\.?)(?=\s|\d|$)', ' ', text, flags=re.I)
    candidates = []
    for match in NUMBER.finditer(text):
        if not rate and re.match(r'\s*%', text[match.end():]):
            continue
        value = match.group().replace(',', '')
        if re.fullmatch(r'\s*\(\s*' + re.escape(match.group()) + r'\s*\)\s*', text):
            value = '-' + value.lstrip('+-')
        candidates.append(value)
    distinct = {Decimal(x) for x in candidates}
    return candidates[0] if len(distinct) == 1 else None

def date_value(value):
    for fmt in ['%Y-%m-%d', '%d-%b-%Y', '%d %b %Y', '%d %B %Y', '%d-%B-%Y']:
        try:
            return datetime.strptime(value.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    match = re.fullmatch(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', value.strip())
    if match:
        day, month, year = map(int, match.groups())
        if day > 12 and 1 <= month <= 12:
            try: return datetime(year, month, day).date().isoformat()
            except ValueError: pass
    return None

def parse_text(text):
    result = {key: None for key in FIELDS}
    candidates = {key: [] for key in FIELDS}
    lines = [line.strip() for line in text.replace('\r', '').split('\n') if line.strip()]
    section = None
    for index, line in enumerate(lines):
        if re.fullmatch(r'(?:bill(?:ed)?\s+to|buyer|recipient|customer|supplier|seller|sold\s+by)\s*:?', line, re.I):
            section = 'buyer' if re.match(r'bill|buyer|recipient|customer', line, re.I) else 'supplier'
            continue
        matches = [(key, re.match(r'^' + label + r'(?=\s|[:=]|$)\s*[:=]?\s*(.*)$', line, re.I)) for key, label in LABELS.items()]
        matches = [(key, match) for key, match in matches if match]
        # Prefer the complete label: "Total taxable value" is not "Total".
        for key, match in sorted(matches, key=lambda item: item[1].start(1), reverse=True)[:1]:
            value = match.group(1).strip()
            if not value and index + 1 < len(lines) and not START.match(lines[index + 1]) and not re.match(r'^GSTIN\b', lines[index + 1], re.I):
                value = lines[index + 1]
            value = re.split(r'\s+(?=(?:invoice\s*(?:no\.?|number|date)|date)\s*[:=])', value, maxsplit=1, flags=re.I)[0]
            if key in NUMERIC: value = numeric_value(value, rate=key == 'tax_rate')
            elif key == 'invoice_date': value = date_value(value)
            elif key.endswith('gstin'): value = value.upper().replace(' ', '') if value else None
            if value: candidates[key].append(value)
        match = re.fullmatch(r'GSTIN\s*[:=]?\s*(\S+)', line, re.I)
        if match and section: candidates[section + '_gstin'].append(match.group(1).upper())
        match = re.search(r'\s+(?:invoice\s+date|date)\s*[:=]\s*(.+)$', line, re.I)
        if match:
            value = date_value(match.group(1))
            if value: candidates['invoice_date'].append(value)
    for key, values in candidates.items():
        unique = {Decimal(x) for x in values} if key in NUMERIC else set(values)
        if len(unique) == 1: result[key] = values[0]
    return result
