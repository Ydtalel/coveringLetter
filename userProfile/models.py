from django.db import models
from django.conf import settings


class CoverLetter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cover Letter for {self.user.username}"


class ProcessedCoverLetter(models.Model):
    cover_letter = models.ForeignKey(CoverLetter, related_name='processed_letters', on_delete=models.CASCADE)
    processed_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Processed Cover Letter for {self.cover_letter.user.username}"
