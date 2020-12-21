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

class Verb(models.Model):
    kana = models.CharField(max_length=30, default='')
    kanji = models.CharField(max_length=30, default='', blank=True)
    neutre_present = models.CharField(max_length=40, default='')
    neutre_passe = models.CharField(max_length=40, default='')
    neutre_present_neg = models.CharField(max_length=40, default='')
    neutre_passe_neg = models.CharField(max_length=40, default='')
    poli_present = models.CharField(max_length=40, default='')
    poli_passe = models.CharField(max_length=40, default='')
    poli_present_neg = models.CharField(max_length=40, default='')
    poli_passe_neg = models.CharField(max_length=40, default='')
    forme_te = models.CharField(max_length=40, default='')
    forme_passive = models.CharField(max_length=40, default='')
    cond_tara = models.CharField(max_length=40, default='')
    cond_eba = models.CharField(max_length=40, default='')
    factitif = models.CharField(max_length=40, default='')
    potentiel = models.CharField(max_length=40, default='')
    volitive = models.CharField(max_length=40, default='')
    suspensive = models.CharField(max_length=40, default='')
    poli_conjectural = models.CharField(max_length=40, default='')
    gerondif = models.CharField(max_length=40, default='')
    imperatif = models.CharField(max_length=40, default='')
    imperatif_neg = models.CharField(max_length=40, default='')
    imperatif_sup = models.CharField(max_length=40, default='')
    imperatif_neg_sup = models.CharField(max_length=40, default='')
    imperatif_poli = models.CharField(max_length=40, default='')
    imperatif_poli_neg = models.CharField(max_length=40, default='')



