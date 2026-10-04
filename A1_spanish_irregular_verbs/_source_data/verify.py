# -*- coding: utf-8 -*-
"""Cross-check verbecc against Wiktionary's Spanish section, cell by cell."""
import json, sys, unicodedata
sys.path.insert(0,'/home/claude/a3')
from wikt import parse

D = json.load(open('data/verbs.json'))
FULL = [v['verb'] for f in D['families'] for v in f['verbs']]
CHECK = ['Present','Imperfect','Preterite','Future','Conditional',
         'Present Subjunctive','Imperfect Subj. (-ra)','Future Subjunctive']

def norm(s):
    return unicodedata.normalize('NFC', (s or '').strip().lower())

by_verb = {v['verb']: v for f in D['families'] for v in f['verbs']}
checked = mism = 0
problems, skipped = [], []
for v in FULL:
    try:
        w = parse(v)
    except Exception as e:
        skipped.append((v, str(e)[:60])); continue
    for t in CHECK:
        if t not in w: continue
        ours = [c['form'] for c in by_verb[v]['tenses'][t]]
        theirs = w[t]
        for i,(a,b) in enumerate(zip(ours, theirs)):
            checked += 1
            if norm(a) != norm(b):
                mism += 1
                problems.append('%s | %s | slot %d | verbecc=%r wiktionary=%r' % (v,t,i,a,b))
print('verbs cross-checked :', len(FULL)-len(skipped), 'of', len(FULL))
print('cells checked       :', checked)
print('mismatches          :', mism)
for p in problems[:30]: print('   ', p)
for s in skipped: print('   SKIPPED', s)
json.dump({'verbs':len(FULL)-len(skipped),'checked':checked,'mismatches':mism,
           'problems':problems,'skipped':skipped},
          open('data/verification.json','w'), ensure_ascii=False, indent=1)
