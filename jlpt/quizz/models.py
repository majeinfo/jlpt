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
    kanji = models.CharField(max_length=30, default='', blank=True)
    romaji = models.CharField(max_length=30, default='', blank=True)
    traduction = models.CharField(max_length=30, default='', blank=True)
    present_pos_poli = models.CharField(max_length=40, default='', blank=True)
    present_neg = models.CharField(max_length=40, default='', blank=True)
    present_neg_poli = models.CharField(max_length=40, default='', blank=True)
    passe_pos = models.CharField(max_length=40, default='', blank=True)
    passe_pos_poli = models.CharField(max_length=40, default='', blank=True)
    passe_neg = models.CharField(max_length=40, default='', blank=True)
    passe_neg_poli = models.CharField(max_length=40, default='', blank=True)
    forme_te_pos = models.CharField(max_length=40, default='', blank=True)
    forme_te_neg = models.CharField(max_length=40, default='', blank=True)
    volitive = models.CharField(max_length=40, default='', blank=True)
    volitive_poli = models.CharField(max_length=40, default='', blank=True)
    potentiel_pos = models.CharField(max_length=40, default='', blank=True)
    potentiel_pos_poli = models.CharField(max_length=40, default='', blank=True)
    potentiel_neg = models.CharField(max_length=40, default='', blank=True)
    potentiel_neg_poli = models.CharField(max_length=40, default='', blank=True)
    passif_pos = models.CharField(max_length=40, default='', blank=True)
    passif_pos_poli = models.CharField(max_length=40, default='', blank=True)
    passif_neg = models.CharField(max_length=40, default='', blank=True)
    passif_neg_poli = models.CharField(max_length=40, default='', blank=True)
    causatif_pos = models.CharField(max_length=40, default='', blank=True)
    causatif_pos_poli = models.CharField(max_length=40, default='', blank=True)
    causatif_neg = models.CharField(max_length=40, default='', blank=True)
    causatif_neg_poli = models.CharField(max_length=40, default='', blank=True)
    imperatif_pos = models.CharField(max_length=40, default='', blank=True)
    imperatif_pos_poli = models.CharField(max_length=40, default='', blank=True)
    imperatif_neg = models.CharField(max_length=40, default='', blank=True)
    imperatif_neg_poli = models.CharField(max_length=40, default='', blank=True)
    conditionnel_eba_pos = models.CharField(max_length=40, default='', blank=True)
    conditionnel_eba_neg = models.CharField(max_length=40, default='', blank=True)
    conditionnel_tara_pos = models.CharField(max_length=40, default='', blank=True)
    conditionnel_tara_neg = models.CharField(max_length=40, default='', blank=True)
    gerondif = models.CharField(max_length=40, default='', blank=True)
    desideratif_present = models.CharField(max_length=40, default='', blank=True)
    desideratif_present_neg = models.CharField(max_length=40, default='', blank=True)
    desideratif_passe = models.CharField(max_length=40, default='', blank=True)
    desideratif_passe_neg = models.CharField(max_length=40, default='', blank=True)




