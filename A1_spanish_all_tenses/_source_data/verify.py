# -*- coding: utf-8 -*-
"""Independent second derivation of the regular Spanish paradigms, written from the
standard published ending tables, then diffed cell-by-cell against verbecc output.
Two independent derivations agreeing is the substitute for a native reviewer."""
import json

E = {
 'ar': dict(pres=['o','as','a','amos','áis','an'],
            imp =['aba','abas','aba','ábamos','abais','aban'],
            pret=['é','aste','ó','amos','asteis','aron'],
            psub=['e','es','e','emos','éis','en'],
            isra=['ara','aras','ara','áramos','arais','aran'],
            isse=['ase','ases','ase','ásemos','aseis','asen'],
            fsub=['are','ares','are','áremos','areis','aren'],
            part='ado'),
 'er': dict(pres=['o','es','e','emos','éis','en'],
            imp =['ía','ías','ía','íamos','íais','ían'],
            pret=['í','iste','ió','imos','isteis','ieron'],
            psub=['a','as','a','amos','áis','an'],
            isra=['iera','ieras','iera','iéramos','ierais','ieran'],
            isse=['iese','ieses','iese','iésemos','ieseis','iesen'],
            fsub=['iere','ieres','iere','iéremos','iereis','ieren'],
            part='ido'),
 'ir': dict(pres=['o','es','e','imos','ís','en'],
            imp =['ía','ías','ía','íamos','íais','ían'],
            pret=['í','iste','ió','imos','isteis','ieron'],
            psub=['a','as','a','amos','áis','an'],
            isra=['iera','ieras','iera','iéramos','ierais','ieran'],
            isse=['iese','ieses','iese','iésemos','ieseis','iesen'],
            fsub=['iere','ieres','iere','iéremos','iereis','ieren'],
            part='ido'),
}
FUT  = ['é','ás','á','emos','éis','án']         # attached to the full infinitive
COND = ['ía','ías','ía','íamos','íais','ían']
HAB = dict(pres=['he','has','ha','hemos','habéis','han'],
           imp =['había','habías','había','habíamos','habíais','habían'],
           pret=['hube','hubiste','hubo','hubimos','hubisteis','hubieron'],
           fut =['habré','habrás','habrá','habremos','habréis','habrán'],
           cond=['habría','habrías','habría','habríamos','habríais','habrían'],
           psub=['haya','hayas','haya','hayamos','hayáis','hayan'],
           isra=['hubiera','hubieras','hubiera','hubiéramos','hubierais','hubieran'],
           isse=['hubiese','hubieses','hubiese','hubiésemos','hubieseis','hubiesen'],
           fsub=['hubiere','hubieres','hubiere','hubiéremos','hubiereis','hubieren'])

def expect(inf):
    s, cls = inf[:-2], inf[-2:]
    e = E[cls]; P = e['part']; part = s + P
    def simple(k): return [s+x for x in e[k]]
    def comp(k):   return [h+' '+part for h in HAB[k]]
    psub = simple('psub')
    out = {
      'Present': simple('pres'),
      'Imperfect': simple('imp'),
      'Preterite': simple('pret'),
      'Future': [inf+x for x in FUT],
      'Present Perfect': comp('pres'),
      'Past Perfect': comp('imp'),
      'Preterite Perfect': comp('pret'),
      'Future Perfect': comp('fut'),
      'Conditional': [inf+x for x in COND],
      'Conditional Perfect': comp('cond'),
      'Present Subjunctive': psub,
      'Imperfect Subj. (-ra)': simple('isra'),
      'Imperfect Subj. (-se)': simple('isse'),
      'Future Subjunctive': simple('fsub'),
      'Present Perfect Subj.': comp('psub'),
      'Past Perfect Subj. (-ra)': comp('isra'),
      'Past Perfect Subj. (-se)': comp('isse'),
      'Future Perfect Subj.': [h+' '+part for h in HAB['fsub']],
      # commands: tú = 3sg present indic; Ud./nos./Uds. = present subjunctive; vosotros = inf[:-1]+d
      'Affirmative Command': [simple('pres')[2], psub[2], psub[3], s+cls[0]+'d', psub[5]],
      'Negative Command': ['no '+psub[1], 'no '+psub[2], 'no '+psub[3], 'no '+psub[4], 'no '+psub[5]],
    }
    return out

data = json.load(open('/home/claude/a1/data/conjugations.json'))
checked = mismatch = 0
problems = []
for v in data['verbs']:
    exp = expect(v['verb'])
    for g in v['groups']:
        for t in g['tenses']:
            got = [c['form'] for c in t['cells']]
            want = exp[t['en']]
            for i,(a,b) in enumerate(zip(got,want)):
                checked += 1
                if a != b:
                    mismatch += 1
                    problems.append(f"{v['verb']} | {t['en']} | slot {i} | verbecc={a!r} independent={b!r}")
print(f"cells checked : {checked}")
print(f"mismatches    : {mismatch}")
for p in problems[:25]: print("  ", p)
json.dump({'checked':checked,'mismatches':mismatch,'problems':problems},
          open('/home/claude/a1/data/verification.json','w'), ensure_ascii=False, indent=1)
