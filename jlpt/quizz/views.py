import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import Word, Translation, Verb
from django.contrib import messages
from django.utils.translation import ugettext as _

from django.shortcuts import render, redirect

verb_forms = [
    {'title': 'neutre passé', 'field': 'neutre_passe'},
    {'title': 'neutre présent négatif', 'field': 'neutre_present_neg'},
    {'title': 'neutre passé négatif', 'field': 'neutre_passe_neg'},
    {'title': 'forme polie au présent', 'field': 'poli_present'},
    {'title': 'forme polie au passé', 'field': 'poli_passe'},
    {'title': 'forme polie au présent négatif', 'field': 'poli_present_neg'},
    {'title': 'forme polie au passé négatif', 'field': 'poli_passe_neg'},
    {'title': 'forme en -te', 'field': 'forme_te'},
    {'title': 'forme passive', 'field': 'forme_passive'},
    {'title': 'forme conditionnelle en -tara', 'field': 'cond_tara'},
    {'title': 'forme conditionnelle en -eba', 'field': 'cond_eba'},
    {'title': 'forme factitive (faire faire)', 'field': 'factitif'},
    {'title': 'forme potentielle (pouvoir faire)', 'field': 'potentiel'},
    {'title': 'forme volitive (vouloir faire)', 'field': 'volitive'},
    {'title': 'forme suspensive polie (-tari)', 'field': 'suspensive'},
    {'title': 'forme conjecturale polie (faisons...)', 'field': 'poli_conjectural'},
    {'title': 'gérondif (en faisant...)', 'field': 'gerondif'},
    {'title': 'impératif neutre', 'field': 'imperatif'},
    {'title': 'impératif neutre négatif', 'field': 'imperatif_neg'},
    {'title': 'impératif autoritaire', 'field': 'imperatif_sup'},
    {'title': 'impératif autoritaire négatif', 'field': 'imperatif_neg_sup'},
    {'title': 'impératif poli', 'field': 'imperatif_poli'},
    {'title': 'impératif poli négatif', 'field': 'imperatif_poli_neg'},
]

cur_lang = 'fr'

def index(request):
    context = { 'wc': _word_count(), 'verbs_wc': _verb_count() }
    return render(request, 'index.html', context)


def run_quizz(request):
    # Select "n" random words
    count = 20      # TODO: could be chosen by the user
                    # TODO: could choose the columns (hiragan/kanji)
    words = Word.objects.order_by('?')[:count]

    context = { 'words': words, 'wc': _word_count(), 'verbs_wc': _verb_count() }
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

    context = { 'wc': _word_count(), 'verbs_wc': _verb_count(), 'results': results, 'goods': goods, 'count': count }
    messages.info(request, _('Votre score est de %d/%d') % (goods, count))
    return render(request, 'check.html', context)


def run_verbs(request):
    # Select "n" random verbs
    count = 20      # TODO: could be chosen by the user
    verbs = Verb.objects.order_by('?')[:count]

    verbs2 = []
    for verb in verbs:
        f = random.randrange(len(verb_forms))
        verbs2.append(
            {
                'forme': verb_forms[f]['title'],
                'field': verb_forms[f]['field'],
                'kana': verb.kana,
                'kanji': verb.kanji,
                'neutre_present': verb.neutre_present,
                'id': verb.id
            }
        )

    context = { 'verbs': verbs2, 'wc': _word_count(), 'verbs_wc': _verb_count() }
    return render(request, 'index.html', context)


def check_verbs(request):
    results = []
    verbs_id = request.GET.getlist('id')
    verbs_kana = request.GET.getlist('kana')
    verbs_kanji = request.GET.getlist('kanji')
    verbs_neutre_present = request.GET.getlist('neutre_present')
    verbs_formes = request.GET.getlist('forme')
    verbs_fields = request.GET.getlist('field')
    count = len(verbs_id)
    goods = 0

    for idx, wid in enumerate(verbs_id):
        item = {
            'status': False,
            'kana': verbs_kana[idx],
            'kanji': verbs_kanji[idx],
            'neutre_present': verbs_neutre_present[idx],
            'forme' : verbs_formes[idx],
            'answer': _normalize(request.GET[verbs_neutre_present[idx] + "+" + verbs_fields[idx]])
        }
        qs = Verb.objects.get(pk=verbs_id[idx])
        item['good_answer'] = getattr(qs, verbs_fields[idx])
        if item['good_answer'] == item['answer']:
            item['status'] = True
            goods += 1

        results.append(item)

    context = { 'wc': _word_count(), 'verbs_wc': _verb_count(), 'results': results, 'goods': goods, 'count': count }
    messages.info(request, _('Votre score est de %d/%d') % (goods, count))
    return render(request, 'check_verbs.html', context)


def _word_count():
    return Word.objects.all().count()


def _verb_count():
    return Verb.objects.all().count()


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
