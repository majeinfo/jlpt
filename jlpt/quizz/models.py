from django.db import models

class Word(models.Model):
    word_kana = models.CharField(max_length=30, default='')
    word_romaji = models.CharField(max_length=40, default='')
    word_kanji = models.CharField(max_length=30, default='', blank=True)


class Translation(models.Model):
    LANG = (
        ('fr', 'Français'),
    )
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    lang = models.CharField(max_length=6, choices=LANG, default='fr')
    trans = models.CharField(max_length=64)

