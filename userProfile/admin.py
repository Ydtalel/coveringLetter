from django.contrib import admin
from .models import CoverLetter, ProcessedCoverLetter


class ProcessedCoverLetterInline(admin.TabularInline):
    model = ProcessedCoverLetter
    extra = 0  # Указываем 0, чтобы не показывать лишние пустые поля для добавления новых вариантов


class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')
    list_filter = ('user',)
    search_fields = ('user__username', 'text')
    inlines = [ProcessedCoverLetterInline]  # Добавляем встроенный класс для отображения обработанных вариантов


class ProcessedCoverLetterAdmin(admin.ModelAdmin):
    list_display = ('cover_letter', 'processed_text', 'created_at')
    list_filter = ('cover_letter__user', 'created_at')
    search_fields = ('cover_letter__user__username', 'processed_text')


admin.site.register(CoverLetter, CoverLetterAdmin)
admin.site.register(ProcessedCoverLetter, ProcessedCoverLetterAdmin)
