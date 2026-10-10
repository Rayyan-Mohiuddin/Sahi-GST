import base64
import io
import json
import urllib.request
import urllib.error
from datetime import timedelta
from PIL import Image, UnidentifiedImageError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Case,When,Value,BooleanField,Prefetch
from django.db import transaction
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from .models import Review,ReviewPage
from .rules import validate, correction_draft, clean_fields, FIELDS
from .parser import parse_invoice
from .document_check import check_invoice_text
from .report import build_report
from .images import decode_pages,verify_image,MAX_PAGES,MAX_TOTAL
from .gemini import extract_fields,explain_findings
from .languages import LANGUAGES,rule_explanations

def error(message, status=400): return JsonResponse({'error': message}, status=status)

def body(request):
    data = json.loads(request.body or '{}')
    if not isinstance(data, dict): raise ValueError('Expected a JSON object.')
    return data

def owned(request):
    if request.user.is_authenticated: return Review.objects.filter(owner=request.user)
    if not request.session.session_key: return Review.objects.none()
    return Review.objects.filter(owner__isnull=True, session_key=request.session.session_key, created_at__gte=timezone.now() - timedelta(hours=24))

def serialize(review):
    has_image=review.image_saved if hasattr(review,'image_saved') else bool(review.source_image)
    image_urls=([f'/api/reviews/{review.id}/image/'] if has_image else [])+[f'/api/reviews/{review.id}/pages/{page.id}/' for page in review.pages.all()]
    return {'image_urls':image_urls,'id': str(review.id), 'fields': review.fields, 'result': review.result, 'source': review.source, 'status': review.status, 'created_at': review.created_at.isoformat(), 'original_id': str(review.original_id) if review.original_id else None, 'draft': correction_draft(review.fields, review.result), 'image_url': f'/api/reviews/{review.id}/image/' if has_image else None, 'report_url': f'/api/reviews/{review.id}/report/'}

def metadata(query):
    return query.prefetch_related(Prefetch('pages',queryset=ReviewPage.objects.defer('data'))).defer('source_image').annotate(image_saved=Case(When(source_image__isnull=False,then=Value(True)),default=Value(False),output_field=BooleanField()))

@ensure_csrf_cookie
def session(request):
    Review.objects.filter(owner__isnull=True, created_at__lt=timezone.now()-timedelta(hours=24)).delete()
    if not request.session.session_key: request.session.create()
    return JsonResponse({'authenticated': request.user.is_authenticated, 'username': request.user.get_username() if request.user.is_authenticated else None, 'cloud_extraction': bool(settings.GEMINI_API_KEY and settings.GEMINI_FREE_TIER_CONFIRMED), 'database': 'postgresql' if 'postgresql' in settings.DATABASES['default']['ENGINE'] else 'local-sqlite-smoke-test'})

def health(request):
    from django.db import connection
    try:
        with connection.cursor() as cursor: cursor.execute('SELECT 1')
        return JsonResponse({'status': 'ok', 'app': 'Sahi GST'})
    except Exception:
        return error('Database unavailable.', 503)

@require_http_methods(['GET', 'POST'])
def reviews(request):
    if request.method == 'GET':
        return JsonResponse({'reviews': [serialize(x) for x in metadata(owned(request))[:100]]})
    try:
        data = body(request)
        if data.get('scope_confirmed') is not True:
            return error('Confirm this is a supported single-rate domestic B2B goods invoice before checking.')
        source = data.get('source', 'manual')
        if source not in ['manual', 'local_ocr', 'gemini', 'sample']:
            return error('Unknown extraction source.')
        if source == 'local_ocr':
            ocr_text = data.get('ocr_text', '')
            if not isinstance(ocr_text,str) or len(ocr_text)>30000 or check_invoice_text(ocr_text)['status'] != 'invoice_like':
                return error('Invoice-like text was not recognized. Retry with an invoice image or use manual entry.',422)
        if not request.session.session_key: request.session.create()
        if owned(request).filter(created_at__gte=timezone.now()-timedelta(minutes=1)).count() >= 10:
            return error('Please wait a minute before creating more reviews.', 429)
        result = validate(data.get('fields', {}))
        original_id = data.get('original_id')
        image_bytes, image_mime = None, ''
        if original_id:
            original = get_object_or_404(owned(request), id=original_id)
            original_id = original.id
        pages=[]
        if data.get('save_image') is True:
            pages=decode_pages(data)
            if not pages and original_id:
                pages=([(bytes(original.source_image),original.source_mime)] if original.source_image else [])+[(bytes(page.data),page.mime) for page in original.pages.all()]
        image_bytes,image_mime=pages[0] if pages else (None,'')
        with transaction.atomic():
            review = Review.objects.create(owner=request.user if request.user.is_authenticated else None, session_key='' if request.user.is_authenticated else request.session.session_key, fields=result['fields'], result=result, source=source, status=result['status'], original_id=original_id,source_image=image_bytes,source_mime=image_mime)
            ReviewPage.objects.bulk_create([ReviewPage(review=review,position=index,data=raw,mime=mime) for index,(raw,mime) in enumerate(pages[1:],2)])
        return JsonResponse(serialize(review), status=201)
    except (ValueError, TypeError, json.JSONDecodeError, ValidationError):
        return error('Invalid invoice fields. Check the format and try again.')

