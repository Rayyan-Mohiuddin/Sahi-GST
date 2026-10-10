import base64,io
from unittest.mock import patch
from django.test import TestCase,Client,override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from .tests import sample
from .gemini import extract_fields,explain_findings
from .rules import validate,FIELDS
from .images import decode_pages,verify_image

def image_bytes():
    buffer=io.BytesIO();Image.new('RGB',(20,20),'white').save(buffer,format='PNG');return buffer.getvalue()

class MultiPageTests(TestCase):
    def test_all_saved_pages_private_and_deleted(self):
        a,b=Client(),Client();encoded=base64.b64encode(image_bytes()).decode()
        response=a.post('/api/reviews/',data={'fields':sample(),'source':'sample','scope_confirmed':True,'save_image':True,'image_pages':[encoded,encoded]},content_type='application/json')
        self.assertEqual(response.status_code,201);data=response.json();self.assertEqual(len(data['image_urls']),2)
        self.assertEqual(a.get(data['image_urls'][1]).content,image_bytes());self.assertEqual(b.get(data['image_urls'][1]).status_code,404)
        a.delete('/api/reviews/'+data['id']+'/');self.assertEqual(a.get(data['image_urls'][1]).status_code,404)

    def test_page_limit_and_legacy_single_image(self):
        encoded=base64.b64encode(image_bytes()).decode()
        with self.assertRaises(ValueError):decode_pages({'image_pages':[encoded]*6})
        self.assertEqual(len(decode_pages({'image_data':encoded})),1)

    def test_deployment_image_limit(self):
        with self.assertRaisesRegex(ValueError,'3 MB'):verify_image(b'x'*(3*1024*1024+1))

    def test_tax_context_is_not_a_credit_loss_claim(self):
        result=validate(sample());self.assertEqual(result['tax_context']['amount'],'1800.00');self.assertFalse(result['tax_context']['eligibility_checked'])
        self.assertIsNone(validate(sample()|{'igst':None})['tax_context']['amount'])

class AIAdapterTests(TestCase):
    @patch('invoices.gemini.request_json')
    def test_extraction_preserves_uncertainty(self,request):
        request.return_value={'document_type':'invoice','fields':sample()|{'buyer_gstin':None},'uncertain_fields':['supplier_gstin']}
        data=extract_fields([(image_bytes(),'image/png')]*2)
        self.assertIsNone(data['fields']['buyer_gstin']);self.assertIn('supplier_gstin',[x['field'] for x in data['review_fields']])
        self.assertEqual(len(request.call_args.args[1]),2)

    @patch('invoices.gemini.request_json')
    def test_ai_cannot_add_verdicts_ids_or_amounts(self,request):
        findings=validate(sample())['findings'];ids=[x['id'] for x in findings if x['status'] in ['issue','review']]
        request.return_value={'explanations':[{'id':ident,'text':'Check the total against the original and ask the supplier to clarify.'} for ident in ids]}
        self.assertEqual(len(explain_findings(findings,'English')),len(ids))
        request.return_value={'explanations':[{'id':ids[0],'text':'You will save 1000.'}]}
        with self.assertRaises(ValueError):explain_findings(findings,'English')
        request.return_value={'explanations':[{'id':'invented','text':'The invoice is fine.'}]}
        with self.assertRaises(ValueError):explain_findings(findings,'English')

    @override_settings(GEMINI_API_KEY='test-only',GEMINI_FREE_TIER_CONFIRMED=True)
    @patch('invoices.views.extract_fields')
    def test_cloud_accepts_multiple_pages_but_requires_login_consent(self,extract):
        a=Client();files=lambda:[SimpleUploadedFile('one.png',image_bytes(),content_type='image/png'),SimpleUploadedFile('two.png',image_bytes(),content_type='image/png')]
        self.assertEqual(a.post('/api/extract/',{'files':files(),'consent':'true'}).status_code,401)
        user=get_user_model().objects.create_user(username='ai-test',password='test-password');a.force_login(user)
        self.assertEqual(a.post('/api/extract/',{'files':files()}).status_code,400)
        extract.return_value={'fields':sample(),'document_check':{'status':'invoice_like'}}
        self.assertEqual(a.post('/api/extract/',{'files':files(),'consent':'true'}).status_code,200);self.assertEqual(len(extract.call_args.args[0]),2)

    def test_languages_ownership_and_no_fake_ai(self):
        a,b=Client(),Client();review=a.post('/api/reviews/',data={'fields':sample(),'source':'sample','scope_confirmed':True},content_type='application/json').json()
        url=f"/api/reviews/{review['id']}/explanations/"
        for lang in ['en','hi','te']:
            response=a.post(url,data={'language':lang},content_type='application/json');self.assertEqual(response.status_code,200);self.assertEqual(response.json()['source'],'rule')
        self.assertEqual(b.post(url,data={'language':'en'},content_type='application/json').status_code,404)
        self.assertEqual(a.post(url,data={'use_ai':True},content_type='application/json').status_code,401)
