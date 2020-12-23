from django.contrib import admin

from .models import Word, Translation, Verb

class ChoiceInline(admin.TabularInline):
    model = Translation
    extra = 1


class WordAdmin(admin.ModelAdmin):
    list_display = ('word_kana', 'word_kanji', 'word_romaji')
    search_fields = ('word_kana', 'word_romaji')
    inlines = [ChoiceInline]


class VerbAdmin(admin.ModelAdmin):
    list_display = ('kanji', 'romaji', 'present_pos_poli')
    search_fields = ('romaji', 'present_pos_poli')


admin.site.register(Word, WordAdmin)
admin.site.register(Verb, VerbAdmin)
