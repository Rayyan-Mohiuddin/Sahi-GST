"""Conservative OCR parsing with field-specific, auditable corrections."""
import re
from datetime import datetime
from decimal import Decimal
from .rules import FIELDS
from .gstin import valid as valid_gstin
from .ocr_config import ocr_config
from .ocr_metrics import record_parse_metrics

LABELS = {
    'supplier_name': r'(?:supplier|seller)(?!\s+gstin\b)(?:\s+name)?', 'buyer_name': r'(?:buyer|recipient|customer)(?!\s+gstin\b)(?:\s+name)?',
    'supplier_gstin': r'(?:supplier|seller)\s+gstin', 'buyer_gstin': r'(?:buyer|recipient|customer)\s+gstin',
    'invoice_number': r'(?:invoice|inv\.?)\s*(?:number|no\.?|#)', 'invoice_date': r'(?:invoice\s+date|dated|date)',
    'description': r'(?:goods\s+description|description|goods)', 'place_of_supply': r'place\s+of\s+supply',
    'taxable_value': r'(?:total\s+taxable\s*(?:value|amount)|taxable\s*(?:value|amount)|sub[ -]?total)',
    'cgst': r'cgst(?:\s+amount)?', 'sgst': r'sgst(?:\s+amount)?', 'igst': r'igst(?:\s+amount)?',
    'tax_rate': r'(?:printed\s+)?(?:gst|tax)\s+rate(?:\s*\(%\))?', 'round_off': r'(?:stated\s+)?round[ -]?(?:off|ing)',
    'total': r'(?:grand\s+total|invoice\s+total|total\s+amount|amount\s+payable|net\s+payable|total)',
}
NUMERIC = {'taxable_value', 'cgst', 'sgst', 'igst', 'tax_rate', 'total', 'round_off'}
START = re.compile(r'^\s*(?:' + '|'.join(LABELS.values()) + r')(?=\s|[:=]|$)', re.I)
NUMBER = re.compile(r'(?<![\w.,])[-+]?(?:\d{1,3}(?:,\d{2,3})+|\d+)(?:\.\d+)?(?![\w.,])')
CONFUSIONS = str.maketrans({'O':'0', 'I':'1', 'L':'1', 'S':'5', 'Z':'2'})

def _confidence_for(line, metadata):
    for item in (metadata or {}).get('lines', []):
        if item.get('text', '').strip() == line.strip() and isinstance(item.get('confidence'), (int, float)):
            return round(float(item['confidence']), 1), item.get('bbox')
    value = (metadata or {}).get('confidence')
    return (round(float(value), 1) if isinstance(value, (int, float)) else None), None

def numeric_value(text, rate=False):
    text = re.sub(r'\b(?:INR|Rs\.?)(?=\s|\d|$)', ' ', text.replace('−', '-').replace('₹', ' '), flags=re.I).strip()
    corrected = text.upper().translate(CONFUSIONS)
    choices = []
    for source in [text, corrected] if corrected != text else [text]:
        # A partial regex match such as the trailing "00.00" in "1O00.00"
        # is not a safe amount. Let the field-specific normalized candidate
        # decide instead of silently dropping the leading digits.
        if source == text and re.search(r'\d[OILSZ]\d', source.upper()): continue
        values = []
        for match in NUMBER.finditer(source):
            if not rate and re.match(r'\s*%', source[match.end():]): continue
            value = match.group().replace(',', '')
            if re.fullmatch(r'\s*\(\s*' + re.escape(match.group()) + r'\s*\)\s*', source): value = '-' + value.lstrip('+-')
            values.append(value)
        if values: choices.append(values)
    if not choices or len({Decimal(x) for x in choices[0]}) != 1: return None, None
    return choices[0][0], 'numeric_character_normalization' if corrected != text else None