@require_http_methods(['GET', 'DELETE'])
def detail(request, ident):
    review = get_object_or_404(metadata(owned(request)), id=ident)
    if request.method == 'DELETE':
        review.delete()
        return JsonResponse({'deleted': True})
    return JsonResponse(serialize(review))

@require_http_methods(['GET'])
def review_image(request,ident):
    review=get_object_or_404(owned(request).only('source_image','source_mime'),id=ident)
    if not review.source_image: return error('No original image was saved for this review.',404)
    response=HttpResponse(bytes(review.source_image),content_type=review.source_mime)
    response['Cache-Control']='private, no-store'
    return response

@require_http_methods(['GET'])
def review_page(request,ident,page_id):
    review=get_object_or_404(owned(request),id=ident)
    page=get_object_or_404(review.pages,id=page_id)
    response=HttpResponse(bytes(page.data),content_type=page.mime)
    response['Cache-Control']='private, no-store'
    return response

@require_http_methods(['GET'])
def review_report(request,ident):
    review=get_object_or_404(owned(request),id=ident)
    response=HttpResponse(build_report([review]),content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="Sahi-GST-{review.id}.pdf"'
    response['Cache-Control']='private, no-store'
    return response

@require_http_methods(['GET'])
def all_reports(request):
    response=HttpResponse(build_report(list(owned(request).defer('source_image')[:100])),content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="Sahi-GST-reviews.pdf"'
    response['Cache-Control']='private, no-store'
    return response

@require_http_methods(['POST'])
def parse(request):
    try:
        data = body(request)
        text = data.get('text', '')
        if not isinstance(text, str) or len(text) > 30000: return error('Text must be under 30,000 characters.')
        return JsonResponse({**parse_invoice(text), 'document_check':check_invoice_text(text), 'source': 'local_ocr', 'message': 'Best-effort label matching. Confirm every field against the original.'})
    except (ValueError, TypeError): return error('Invalid request.')

@require_http_methods(['POST'])
def extract(request):
    if not settings.GEMINI_API_KEY or not settings.GEMINI_FREE_TIER_CONFIRMED:
        return error('Cloud extraction is not configured. Use free on-device OCR or manual entry.', 503)
    if not request.user.is_authenticated:
        return error('Sign in to use the optional shared cloud extraction quota.', 401)
    if request.POST.get('consent') != 'true': return error('Explicit consent is required before sending this image to Google.')
    last = request.session.get('last_extraction', 0)
    if timezone.now().timestamp() - last < 20: return error('Please wait 20 seconds between cloud scans.', 429)
    uploads=request.FILES.getlist('files') or request.FILES.getlist('file')
    if not uploads or len(uploads)>MAX_PAGES or sum(x.size for x in uploads)>MAX_TOTAL:
        return error('Choose up to 5 invoice pages under 3 MB combined.')
    try: images=[verify_image(upload.read()) for upload in uploads]
    except ValueError as exc: return error(str(exc))
    request.session['last_extraction']=timezone.now().timestamp()
    try:
        data=extract_fields(images)
        if data['document_check']['status']!='invoice_like': return error('AI could not recognize a single invoice. Check the images or use local OCR/manual entry.',422)
        return JsonResponse(data)
    except urllib.error.HTTPError as exc:
        return error('AI quota/provider unavailable. Local OCR remains available; no paid fallback is enabled.',429 if exc.code==429 else 502)
    except Exception:
        return error('AI extraction did not return verifiable fields. Try local OCR or manual entry.',502)

@require_http_methods(['POST'])
def explanations(request,ident):
    review=get_object_or_404(owned(request).defer('source_image'),id=ident)
    try:
        data=body(request);language=data.get('language','en')
        if language not in LANGUAGES: return error('Unsupported language.')
        if data.get('use_ai') is not True:
            return JsonResponse({'explanations':rule_explanations(review.result['findings'],language),'source':'rule','language':language})
        if not request.user.is_authenticated: return error('Sign in to request AI wording.',401)
        if not settings.GEMINI_API_KEY or not settings.GEMINI_FREE_TIER_CONFIRMED: return error('AI is not configured. Rule explanations remain available.',503)
        last=request.session.get('last_explanation',0)
        if timezone.now().timestamp()-last<20: return error('Please wait 20 seconds before another AI explanation.',429)
        request.session['last_explanation']=timezone.now().timestamp()
        return JsonResponse({'explanations':explain_findings(review.result['findings'],LANGUAGES[language]),'source':'gemini','language':language})
    except urllib.error.HTTPError as exc: return error('AI wording unavailable. Use the rule explanation.',429 if exc.code==429 else 502)
    except (ValueError,TypeError): return error('Explanation could not be verified. Use the rule explanation.',502)
    except Exception: return error('AI wording unavailable. Use the rule explanation.',502)


def frontend(request, path=''):
    root = settings.FRONTEND_DIR.resolve()
    candidate = (root / (path or 'index.html')).resolve()
    if not candidate.is_relative_to(root): return HttpResponse(status=404)
    if candidate.is_dir(): candidate = candidate / 'index.html'
    if not candidate.exists() and not path: candidate = root / 'index.html'
    if candidate.is_file():
        return FileResponse(candidate.open('rb'))
    return HttpResponse('Frontend not built. Run npm run build in frontend, or open the local Next.js dev server.', status=404)
