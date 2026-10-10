from django.test import TestCase, Client
from .rules import validate, correction_draft
from .parser import parse_text
import json
from pathlib import Path

class ParserLayoutTests(TestCase):
    def test_synthetic_layouts(self):
        fixtures = json.loads((Path(__file__).parent / 'fixtures' / 'parser_layouts.json').read_text())
        for fixture in fixtures:
            with self.subTest(layout=fixture['name']):
                parsed = parse_text(fixture['text'])
                for field, expected in fixture['expected'].items():
                    self.assertEqual(parsed[field], expected, field)

    def test_explicit_labels_do_not_bleed_into_each_other(self):
        parsed = parse_text('Supplier GSTIN: 27ABCDE1234F1Z5\nBuyer GSTIN: 27PQRST5678L1Z2\nInvoice Date: 2026-10-10')
        self.assertIsNone(parsed['supplier_name'])
        self.assertIsNone(parsed['buyer_name'])
        self.assertIsNone(parsed['invoice_number'])

    def test_next_label_is_not_a_missing_value(self):
        parsed = parse_text('Invoice No:\nInvoice Date: 2026-10-10\nCGST:\nSGST: 450')
        self.assertIsNone(parsed['invoice_number'])
        self.assertIsNone(parsed['cgst'])

    def test_longer_label_and_negative_accounting_value(self):
        parsed = parse_text('Total taxable value: 10000\nRound off: (-0.50)')
        self.assertEqual(parsed['taxable_value'], '10000')
        self.assertIsNone(parsed['total'])
        self.assertEqual(parsed['round_off'], '-0.50')

def sample():
    return {'supplier_name': 'Demo Supplies', 'supplier_gstin': '27ABCDE1234F1Z5', 'buyer_name': 'Demo Buyer', 'buyer_gstin': '27PQRST5678L1Z2', 'invoice_number': 'DEMO/001', 'invoice_date': '2026-10-09', 'description': 'Synthetic goods', 'taxable_value': '10000', 'cgst': '900', 'sgst': '900', 'igst': '0', 'tax_rate': '18', 'total': '12800', 'round_off': '0'}

class RuleTests(TestCase):
    def test_difference(self):
        r = validate(sample())
        f = next(x for x in r['findings'] if x['rule_id'] == 'M04')
        self.assertEqual(f['expected'], '11800.00')
        self.assertEqual(f['status'], 'issue')
        self.assertIn('not changed', correction_draft(r['fields'], r))

    def test_clean_and_decimal(self):
        data = sample() | {'taxable_value': '0.10', 'cgst': '0', 'sgst': '0', 'igst': '0', 'tax_rate': '0', 'total': '0.10'}
        self.assertEqual(validate(data)['counts']['issue'], 0)

    def test_unknown_not_zero(self):
        r = validate(sample() | {'igst': None})
        self.assertEqual(next(x['status'] for x in r['findings'] if x['rule_id'] == 'M04'), 'not_checked')

    def test_nonfinite_and_negative(self):
        for bad in ['NaN', 'Infinity', '-10']:
            r = validate(sample() | {'taxable_value': bad})
            self.assertEqual(next(x['status'] for x in r['findings'] if x['rule_id'] == 'M04'), 'not_checked')

    def test_invalid_shapes(self):
        with self.assertRaises(ValueError): validate({'total': {'nested': 1}})

    def test_parse_no_hallucination(self):
        p = parse_text('Supplier: Demo\nGrand total: 12,800.00\nCGST: 900\n')
        self.assertEqual(p['total'], '12800.00')
        self.assertIsNone(p['buyer_gstin'])

class ApiTests(TestCase):
    def test_session_isolation_and_draft(self):
        a, b = Client(), Client()
        a.get('/api/session/')
        response = a.post('/api/reviews/', data={'fields': sample(), 'source': 'manual', 'scope_confirmed': True}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        ident = response.json()['id']
        self.assertEqual(a.get('/api/reviews/').json()['reviews'][0]['id'], ident)
        self.assertEqual(b.get(f'/api/reviews/{ident}/').status_code, 404)
        self.assertEqual(b.delete(f'/api/reviews/{ident}/').status_code, 404)
        self.assertIn('corrected document', a.get(f'/api/reviews/{ident}/').json()['draft'])

    def test_scope_required(self):
        self.assertEqual(Client().post('/api/reviews/', data={'fields': sample()}, content_type='application/json').status_code, 400)

    def test_csrf_enforced(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post('/api/reviews/', data={}, content_type='application/json').status_code, 403)

    def test_bad_json(self):
        self.assertEqual(Client().post('/api/parse/', data='[]', content_type='application/json').status_code, 400)