def date_value(value):
    for fmt in ['%Y-%m-%d', '%d-%b-%Y', '%d %b %Y', '%d %B %Y', '%d-%B-%Y']:
        try: return datetime.strptime(value.strip(), fmt).date().isoformat()
        except ValueError: pass
    match = re.fullmatch(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', value.strip())
    if match:
        day, month, year = map(int, match.groups())
        if day > 12 and 1 <= month <= 12:
            try: return datetime(year, month, day).date().isoformat()
            except ValueError: pass
    return None

def gstin_value(value):
    original = re.sub(r'\s+', '', value.upper())
    if valid_gstin(original): return original, None
    # GSTIN positions make ambiguity bounded: do not replace every Z/O/I in
    # the identifier, only characters in positions where a digit/letter is
    # mandated. The fixed penultimate Z is deliberately protected.
    digit_positions = {0, 1, 7, 8, 9, 10, 12}
    letter_positions = {2, 3, 4, 5, 6, 11}
    digit_map = {'O':'0', 'I':'1', 'L':'1', 'S':'5', 'Z':'2'}
    letter_map = {'0':'O', '1':'I', '2':'Z', '5':'S'}
    chars = []
    for index, char in enumerate(original):
        if index in digit_positions: chars.append(digit_map.get(char, char))
        elif index in letter_positions: chars.append(letter_map.get(char, char))
        elif index == 13: chars.append('Z' if char == '2' else char)
        elif index == 14: chars.append(digit_map.get(char, char))
        else: chars.append(char)
    candidate = ''.join(chars)
    if candidate != original and valid_gstin(candidate): return candidate, 'gstin_format_checksum_normalization'
    return original or None, None

def invoice_number_value(value):
    original = value.strip(); candidate = re.sub(r'[^A-Za-z0-9/\-]', '', original)
    if candidate and candidate != original and re.fullmatch(r'[A-Za-z0-9/-]{1,16}', candidate): return candidate, 'invoice_number_symbol_removal'
    return original or None, None

def parse_invoice(text, ocr_metadata=None):
    if not isinstance(text, str): raise ValueError('OCR text must be text.')
    cfg = ocr_config(); result = {key: None for key in FIELDS}; candidates = {key: [] for key in FIELDS}; uncertain = set(); evidence = {}; confidence = {}; regions = {}; corrections = []
    lines = [line.strip() for line in text.replace('\r', '').split('\n') if line.strip()]; section = None
    for index, line in enumerate(lines):
        if re.fullmatch(r'(?:bill(?:ed)?\s+to|buyer|recipient|customer|supplier|seller|sold\s+by)\s*:?', line, re.I):
            section = 'buyer' if re.match(r'bill|buyer|recipient|customer', line, re.I) else 'supplier'; continue
        matches = [(key, re.match(r'^' + label + r'(?=\s|[:=]|$)\s*[:=]?\s*(.*)$', line, re.I)) for key, label in LABELS.items()]
        for key, match in sorted([(key, match) for key, match in matches if match], key=lambda item:item[1].start(1), reverse=True)[:1]:
            value = match.group(1).strip()
            if not value and index + 1 < len(lines) and not START.match(lines[index + 1]) and not re.match(r'^GSTIN\b', lines[index + 1], re.I): value = lines[index + 1]
            value = re.split(r'\s+(?=(?:invoice\s*(?:no\.?|number|date)|date)\s*[:=])', value, maxsplit=1, flags=re.I)[0]
            raw_value = value; method = None; evidence.setdefault(key, line[:250]); conf, bbox = _confidence_for(line, ocr_metadata); confidence.setdefault(key, conf); regions.setdefault(key, bbox)
            if key in NUMERIC: value, method = numeric_value(value, rate=key == 'tax_rate')
            elif key == 'invoice_date': value = date_value(value)
            elif key.endswith('gstin'): value, method = gstin_value(value)
            elif key == 'invoice_number': value, method = invoice_number_value(value)
            if method and not cfg['enable_corrections']: value, method = raw_value, None
            if value: candidates[key].append(value)
            elif raw_value: uncertain.add(key)
            if method and raw_value != value: corrections.append({'field':key, 'rule':method, 'original':raw_value, 'normalized':value})
        match = re.fullmatch(r'GSTIN\s*[:=]?\s*(\S+)', line, re.I)
        if match and section:
            value, method = gstin_value(match.group(1));
            if method and not cfg['enable_corrections']: value, method = match.group(1), None
            candidates[section + '_gstin'].append(value); evidence.setdefault(section + '_gstin', line[:250]); conf, bbox = _confidence_for(line, ocr_metadata); confidence.setdefault(section + '_gstin', conf); regions.setdefault(section + '_gstin', bbox)
            if method: corrections.append({'field':section + '_gstin','rule':method,'original':match.group(1),'normalized':value})
        match = re.search(r'\s+(?:invoice\s+date|date)\s*[:=]\s*(.+)$', line, re.I)
        if match:
            value = date_value(match.group(1)); candidates['invoice_date'].append(value) if value else uncertain.add('invoice_date')
    quality = (ocr_metadata or {}).get('quality') if isinstance((ocr_metadata or {}).get('quality'), dict) else {}
    review_fields = []
    for key, values in candidates.items():
        values = [value for value in values if value]; unique = {Decimal(x) for x in values} if key in NUMERIC else set(values)
        if len(unique) == 1 and key not in uncertain: result[key] = values[0]
        if len(unique) > 1: reason, message = 'conflicting_values', 'More than one value was read. Confirm the correct value from the original.'
        elif key in uncertain: reason, message = 'uncertain_value', 'Text was found but could not be read unambiguously. Confirm it from the original.'
        elif result[key] is None: reason, message = 'not_extracted', 'Not extracted. Enter the printed value; leave unknown values blank.'
        elif key.endswith('gstin') and not valid_gstin(result[key]): reason, message = 'identifier_structure', 'GSTIN format/checksum did not validate. Check the original character by character.'
        elif confidence.get(key) is not None and confidence[key] < cfg['field_confidence']: reason, message = 'low_confidence', 'OCR confidence is low for this field. Confirm it from the original.'
        elif quality.get('score') is not None and quality['score'] < cfg['quality_score']: reason, message = 'low_image_quality', 'Image quality is too low to trust OCR alone. Retake in even light with the full page visible.'
        else: continue
        review_fields.append({'field':key, 'reason':reason, 'message':message, 'evidence':evidence.get(key), 'confidence':confidence.get(key), 'region':regions.get(key)})
    payload = {'fields':result, 'review_fields':review_fields, 'extracted_count':sum(value is not None for value in result.values()), 'field_count':len(FIELDS), 'field_confidence':confidence, 'corrections':corrections, 'raw_ocr_text':text, 'image_quality':quality}
    record_parse_metrics(quality=quality, field_confidence=confidence, corrections=corrections, review_fields=review_fields)
    return payload

def parse_text(text): return parse_invoice(text)['fields']
