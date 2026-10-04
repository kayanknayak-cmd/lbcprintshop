# -*- coding: utf-8 -*-
import verbecc, json, re, os, sys
sys.path.insert(0,'/home/claude/a3')

FAMILIES = [
 ("irregular", "Truly irregular", "No pattern. Learn these first, they are the most used verbs in Spanish.",
  ['ser','estar','ir','haber','dar','ver','saber']),
 ("yogo", "Irregular yo", "Regular everywhere except the yo form, which usually gains a g.",
  ['tener','hacer','poner','salir','venir','decir','traer','oír','conocer']),
 ("eie", "Stem change e to ie", "The e in the stem becomes ie, except in nosotros and vosotros.",
  ['pensar','querer','empezar','sentir']),
 ("oue", "Stem change o to ue", "The o in the stem becomes ue, except in nosotros and vosotros.",
  ['poder','dormir','volver','encontrar']),
 ("ei", "Stem change e to i", "The e in the stem becomes i, except in nosotros and vosotros.",
  ['pedir','seguir','servir']),
]
FULL = [v for _,_,_,vs in FAMILIES for v in vs]

INDEX_EXTRA = ['jugar','comenzar','perder','entender','mostrar','recordar','contar','morir',
               'repetir','vestir','caer','valer','conducir','traducir','construir','huir',
               'elegir','sonreír']
ALL_VERBS = FULL + INDEX_EXTRA

SIMPLE = [
 ('Present','Presente','ind'), ('Imperfect','Imperfecto','ind'),
 ('Preterite','Pretérito','ind'), ('Future','Futuro','ind'),
 ('Conditional','Condicional','con'),
 ('Present Subjunctive','Presente subj.','sub'),
 ('Imperfect Subj. (-ra)','Imperfecto subj.','sub'),
 ('Future Subjunctive','Futuro subj.','sub'),
 ('Affirmative Command','Imperativo','imp'),
 ('Negative Command','Imperativo neg.','imp'),
]
KEY = {'Present':('indicativo','presente'),'Imperfect':('indicativo','pretérito-imperfecto'),
 'Preterite':('indicativo','pretérito-perfecto-simple'),'Future':('indicativo','futuro'),
 'Conditional':('condicional','presente'),'Present Subjunctive':('subjuntivo','presente'),
 'Imperfect Subj. (-ra)':('subjuntivo','pretérito-imperfecto-1'),
 'Future Subjunctive':('subjuntivo','futuro'),
 'Affirmative Command':('imperativo','afirmativo'),'Negative Command':('imperativo','negativo')}
PERSONS = [("yo",["yo"]),("tú",["tú"]),("él/ella/Ud.",["él"]),
           ("nosotros",["nosotros"]),("vosotros",["vosotros"]),("ellos/Uds.",["ellos"])]
IMP_PERSONS = [("tú",["tú"]),("Ud.",["usted"]),("nosotros",["nosotros"]),
               ("vosotros",["vosotros"]),("Uds.",["ustedes"])]

E = {'ar':dict(pres=['o','as','a','amos','áis','an'],imp=['aba','abas','aba','ábamos','abais','aban'],
      pret=['é','aste','ó','amos','asteis','aron'],psub=['e','es','e','emos','éis','en'],
      isra=['ara','aras','ara','áramos','arais','aran'],fsub=['are','ares','are','áremos','areis','aren']),
     'er':dict(pres=['o','es','e','emos','éis','en'],imp=['ía','ías','ía','íamos','íais','ían'],
      pret=['í','iste','ió','imos','isteis','ieron'],psub=['a','as','a','amos','áis','an'],
      isra=['iera','ieras','iera','iéramos','ierais','ieran'],fsub=['iere','ieres','iere','iéremos','iereis','ieren']),
     'ir':dict(pres=['o','es','e','imos','ís','en'],imp=['ía','ías','ía','íamos','íais','ían'],
      pret=['í','iste','ió','imos','isteis','ieron'],psub=['a','as','a','amos','áis','an'],
      isra=['iera','ieras','iera','iéramos','ierais','ieran'],fsub=['iere','ieres','iere','iéremos','iereis','ieren'])}
