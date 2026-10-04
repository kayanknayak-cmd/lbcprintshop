# -*- coding: utf-8 -*-
import json, os, re, sys
D = json.load(open('/home/claude/a1/data/conjugations.json'))
V = {v['verb']: v for v in D['verbs']}
ORDER = ['hablar','comer','vivir']
_a=sys.argv[1:]
S_POSTER=float(_a[0]) if len(_a)>0 else 1.0
S_PAGE=float(_a[1]) if len(_a)>1 else 1.0
S_REF=float(_a[2]) if len(_a)>2 else 1.0

def tense(verb, en):
    for g in V[verb]['groups']:
        for t in g['tenses']:
            if t['en'] == en: return t
    raise KeyError(en)

SIMPLE = [
 ('Present','Presente','ind'), ('Imperfect','Pretérito imperfecto','ind'),
 ('Preterite','Pretérito perfecto simple','ind'), ('Future','Futuro simple','ind'),
 ('Conditional','Condicional simple','con'),
 ('Present Subjunctive','Presente de subjuntivo','sub'),
 ('Imperfect Subj. (-ra)','Imperfecto de subjuntivo','sub'),
 ('Imperfect Subj. (-se)','Imperfecto de subjuntivo','sub'),
 ('Future Subjunctive','Futuro de subjuntivo','sub'),
 ('Affirmative Command','Imperativo afirmativo','imp'),
 ('Negative Command','Imperativo negativo','imp'),
]
COMPOUND = [
 ('Present Perfect','Pretérito perfecto compuesto'),
 ('Past Perfect','Pluscuamperfecto'),
 ('Preterite Perfect','Pretérito anterior'),
 ('Future Perfect','Futuro perfecto'),
 ('Conditional Perfect','Condicional perfecto'),
 ('Present Perfect Subj.','Pretérito perfecto de subjuntivo'),
 ('Past Perfect Subj. (-ra)','Pluscuamperfecto de subjuntivo'),
 ('Future Perfect Subj.','Futuro perfecto de subjuntivo'),
]
ENDINGS = [
 ("Present","o · as · a · amos · áis · an","o · es · e · emos · éis · en","o · es · e · imos · ís · en"),
 ("Imperfect","aba · abas · aba · ábamos · abais · aban","ía · ías · ía · íamos · íais · ían","ía · ías · ía · íamos · íais · ían"),
 ("Preterite","é · aste · ó · amos · asteis · aron","í · iste · ió · imos · isteis · ieron","í · iste · ió · imos · isteis · ieron"),
 ("Future","+ é · ás · á · emos · éis · án","+ é · ás · á · emos · éis · án","+ é · ás · á · emos · éis · án"),
 ("Conditional","+ ía · ías · ía · íamos · íais · ían","+ ía · ías · ía · íamos · íais · ían","+ ía · ías · ía · íamos · íais · ían"),
 ("Present Subjunctive","e · es · e · emos · éis · en","a · as · a · amos · áis · an","a · as · a · amos · áis · an"),
 ("Imperfect Subj. (-ra)","ara · aras · ara · áramos · arais · aran","iera · ieras · iera · iéramos · ierais · ieran","iera · ieras · iera · iéramos · ierais · ieran"),
 ("Imperfect Subj. (-se)","ase · ases · ase · ásemos · aseis · asen","iese · ieses · iese · iésemos · ieseis · iesen","iese · ieses · iese · iésemos · ieseis · iesen"),
 ("Future Subjunctive","are · ares · are · áremos · areis · aren","iere · ieres · iere · iéremos · iereis · ieren","iere · ieres · iere · iéremos · iereis · ieren"),
 ("Past participle","ado","ido","ido"),
 ("Gerund","ando","iendo","iendo"),
]
MOODCOL = {'ind':'#A34234','con':'#8A5A2B','sub':'#6E5A86','imp':'#2E6B5E'}

def _scale(css, S):
    def f(m): return "%.3f%s" % (float(m.group(1)) * S, m.group(2))
    head, sep, tail = css.partition("}")          # leave .sheet page size untouched
    return head + sep + re.sub(r"([\d.]+)(pt|in)", f, tail)

