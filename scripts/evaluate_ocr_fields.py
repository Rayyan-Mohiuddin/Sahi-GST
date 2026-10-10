"""Compare real synthetic-image OCR output to labelled field expectations."""
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'backend'))
from invoices.parser import parse_invoice, NUMERIC

fixtures = json.loads((root / 'tests/ocr_images/manifest.json').read_text())
records = json.loads((root / '.local/ocr-evaluation/ocr-output.json').read_text())
by_name = {record['name']: record for record in records}
def equal(field, actual, expected):
    if field in NUMERIC and actual is not None and expected is not None:
        try: return Decimal(actual) == Decimal(expected)
        except InvalidOperation: return False
    return actual == expected

report = {'dataset':'Three generated synthetic invoices; no real-world accuracy claim', 'images':[], 'present_fields_correct':0, 'present_fields_total':0, 'expected_unknown_correct':0, 'expected_unknown_total':0, 'mismatches_flagged_for_review':0}
for fixture in fixtures:
    record = by_name[fixture['name']]
    parsed = parse_invoice(record.get('text',''))
    mismatches = []
    for field, expected in fixture['expected'].items():
        correct = equal(field, parsed['fields'][field], expected)
        group = 'expected_unknown' if expected is None else 'present_fields'
        report[group+'_total'] += 1
        report[group+'_correct'] += correct
        if not correct:
            flagged = any(hint['field'] == field for hint in parsed['review_fields'])
            report['mismatches_flagged_for_review'] += flagged
            mismatches.append({'field':field,'expected':expected,'observed':parsed['fields'][field], 'flagged_for_review':flagged})
    report['images'].append({'name':fixture['name'],'elapsed_ms':record['elapsed_ms'],'error':record.get('error'),'mismatches':mismatches,'review_fields':parsed['review_fields']})
report_path = root / '.local/ocr-evaluation/field-report.json'
report_path.write_text(json.dumps(report,indent=2)+'\n')
print(f"Present fields: {report['present_fields_correct']}/{report['present_fields_total']}; expected unknown: {report['expected_unknown_correct']}/{report['expected_unknown_total']}")
for image in report['images']:
    print(image['name'], 'mismatched fields:', ', '.join(x['field'] for x in image['mismatches']) or 'none', 'error:', image['error'] or 'none')
print(f'Full report: {report_path}')
