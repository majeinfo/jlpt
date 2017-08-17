from django.shortcuts import render
from django.http import HttpResponse
from .models import Word, Translation
from django.contrib import messages
from django.utils.translation import ugettext as _

from django.shortcuts import render, redirect

cur_lang = 'fr'

def index(request):
    context = { 'wc': _word_count() }
    return render(request, 'index.html', context)


def run_quizz(request):
    # Select "n" random words
    count = 20      # TODO: could be chosen by the user
                    # TODO: could choose the columns (hiragan/kanji)
    words = Word.objects.order_by('?')[:count]

    context = { 'words': words, 'wc': _word_count() }
    return render(request, 'index.html', context)


def check_quizz(request):
    results = []
    words_romaji = request.GET.getlist('romaji')
    words_kana = request.GET.getlist('kana')
    words_kanji = request.GET.getlist('kanji')
    words_id = request.GET.getlist('id')
    count = len(words_id)
    goods = 0

    for idx, wid in enumerate(words_id):
        item = {
            'status': False,
            'word_kana': words_kana[idx],
            'word_kanji': words_kanji[idx],
            'word_romaji': words_romaji[idx],
            'user_word': request.GET[words_romaji[idx]],
            'word_trans': '',
        }
        trans = Translation.objects.filter(lang=cur_lang, word=wid)
        norm_resp = _normalize(request.GET[words_romaji[idx]])
        for tr in trans:
            norm_tr = _normalize(tr.trans)
            if item['word_trans']: item['word_trans'] += " / "
            item['word_trans'] += tr.trans
            if norm_tr == norm_resp:
                item['status'] = True
                goods += 1
                break

        results.append(item)

    context = { 'wc': _word_count(), 'results': results, 'goods': goods, 'count': count }
    messages.info(request, _('Votre score est de %d/%d') % (goods, count))
    return render(request, 'check.html', context)


def _word_count():
    return Word.objects.all().count()


def _normalize(s):
    # Remove unwanted characters
    for c in ",;:!' -_+*\"\\/~[]{}()=<>":
        s = s.replace(c, "")

    # change accents
    accents = {
        'à': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'û': 'u', 'ü': 'u', 'ù': 'u',
        'ç': 'c'
    }

    for k, v in accents.items():
        s = s.replace(k, v)

    # lowerize everything and suppress the ending 's' for plural
    s = s.lower()
    if len(s) > 1 and s[-1] == 's':
        s = s[:-1]

    return s