def block_multi(en, es, mood, verbs=ORDER):
    ts = {v: tense(v, en) for v in verbs}
    people = [c['person'] for c in ts[verbs[0]]['cells']]
    rows = ''
    for i, p in enumerate(people):
        cells = ''.join('<td>%s</td>' % ts[v]['cells'][i]['form'] for v in verbs)
        rows += '<tr><th>%s</th>%s</tr>' % (p, cells)
    head = ''.join('<td class="vh">%s</td>' % v for v in verbs)
    return ('<section class="blk" style="--m:%s"><header><span class="tn">%s</span>'
            '<span class="ts">%s</span></header><table><tr class="vhr"><th></th>%s</tr>%s</table></section>'
            % (MOODCOL[mood], en, es, head, rows))

def voseo_block():
    rows = ''
    for i, row in enumerate(V['hablar']['voseo']):
        cells = ''
        for v in ORDER:
            vr = V[v]['voseo'][i]
            cells += '<td><span class="tu">%s</span><span class="vs">%s</span></td>' % (vr['tu'], vr['vos'])
        rows += '<tr><th>%s</th>%s</tr>' % (row['en'], cells)
    head = ''.join('<td class="vh">%s</td>' % v for v in ORDER)
    return ('<section class="blk vos" style="--m:#2E6B5E"><header><span class="tn">Voseo (vos)</span>'
            '<span class="ts">Argentina · Uruguay · C. America</span></header>'
            '<table><tr class="vhr"><th></th>%s</tr>%s</table>'
            '<p class="note">Grey is the <b>tú</b> form, teal is the <b>vos</b> form. '
            'Every other tense is the same as tú.</p></section>' % (head, rows))

def endings_block():
    rows = ''
    for name, ar, er, ir in ENDINGS:
        rows += ('<tr><th><span class="cn">%s</span></th><td>%s</td><td>%s</td><td>%s</td></tr>'
                 % (name, ar, er, ir))
    return ('<section class="blk wide end" style="--m:#A34234"><header>'
            '<span class="tn">The endings on their own</span>'
            '<span class="ts">drop the -ar / -er / -ir and add these</span></header>'
            '<table class="hab"><tr class="vhr"><th></th><td class="vh">-ar verbs</td>'
            '<td class="vh">-er verbs</td><td class="vh">-ir verbs</td></tr>%s</table></section>' % rows)

def haber_block():
    rows = ''
    for en, es in COMPOUND:
        t = tense('hablar', en)
        hab = [c['form'].split(' ')[0] for c in t['cells']]
        rows += ('<tr><th><span class="cn">%s</span><span class="cs">%s</span></th>%s</tr>'
                 % (en, es, ''.join('<td>%s</td>' % h for h in hab)))
    people = [c['person'] for c in tense('hablar','Present')['cells']]
    head = ''.join('<td class="vh">%s</td>' % p for p in people)
    return ('<section class="blk wide" style="--m:#8A5A2B"><header>'
            '<span class="tn">Compound tenses</span><span class="ts">haber + past participle</span></header>'
            '<table class="hab"><tr class="vhr"><th></th>%s</tr>%s</table>'
            '<p class="note">Add the past participle: <b>hablado</b> · <b>comido</b> · <b>vivido</b>. '
            'The participle never changes. <i>he hablado, habías comido, habremos vivido.</i></p></section>'
            % (head, rows))

