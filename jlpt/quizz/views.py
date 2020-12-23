import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import Word, Translation, Verb
from django.contrib import messages
from django.utils.translation import ugettext as _

from django.shortcuts import render, redirect

verb_forms = [
    {'title': 'forme neutre passé', 'field': 'passe_pos'},
    {'title': 'forme neutre présent négatif', 'field': 'present_neg'},
    {'title': 'forme neutre passé négatif', 'field': 'passe_neg'},
    {'title': 'forme polie au présent', 'field': 'present_pos_poli'},
    {'title': 'forme polie au passé', 'field': 'passe_pos_poli'},
    {'title': 'forme polie au présent négatif', 'field': 'present_neg_poli'},
    {'title': 'forme polie au passé négatif', 'field': 'passe_neg_poli'},
    {'title': 'forme en -te', 'field': 'forme_te_pos'},
    {'title': 'forme en -te négative', 'field': 'forme_te_neg'},
    {'title': 'forme conditionnelle en -tara', 'field': 'conditionnel_tara_pos'},
    {'title': 'forme conditionnelle négative en -tara', 'field': 'conditionnel_tara_neg'},
    {'title': 'forme conditionnelle en -eba', 'field': 'conditionnel_eba_pos'},
    {'title': 'forme conditionnelle négative en -eba', 'field': 'conditionnel_eba_neg'},
    {'title': 'gérondif (en faisant...)', 'field': 'gerondif'},
    {'title': 'impératif neutre', 'field': 'imperatif_pos'},
    {'title': 'impératif neutre négatif', 'field': 'imperatif_neg'},
    {'title': 'impératif poli', 'field': 'imperatif_pos_poli'},
    {'title': 'impératif poli négatif', 'field': 'imperatif_neg_poli'},
    {'title': 'forme potentielle neutre (pouvoir faire)', 'field': 'potentiel_pos'},
    {'title': 'forme potentielle négative neutre (ne pas pouvoir faire)', 'field': 'potentiel_neg'},
    {'title': 'forme potentielle polie (pouvoir faire)', 'field': 'potentiel_pos_poli'},
    {'title': 'forme potentielle négative polie (ne pas pouvoir faire)', 'field': 'potentiel_neg_poli'},
    {'title': 'forme passive neutre', 'field': 'passif_pos'},
    {'title': 'forme passive négative neutre', 'field': 'passif_neg'},
    {'title': 'forme passive polie', 'field': 'passif_pos_poli'},
    {'title': 'forme passive négative polie', 'field': 'passif_neg_poli'},
    {'title': 'forme volitive (vouloir faire)', 'field': 'volitive'},
    {'title': 'forme volitive polie (vouloir faire)', 'field': 'volitive_poli'},
    {'title': 'forme factitive (faire faire)', 'field': 'causatif_pos'},
    {'title': 'forme factitive négative (faire faire)', 'field': 'causatif_neg'},
    {'title': 'forme factitive polie (faire faire)', 'field': 'causatif_pos_poli'},
    {'title': 'forme factitive négative polie (faire faire)', 'field': 'causatif_neg_poli'},
    {'title': 'forme désidérative présent (je veux...)', 'field': 'desideratif_present'},
    {'title': 'forme désidérative présent négatif (je ne veux pas...)', 'field': 'desideratif_present_neg'},
    {'title': 'forme désidérative passé (je voulais...)', 'field': 'desideratif_passe'},
    {'title': 'forme désidérative passé négatif (je ne voulais pas...)', 'field': 'desideratif_passe_neg'},
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
    verbs = Verb.objects.order_by('?')[:count * 10]

    verbs2 = []
    for verb in verbs:
        # Test que la traduction existe
        if not verb.traduction: continue

        # Teste que le champ n'est pas vide
        count -= 1
        while True:
            f = random.randrange(len(verb_forms))
            v = getattr(verb, verb_forms[f]['field'])
            if v: break

        verbs2.append(
            {
                'forme': verb_forms[f]['title'],
                'field': verb_forms[f]['field'],
                'traduction': verb.traduction,
                'kanji': verb.kanji,
                'romaji': verb.romaji,
                'id': verb.id
            }
        )
        if not count: break

    context = { 'verbs': verbs2, 'wc': _word_count(), 'verbs_wc': _verb_count() }
    return render(request, 'index.html', context)


def check_verbs(request):
    results = []
    verbs_id = request.GET.getlist('id')
    verbs_romaji = request.GET.getlist('romaji')
    verbs_kanji = request.GET.getlist('kanji')
    verbs_traduction = request.GET.getlist('traduction')
    verbs_formes = request.GET.getlist('forme')
    verbs_fields = request.GET.getlist('field')
    count = len(verbs_id)
    goods = 0

    for idx, wid in enumerate(verbs_id):
        item = {
            'status': False,
            'romaji': verbs_romaji[idx],
            'kanji': verbs_kanji[idx],
            'traduction': verbs_traduction[idx],
            'forme' : verbs_formes[idx],
            'answer': _normalize(request.GET[verbs_romaji[idx] + "+" + verbs_fields[idx]])
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
