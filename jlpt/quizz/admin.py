from django.contrib import admin

from .models import Word, Translation

class ChoiceInline(admin.TabularInline):
    model = Translation
    extra = 1


class WordAdmin(admin.ModelAdmin):
    list_display = ('word_kana', 'word_kanji', 'word_romaji')
    search_fields = ('word_kana', 'word_romaji')
    inlines = [ChoiceInline]


admin.site.register(Word, WordAdmin)