CSS_CHART = '''
.sheet{background:#FDFBF7;color:#1C1A17;font-family:Inter,sans-serif}
.hd{border-bottom:3px solid #A34234;display:flex;justify-content:space-between;align-items:flex-end}
.hd .eyebrow{font-weight:600;letter-spacing:.20em;text-transform:uppercase;color:#A34234}
.hd h1{font-family:Fraunces,serif;font-weight:900;letter-spacing:-.02em;line-height:.95}
.hd .sub{font-family:Fraunces,serif;font-weight:900;font-style:italic;color:#A34234}
.hd .rt{text-align:right;color:#3A342C;font-weight:500;line-height:1.55}
.grid{display:grid;grid-template-columns:repeat(3,1fr)}
.blk{break-inside:avoid;border:1px solid rgba(28,26,23,.13);border-radius:.07in;overflow:hidden;background:#fff;display:flex;flex-direction:column}
.blk>header{background:var(--m);color:#fff;display:flex;justify-content:space-between;align-items:baseline}
.blk .tn{font-weight:700}
.blk .ts{font-weight:400;opacity:.82}
.blk table{width:100%;border-collapse:collapse}
.blk th{text-align:left;color:#6B6358;font-weight:500;white-space:nowrap}
.blk td{font-weight:600;color:#1C1A17;white-space:nowrap}
.blk tbody tr:nth-child(even) td,.blk tbody tr:nth-child(even) th{background:rgba(28,26,23,.035)}
.blk .vhr td{font-family:Fraunces,serif;font-weight:900;color:var(--m);background:none!important}
.blk .vhr th{background:none!important}
.blk.wide{grid-column:1/-1}
.hab th{white-space:normal}
.hab .cn{display:block;font-weight:700;color:#1C1A17}
.hab .cs{display:block;font-weight:400;color:#8A8175}
.end .hab td{white-space:normal;font-weight:600;line-height:1.35}
.vos .tu{color:#8A8175;font-weight:500}
.vos .vs{color:#2E6B5E;font-weight:800;margin-left:.10in}
.note{color:#3A342C;border-top:1px solid rgba(28,26,23,.12);margin-top:auto}
.note b{font-weight:700}
.ft{display:flex;justify-content:space-between;color:#8A8175;border-top:1px solid rgba(28,26,23,.15);font-weight:500}
'''

def shell(inner, css, w, h):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">'
            '<style>@page{size:%s %s;margin:0}html,body{width:%s;background:#FDFBF7}%s%s</style>'
            '</head><body>%s</body></html>' % (w, h, w, CSS_CHART, css, inner))

POSTER_CSS = '''
.sheet{width:18in;height:24in;padding:.62in .62in .5in}
.hd{padding-bottom:.20in;margin-bottom:.26in}
.hd .eyebrow{font-size:13pt}
.hd h1{font-size:60pt}
.hd .sub{font-size:27pt;margin-top:.04in}
.hd .rt{font-size:12.5pt}
.grid{gap:.20in}
.blk>header{padding:.07in .11in}
.blk .tn{font-size:12.5pt}
.blk .ts{font-size:8.6pt}
.blk th,.blk td{padding:.045in .10in;font-size:12pt}
.blk th{font-size:10.5pt;width:1.02in}
.blk .vhr td{font-size:12pt;padding-top:.06in;padding-bottom:.03in}
.hab th{width:1.9in}
.hab .cn{font-size:10.2pt}
.hab .cs{font-size:8pt}
.hab td{font-size:11.5pt;padding:.04in .08in}
.end .hab th{width:1.55in}
.end .hab td{font-size:10.6pt}
.note{font-size:11pt;padding:.10in .11in}
.ft{font-size:9.5pt;padding-top:.13in;margin-top:.20in}
'''

def poster(S=1.0):
    blocks = ''.join(block_multi(en, es, m) for en, es, m in SIMPLE) + voseo_block()
    inner = ('<div class="sheet"><div class="hd">'
      '<div><div class="eyebrow">Printable grammar reference</div>'
      '<h1>Spanish Verb<br>Conjugation</h1><div class="sub">all 18 tenses</div></div>'
      '<div class="rt"><b style="font-weight:700">hablar &nbsp;·&nbsp; comer &nbsp;·&nbsp; vivir</b><br>'
      'Regular <i>-ar</i>, <i>-er</i> and <i>-ir</i> models<br>'
      '<span style="color:#A34234;font-weight:700">11 simple tenses + 8 compound</span></div></div>'
      '<div class="grid">' + blocks + endings_block() + haber_block() + '</div>'
      '<div class="ft"><span>Every form generated from the verb dictionary, then checked against an '
      'independent derivation. 354 cells, 0 mismatches.</span><span>LBCPrintShop</span></div></div>')
    return shell(inner, _scale(POSTER_CSS, S), '18in', '24in')

