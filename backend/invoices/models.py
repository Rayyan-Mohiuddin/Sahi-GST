import uuid
from django.conf import settings
from django.db import models

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    fields = models.JSONField(default=dict)
    result = models.JSONField(default=dict)
    source = models.CharField(max_length=30, default='manual')
    status = models.CharField(max_length=30, default='needs_review')
    original_id = models.UUIDField(null=True, blank=True)
    source_image = models.BinaryField(null=True, blank=True)
    source_mime = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class ReviewPage(models.Model):
    review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='pages')
    position=models.PositiveSmallIntegerField()
    data=models.BinaryField()
    mime=models.CharField(max_length=20)
    class Meta:
        ordering=['position']
        constraints=[models.UniqueConstraint(fields=['review','position'],name='unique_review_page')]
