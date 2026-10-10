"""Invoice-content screening, not document authenticity verification."""
import re

def check_invoice_text(text):
    patterns = {
        'invoice_heading': r'\binvoice\b|\binv\.?\s*(?:no|number|#)',
        'reference_or_date': r'\b(?:invoice|inv\.?)\s*(?:no\.?|number|date|#)|\b(?:date|dated)\b',
        'billing_amounts': r'\b(?:total|amount|subtotal|taxable|cgst|sgst|igst|payable)\b',
        'party_details': r'\b(?:supplier|seller|buyer|recipient|gstin|bill\s+to)\b',
    }
    cues = [name for name, pattern in patterns.items() if re.search(pattern, text, re.I)]
    ok = len(cues) >= 3 and 'billing_amounts' in cues
    return {'status':'invoice_like' if ok else 'not_recognized', 'matched_cues':cues,
            'message':'Invoice-like text found; confirm the original and supported scope.' if ok else 'This image could not be recognized as an invoice. Choose a clearer invoice image, or use manual entry without saving this image.'}