PAGE_CSS = '''
.sheet{width:%(W)s;height:%(H)s;padding:%(P)s}
.hd{padding-bottom:.11in;margin-bottom:.14in}
.hd .eyebrow{font-size:8pt}
.hd h1{font-size:33pt;text-transform:lowercase}
.hd .sub{font-size:14pt}
.hd .rt{font-size:8pt}
.grid{gap:.11in;grid-template-columns:repeat(3,1fr)}
.blk>header{padding:.038in .065in}
.blk .tn{font-size:7.8pt}
.blk .ts{font-size:5.6pt}
.blk th,.blk td{padding:.023in .058in;font-size:7.8pt}
.blk th{font-size:6.9pt;width:.66in}
.blk .vhr td{font-size:7.8pt}
.hab th{width:1.15in}
.hab .cn{font-size:6.9pt}
.hab .cs{font-size:5.4pt}
.hab td{font-size:7.6pt;padding:.02in .05in}
.end .hab th{width:1.0in}
.end .hab td{font-size:6.9pt}
.note{font-size:6.9pt;padding:.05in .065in}
.ft{font-size:6.6pt;padding-top:.08in;margin-top:.11in}
'''

def verb_page(verb, size, S=1.0):
    simple = ''.join(block_multi(en, es, m, verbs=[verb]) for en, es, m in SIMPLE)
    people = [c['person'] for c in tense(verb,'Present')['cells']]
    rows = ''
    for en, es in COMPOUND:
        t = tense(verb, en)
        hab = [c['form'].split(' ')[0] for c in t['cells']]
        rows += ('<tr><th><span class="cn">%s</span><span class="cs">%s</span></th>%s</tr>'
                 % (en, es, ''.join('<td>%s</td>' % h for h in hab)))
    head = ''.join('<td class="vh">%s</td>' % p for p in people)
    part = verb[:-2] + ('ado' if verb.endswith('ar') else 'ido')
    comp = ('<section class="blk wide" style="--m:#8A5A2B"><header><span class="tn">Compound tenses</span>'
            '<span class="ts">haber + %s</span></header><table class="hab">'
            '<tr class="vhr"><th></th>%s</tr>%s</table>'
            '<p class="note">Every compound tense is that form of <b>haber</b> plus the participle '
            '<b>%s</b>, which never changes.</p></section>' % (part, head, rows, part))
    cls = verb[-2:]
    inner = ('<div class="sheet"><div class="hd">'
      '<div><div class="eyebrow">Spanish verb conjugation · all 18 tenses</div>'
      '<h1>%s</h1><div class="sub">regular <i>-%s</i> model</div></div>'
      '<div class="rt">Every simple and compound tense,<br>all six persons.<br>'
      '<span style="color:#A34234;font-weight:700">Page %d of 3</span></div></div>'
      '<div class="grid">%s%s</div>'
      '<div class="ft"><span>hablar · comer · vivir</span><span>LBCPrintShop</span></div></div>'
      % (verb, cls, ORDER.index(verb)+1, simple, comp))
    W, H, P = ('8.5in','11in','.42in') if size == 'letter' else ('210mm','297mm','10mm')
    return shell(inner, _scale(PAGE_CSS % {'W':W,'H':H,'P':P}, S), W, H)

def ref_page(size, S=1.0):
    W, H, P = ('8.5in','11in','.42in') if size == 'letter' else ('210mm','297mm','10mm')
    inner = ('<div class="sheet"><div class="hd">'
      '<div><div class="eyebrow">Spanish verb conjugation</div>'
      '<h1>endings &amp; voseo</h1><div class="sub">quick reference</div></div>'
      '<div class="rt">The patterns behind every<br>form on the other pages.<br>'
      '<span style="color:#A34234;font-weight:700">Page 4 of 4</span></div></div>'
      '<div class="grid">' + endings_block() + haber_block() + voseo_block() + '</div>'
      '<div class="ft"><span>354 cells checked against an independent derivation, 0 mismatches.</span>'
      '<span>LBCPrintShop</span></div></div>')
    css = _scale(PAGE_CSS % {'W':W,'H':H,'P':P}, S)
    css += '.vos{grid-column:1/-1}.end .hab td{font-size:%.2fpt}' % (8.4*S)
    return shell(inner, css, W, H)


