"""Limited invoice consistency checks. Never a GST compliance certificate."""
import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from .gstin import GSTIN_PATTERN, valid as valid_gstin
from .ocr_config import ocr_config

RULE_VERSION = '2026-10-10.1'
GSTIN = GSTIN_PATTERN
TEXT_FIELDS = ['supplier_name', 'supplier_gstin', 'buyer_name', 'buyer_gstin', 'invoice_number', 'invoice_date', 'place_of_supply', 'description']
MONEY_FIELDS = ['taxable_value', 'cgst', 'sgst', 'igst', 'total', 'round_off']
FIELDS = TEXT_FIELDS + MONEY_FIELDS + ['tax_rate']
NOT_CHECKED = ['Active GST registration and invoice authenticity', 'HSN classification and legal GST rate', 'Place-of-supply applicability and tax jurisdiction', 'Supplier filing, GSTR-2B match and ITC eligibility', 'Complete Rule 46 requirements, IRN and e-invoice applicability']

def clean_fields(data):
    if not isinstance(data, dict):
        raise ValueError('Invoice fields must be an object.')
    result = {}
    for key in FIELDS:
        value = data.get(key)
        if value is not None and not isinstance(value, (str, int, float)):
            raise ValueError(f'{key} must be text or a number.')
        value = str(value).strip() if value is not None else ''
        if len(value) > 500:
            raise ValueError(f'{key} is too long.')
        result[key] = value or None
    for key in ['supplier_gstin', 'buyer_gstin']:
        if result[key]: result[key] = result[key].upper().replace(' ', '')
    return result

def number(value):
    if value is None or str(value).strip() == '': return None
    try:
        value = Decimal(str(value).replace(',', '').replace('₹', '').strip())
        if not value.is_finite() or abs(value) > Decimal('1000000000000'): return None
        return value
    except InvalidOperation:
        return None

def money(value):
    return str(value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))

