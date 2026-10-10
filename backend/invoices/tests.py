from django.test import TestCase, Client
from .rules import validate, correction_draft
from .parser import parse_text, parse_invoice
import json
from pathlib import Path
import base64
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from .document_check import check_invoice_text

class DocumentAndImageTests(TestCase):
    def test_selectable_pdf_is_parsed_before_ocr(self):
        from reportlab.pdfgen.canvas import Canvas
        raw = io.BytesIO(); pdf = Canvas(raw); pdf.drawString(72, 720, 'Tax Invoice'); pdf.drawString(72, 700, 'Invoice No: PDF/001'); pdf.drawString(72, 680, 'Grand total: 1000.00'); pdf.save()
        response = Client().post('/api/parse-document/', {'file': SimpleUploadedFile('invoice.pdf', raw.getvalue(), content_type='application/pdf')})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['used_embedded_text'])
        self.assertEqual(response.json()['fields']['invoice_number'], 'PDF/001')

    def test_rejects_noninvoice_text_but_not_missing_invoice_fields(self):
        self.assertEqual(check_invoice_text('A cat on a sofa')['status'],'not_recognized')
        self.assertEqual(check_invoice_text('Tax invoice\nSupplier: Demo\nTotal: 100')['status'],'invoice_like')
        self.assertEqual(check_invoice_text('Invoice holiday photo')['status'],'not_recognized')

    def test_local_ocr_review_requires_invoice_cues(self):
        response=Client().post('/api/reviews/',data={'fields':sample(),'source':'local_ocr','scope_confirmed':True,'ocr_text':'A landscape photo'},content_type='application/json')
        self.assertEqual(response.status_code,422)
        from .models import Review
        self.assertEqual(Review.objects.count(),0)

    def test_saved_image_pdf_ownership_and_deletion(self):
        image=io.BytesIO();Image.new('RGB',(20,20),'white').save(image,format='PNG')
        a,b=Client(),Client()
        response=a.post('/api/reviews/',data={'fields':sample(),'source':'sample','scope_confirmed':True,'save_image':True,'image_data':base64.b64encode(image.getvalue()).decode()},content_type='application/json')
        self.assertEqual(response.status_code,201);review=response.json()
        saved=a.get(review['image_url']);self.assertEqual(saved.content,image.getvalue());self.assertEqual(saved['Cache-Control'],'private, no-store')
        self.assertEqual(b.get(review['image_url']).status_code,404)
        pdf=a.get(review['report_url']);self.assertEqual(pdf.status_code,200);self.assertTrue(pdf.content.startswith(b'%PDF-'));self.assertEqual(pdf['Content-Type'],'application/pdf')
        self.assertEqual(b.get(review['report_url']).status_code,404)
        self.assertIsNotNone(a.get('/api/reviews/').json()['reviews'][0]['image_url'])
        a.delete('/api/reviews/'+review['id']+'/');self.assertEqual(a.get(review['image_url']).status_code,404)

    def test_invalid_image_and_opt_out(self):
        payload={'fields':sample(),'source':'manual','scope_confirmed':True,'save_image':True,'image_data':'not-base64'}
        self.assertEqual(Client().post('/api/reviews/',data=payload,content_type='application/json').status_code,400)
        payload['save_image']=False
        response=Client().post('/api/reviews/',data=payload,content_type='application/json')
        self.assertEqual(response.status_code,201);self.assertIsNone(response.json()['image_url'])

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

    def test_review_hints_preserve_uncertainty(self):
        result = parse_invoice('Date: 10/11/2026\nGrand total: 1000\nGrand total: 2000\nSupplier GSTIN: 27ABCDE1234F125')
        hints = {item['field']: item for item in result['review_fields']}
        self.assertEqual(hints['invoice_date']['reason'], 'uncertain_value')
        self.assertEqual(hints['total']['reason'], 'conflicting_values')
        self.assertEqual(hints['supplier_gstin']['reason'], 'identifier_structure')
        self.assertEqual(result['extracted_count'], 1)
        self.assertEqual(result['field_count'], 15)
        self.assertIsNone(result['fields']['invoice_date'])
        self.assertEqual(hints['total']['evidence'], 'Grand total: 1000')

    def test_safe_field_specific_corrections_and_low_quality_review(self):
        result = parse_invoice('Supplier GSTIN: 27ABCDE1234F1ZO\nInvoice No: INV@/002\nGrand total: Rs. 1O00.00', {'confidence': 95, 'quality': {'score': 35}})
        self.assertEqual(result['fields']['supplier_gstin'], '27ABCDE1234F1Z0')
        self.assertEqual(result['fields']['invoice_number'], 'INV/002')
        self.assertEqual(result['fields']['total'], '1000.00')
        self.assertEqual({x['field'] for x in result['corrections']}, {'supplier_gstin','invoice_number','total'})
        self.assertIn('low_image_quality', {x['reason'] for x in result['review_fields']})

    def test_ambiguous_gstin_is_not_guessed(self):
        result = parse_invoice('Supplier GSTIN: 27ABCDE1234F1Z5')
        self.assertEqual(result['fields']['supplier_gstin'], '27ABCDE1234F1Z5')
        self.assertEqual(result['corrections'], [])
        self.assertEqual(next(x['reason'] for x in result['review_fields'] if x['field']=='supplier_gstin'), 'identifier_structure')

def sample():
    return {'supplier_name': 'Demo Supplies', 'supplier_gstin': '27ABCDE1234F1Z0', 'buyer_name': 'Demo Buyer', 'buyer_gstin': '27PQRST5678L1Z0', 'invoice_number': 'DEMO/001', 'invoice_date': '2026-10-09', 'description': 'Synthetic goods', 'taxable_value': '10000', 'cgst': '900', 'sgst': '900', 'igst': '0', 'tax_rate': '18', 'total': '12800', 'round_off': '0'}

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

    def test_parse_api_returns_actionable_hints(self):
        response = Client().post('/api/parse/', data={'text':'CGST: 9%\nBuyer GSTIN: 27PQRST5678L1Z2'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIsNone(result['fields']['cgst'])
        self.assertEqual(next(x['reason'] for x in result['review_fields'] if x['field']=='cgst'), 'uncertain_value')
