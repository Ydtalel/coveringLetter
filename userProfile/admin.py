from django.contrib import admin
from .models import CoverLetter

class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'processed_text', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'text', 'processed_text')


admin.site.register(CoverLetter, CoverLetterAdmin)
