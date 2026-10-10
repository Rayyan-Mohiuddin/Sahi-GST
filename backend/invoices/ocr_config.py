"""Central, deliberately conservative OCR thresholds."""
from django.conf import settings

DEFAULTS = {'field_confidence': 72, 'quality_score': 60, 'arithmetic_tolerance': '0.01', 'enable_corrections': True}

def ocr_config():
    configured = getattr(settings, 'OCR_PIPELINE', {})
    return {**DEFAULTS, **(configured if isinstance(configured, dict) else {})}