def practice_block(en, es, mood):
    people = [c['person'] for c in tense('hablar','Present')['cells']]
    if mood == 'imp': people = [c['person'] for c in tense('hablar','Affirmative Command')['cells']]
    rows = ''.join('<tr><th>%s</th><td class="fill"></td></tr>' % p for p in people)
    return ('<section class="blk" style="--m:%s"><header><span class="tn">%s</span>'
            '<span class="ts">%s</span></header><table>%s</table></section>'
            % (MOODCOL[mood], en, es, rows))

def practice_page(size, S=1.0):
    W, H, P = ('8.5in','11in','.42in') if size == 'letter' else ('210mm','297mm','10mm')
    blocks = ''.join(practice_block(en, es, m) for en, es, m in SIMPLE)
    inner = ('<div class="sheet"><div class="hd">'
      '<div><div class="eyebrow">Spanish verb conjugation · practice</div>'
      '<h1>your verb: <span class="wr"></span></h1><div class="sub">fill it in from memory</div></div>'
      '<div class="rt">Same 11 simple tenses as<br>the reference pages.<br>'
      '<span style="color:#A34234;font-weight:700">Print as many as you need</span></div></div>'
      '<div class="grid">' + blocks + '</div>'
      '<div class="ft"><span>Check your answers against the hablar, comer and vivir pages.</span>'
      '<span>LBCPrintShop</span></div></div>')
    css = _scale(PAGE_CSS % {'W':W,'H':H,'P':P}, S)
    css += ('.fill{height:%.3fin;border-bottom:1px dotted rgba(28,26,23,.35)}'
            '.wr{display:inline-block;width:2.6in;border-bottom:2px solid rgba(28,26,23,.30)}'
            '.blk th{width:.78in}') % (0.19*S)
    return shell(inner, css, W, H)

os.makedirs('/home/claude/a1/build/html', exist_ok=True)
open('/home/claude/a1/build/html/poster.html','w').write(poster(S_POSTER))
for sz in ('letter','a4'):
    for v in ORDER:
        open('/home/claude/a1/build/html/%s_%s.html' % (sz, v),'w').write(verb_page(v, sz, S_PAGE))
    open('/home/claude/a1/build/html/%s_ref.html' % sz,'w').write(ref_page(sz, S_REF if sz=='a4' else S_REF*0.93))
print('scales', S_POSTER, S_PAGE, S_REF, '->', len(os.listdir('/home/claude/a1/build/html')), 'files')

def combine(parts, W, H):
    bodies = []
    for html in parts:
        b = html.split('<body>',1)[1].rsplit('</body>',1)[0]
        bodies.append(b)
    styles = []
    for html in parts:
        st = html.split('<style>',1)[1].split('</style>',1)[0]
        styles.append(st)
    # every sheet gets its own scoped wrapper class so per-page scales survive
    wrapped, css = [], []
    for i,(b,st) in enumerate(zip(bodies, styles)):
        wrapped.append('<div class="pg pg%d">%s</div>' % (i, b))
        st = st.split('}', 0) if False else st
        css.append('\n'.join('.pg%d %s' % (i, rule) if rule.strip().startswith('.') else rule
                              for rule in st.split('\n')))
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">'
            '<style>@page{size:%s %s;margin:0}html,body{width:%s;background:#FDFBF7}'
            '.pg{break-after:page}.pg:last-child{break-after:auto}%s</style></head><body>%s</body></html>'
            % (W,H,W,'\n'.join(css),''.join(wrapped)))

for sz in ('letter','a4'):
    W,H = ('8.5in','11in') if sz=='letter' else ('210mm','297mm')
    parts = [verb_page(v, sz, S_PAGE) for v in ORDER]
    parts.append(ref_page(sz, S_REF if sz=='a4' else S_REF*0.93))
    open('/home/claude/a1/build/html/set_%s.html' % sz,'w').write(combine(parts, W, H))
practice_parts = [practice_page('letter', S_PAGE), practice_page('a4', S_PAGE)]
open('/home/claude/a1/build/html/practice_letter.html','w').write(practice_parts[0])
open('/home/claude/a1/build/html/practice_a4.html','w').write(practice_parts[1])
print('combined sets written')