FUT=['é','ás','á','emos','éis','án']; COND=['ía','ías','ía','íamos','íais','ían']
EKEY={'Present':'pres','Imperfect':'imp','Preterite':'pret','Present Subjunctive':'psub',
      'Imperfect Subj. (-ra)':'isra','Future Subjunctive':'fsub'}

def regular_forms(inf, tense):
    cls = inf[-2:]
    if cls not in E: return None
    stem = inf[:-2]
    if tense == 'Future':       return [inf+x for x in FUT]
    if tense == 'Conditional':  return [inf+x for x in COND]
    k = EKEY.get(tense)
    return [stem+x for x in E[cls][k]] if k else None

def mark(form, reg):
    """Wrap the part of `form` that deviates from the regular form. Powers the
    highlight that shows a learner exactly which letters change."""
    if not reg or form == reg: return None
    a, b = form, reg
    i = 0
    while i < min(len(a),len(b)) and a[i]==b[i]: i += 1
    j = 0
    while j < min(len(a),len(b))-i and a[len(a)-1-j]==b[len(b)-1-j]: j += 1
    return (a[:i], a[i:len(a)-j] or '', a[len(a)-j:] if j else '')

def strip_pronoun(form, pr):
    f = form.strip()
    neg = f.startswith('no ')
    if neg: f = f[3:]
    if f.startswith(pr+' '): f = f[len(pr)+1:]
    return ('no '+f) if neg else f

c = verbecc.CompleteConjugator(lang='es')
data = {'families':[], 'index':[], 'simple':[(a,b,m) for a,b,m in SIMPLE]}
gate = []
for v in ALL_VERBS:
    r = c.conjugate(v)
    info = json.loads(str(r._verb_info))
    gate.append((v, info['predicted'], info['template']))
    assert info['predicted'] is False, "%s: verbecc PREDICTED this verb. Not shippable." % v

def build(v):
    r = c.conjugate(v); moods = json.loads(str(r._moods_conjugation))
    out = {'verb': v, 'tenses': {}}
    for en, es, mood in SIMPLE:
        m, t = KEY[en]; rows = moods[m][t]
        people = IMP_PERSONS if m=='imperativo' else PERSONS
        reg = regular_forms(v, en)
        cells = []
        for idx,(label,prons) in enumerate(people):
            hit = next((x for x in rows if x.get('pr') in prons), None)
            f = strip_pronoun(hit['c'][0], hit['pr']) if hit else None
            mk = mark(f, reg[idx]) if (reg and f and m!='imperativo') else None
            cells.append({'person':label,'form':f,'mark':mk})
        out['tenses'][en] = cells
    return out

for key, name, blurb, verbs in FAMILIES:
    data['families'].append({'key':key,'name':name,'blurb':blurb,
                             'verbs':[build(v) for v in verbs]})
for v in ALL_VERBS:
    b = build(v)
    data['index'].append({'verb':v,'yo':b['tenses']['Present'][0]['form'],
        'pret_yo':b['tenses']['Preterite'][0]['form'],
        'sub_yo':b['tenses']['Present Subjunctive'][0]['form'],
        'el':b['tenses']['Present'][2]['form']})
data['gate'] = gate
json.dump(data, open('data/verbs.json','w'), ensure_ascii=False)
print('verbs fully conjugated:', len(FULL))
print('verbs in the index    :', len(ALL_VERBS))
print('all predicted=False   :', all(not p for _,p,_ in gate))
print('sample tener/Present  :', [x['form'] for x in data['families'][1]['verbs'][0]['tenses']['Present']])
print('sample pensar marks   :', [x['mark'] for x in data['families'][2]['verbs'][0]['tenses']['Present']])