def validate(data):
    f = clean_fields(data)
    findings = []
    def add(rule, field, status, title, message, observed=None, expected=None):
        findings.append({'id': f'{rule}-{field}', 'rule_id': rule, 'field': field, 'status': status, 'title': title, 'message': message, 'observed': observed, 'expected': expected})
    for key, label in [('supplier_name', 'Supplier name'), ('supplier_gstin', 'Supplier GSTIN'), ('buyer_name', 'Buyer name'), ('buyer_gstin', 'Buyer GSTIN'), ('invoice_number', 'Invoice number'), ('invoice_date', 'Invoice date'), ('description', 'Goods description')]:
        if not f[key]:
            add('F01', key, 'review', f'{label} needs confirmation', 'Not extracted or entered. Check the original; if actually missing, request it from the supplier.')
        else:
            add('F01', key, 'pass', f'{label} provided', 'Present in the confirmed fields; not independently verified.', f[key])
    for key in ['supplier_gstin', 'buyer_gstin']:
        if f[key]:
            ok = valid_gstin(f[key])
            add('I01', key, 'pass' if ok else 'issue', 'GSTIN structure and checksum checked' if ok else 'GSTIN structure/checksum differs', 'Format and checksum only; this does not check active registration or identity.' if ok else 'Confirm the original GSTIN. Expected a valid 15-character GSTIN and checksum.', f[key])
    if f['invoice_number']:
        ok = bool(re.fullmatch(r'[A-Za-z0-9/-]{1,16}', f['invoice_number']))
        add('I02', 'invoice_number', 'pass' if ok else 'review', 'Invoice number format', 'Expected up to 16 letters, digits, hyphens or slashes in the supported tax-invoice case; confirm document type if different.', f['invoice_number'])
    if f['invoice_date']:
        try:
            d = date.fromisoformat(f['invoice_date'])
            ok = d <= date.today() + timedelta(days=1)
            add('I03', 'invoice_date', 'pass' if ok else 'review', 'Invoice date', 'Date parses.' if ok else 'Future date: confirm the document date, not automatically an invalid invoice.', f['invoice_date'])
        except ValueError:
            add('I03', 'invoice_date', 'review', 'Confirm invoice date', 'Use YYYY-MM-DD after checking the original.', f['invoice_date'])
    values = {key: number(f[key]) for key in MONEY_FIELDS + ['tax_rate']}
    for key, value in values.items():
        if value is None:
            add('M00', key, 'review', key.replace('_', ' ').capitalize() + ' needs confirmation', 'Enter the amount shown on the invoice. Enter zero only when you confirm it is zero.')
        elif value < 0 and key != 'round_off':
            add('M00', key, 'review', 'Negative value outside current scope', 'Credit notes and negative adjustments need a different review flow.', f[key])
    components = ['taxable_value', 'cgst', 'sgst', 'igst', 'round_off', 'total']
    if all(values[k] is not None for k in components) and all(values[k] >= 0 for k in components if k != 'round_off'):
        expected = sum(values[k] for k in components if k != 'total')
        difference = values['total'] - expected
        ok = abs(difference) <= Decimal(str(ocr_config()['arithmetic_tolerance']))
        add('M04', 'total', 'pass' if ok else 'issue', 'Invoice total agrees' if ok else f'Total differs by ₹{abs(difference):,.2f}', 'Taxable value + CGST + SGST + IGST + stated round-off. Confirm all extracted amounts before requesting a correction.', money(values['total']), money(expected))
    else:
        add('M04', 'total', 'not_checked', 'Total check waiting', 'All component amounts must be confirmed numeric values first.')
    if all(values[k] is not None and values[k] >= 0 for k in ['taxable_value', 'tax_rate', 'cgst', 'sgst', 'igst']) and values['tax_rate'] <= 100:
        expected = values['taxable_value'] * values['tax_rate'] / 100
        observed = values['cgst'] + values['sgst'] + values['igst']
        ok = money(expected) == money(observed)
        add('M02', 'tax_rate', 'pass' if ok else 'review', 'Printed rate arithmetic agrees' if ok else 'Tax amount needs review', 'Single-rate, tax-exclusive invoice assumption. Multiple-rate invoices need line-level review; this does not verify the legal rate.', money(observed), money(expected))
    else:
        add('M02', 'tax_rate', 'not_checked', 'Rate arithmetic waiting', 'Confirm a single rate between 0 and 100 and nonnegative tax amounts.')
    if all(values[k] is not None for k in ['cgst', 'sgst', 'igst']):
        if values['igst'] > 0 and (values['cgst'] > 0 or values['sgst'] > 0):
            add('M03', 'igst', 'review', 'Mixed tax components', 'IGST and CGST/SGST are both shown. Confirm the invoice scope; jurisdiction is not decided from buyer state.')
    count = {s: sum(x['status'] == s for x in findings) for s in ['issue', 'review', 'pass', 'not_checked']}
    tax_values=[values[k] for k in ['cgst','sgst','igst']]
    tax_amount=money(sum(tax_values)) if all(x is not None and x>=0 for x in tax_values) else None
    return {'fields': f, 'rule_version': RULE_VERSION, 'findings': findings, 'counts': count, 'not_checked': NOT_CHECKED, 'status': 'needs_review' if count['issue'] or count['review'] else 'checked', 'tax_context':{'amount':tax_amount,'label':'GST amount under review' if count['issue'] or count['review'] else 'GST amount on invoice','eligibility_checked':False}}

def correction_draft(fields, result):
    problems = [x for x in result['findings'] if x['status'] in ['issue', 'review']]
    if not problems:
        return 'No correction request generated: no issue was identified in the supported checks. Unchecked areas still require review.'
    lines = [f"Hello {fields.get('supplier_name') or 'supplier'},", '', f"Please help us review invoice {fields.get('invoice_number') or '(number to confirm)'}. After checking our transcription, we noticed:"]
    for item in problems:
        detail = item['title']
        if item.get('expected') is not None:
            detail += f" (observed {item.get('observed')}; arithmetic expected {item['expected']})"
        lines.append('- ' + detail)
    lines += ['', 'Please clarify these details and provide a corrected document where appropriate. We have not changed your original invoice.', '', 'Thank you.']
    return '\n'.join(lines)
