"""Safe server-side OCR telemetry. Invoice contents are never logged."""
import logging
logger = logging.getLogger(__name__)

def record_parse_metrics(*, quality, field_confidence, corrections, review_fields):
    values = [value for value in field_confidence.values() if isinstance(value, (int, float))]
    logger.info('ocr_pipeline_metrics quality_score=%s mean_field_confidence=%s corrections=%s validation_review_fields=%s manual_review_rate=%s', quality.get('score') if isinstance(quality, dict) else None, round(sum(values) / len(values), 1) if values else None, len(corrections), len(review_fields), round(len(review_fields) / max(len(field_confidence), 1), 3))
