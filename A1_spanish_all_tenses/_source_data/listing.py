# -*- coding: utf-8 -*-
import json, os, sys
sys.path.insert(0,'/home/claude/a1/build')
D = json.load(open('/home/claude/a1/data/conjugations.json'))
V = {v['verb']: v for v in D['verbs']}
ORDER = ['hablar','comer','vivir']
G, A, INK, BODY = '#EFE4D2', '#A34234', '#1C1A17', '#3A342C'

def tense(verb, en):
    for g in V[verb]['groups']:
        for t in g['tenses']:
            if t['en'] == en: return t

def card_table(en, es, accent=A, verbs=ORDER, fs=56, ph=300):
    ts = {v: tense(v, en) for v in verbs}
    people = [c['person'] for c in ts[verbs[0]]['cells']]
    rows=''
    for i,p in enumerate(people):
        rows += '<tr><th>%s</th>%s</tr>' % (p, ''.join('<td>%s</td>' % ts[v]['cells'][i]['form'] for v in verbs))
    head = ''.join('<td class="vh">%s</td>' % v for v in verbs)
    return ('<div class="ct" style="--m:%s;--fs:%dpx;--ph:%dpx">'
            '<div class="cth"><span>%s</span><span class="es">%s</span></div>'
            '<table><tr class="vhr"><th></th>%s</tr>%s</table></div>' % (accent, fs, ph, en, es, head, rows))

BASE = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:2000px;height:2000px}
.canvas{width:2000px;height:2000px;position:relative;overflow:hidden;background:%(G)s}
.safe{position:absolute;left:200px;top:0;width:1600px;height:2000px;display:flex;
 flex-direction:column;justify-content:center;align-items:center;text-align:center}
.mark{display:flex;gap:14px;align-items:center}
.mark i{display:block;width:44px;height:13px;border-radius:7px;background:%(A)s}
.mark i.b{background:%(INK)s;opacity:.85}
.mark i.c{background:%(A)s;opacity:.45}
.eyebrow{font-family:Inter,sans-serif;font-weight:600;font-size:38px;letter-spacing:.22em;
 text-transform:uppercase;color:%(A)s}
.big{font-family:Fraunces,serif;font-weight:900;font-size:300px;line-height:.86;
 letter-spacing:-.022em;color:%(INK)s}
.sub{font-family:Fraunces,serif;font-weight:900;font-style:italic;font-size:118px;
 line-height:1;letter-spacing:-.01em;color:%(A)s}
.facts{display:flex;gap:26px;align-items:center;font-family:Inter,sans-serif;font-weight:600;
 font-size:46px;white-space:nowrap;color:%(BODY)s}
.dot{width:12px;height:12px;border-radius:50%%;background:%(A)s;display:inline-block;flex:0 0 auto}
.ct{background:#fff;border-radius:26px;overflow:hidden;
 box-shadow:0 40px 90px rgba(30,18,10,.22),0 8px 22px rgba(30,18,10,.10);width:100%%}
.cth{background:var(--m);color:#fff;display:flex;justify-content:space-between;align-items:baseline;
 padding:26px 38px;font-family:Inter,sans-serif;font-weight:700;font-size:52px}
.cth .es{font-weight:400;font-size:34px;opacity:.85}
.ct table{width:100%%;border-collapse:collapse}
.ct th{text-align:left;color:#6B6358;font-weight:500;font-size:calc(var(--fs)*.80);
 padding:16px 38px;width:var(--ph);white-space:nowrap;font-family:Inter,sans-serif}
.ct td{font-weight:600;color:%(INK)s;font-size:var(--fs);padding:16px 24px;white-space:nowrap;
 font-family:Inter,sans-serif}
.ct tbody tr:nth-child(even) td,.ct tbody tr:nth-child(even) th{background:rgba(28,26,23,.04)}
.ct .vhr td{font-family:Fraunces,serif;font-weight:900;color:var(--m);background:none!important;
 font-size:calc(var(--fs)*.88);padding-bottom:6px}
.ct .vhr th{background:none!important}
.ttl{font-family:Fraunces,serif;font-weight:900;font-size:132px;line-height:.94;color:%(INK)s;
 letter-spacing:-.02em}
.lead{font-family:Inter,sans-serif;font-weight:500;font-size:46px;line-height:1.42;color:%(BODY)s}
.paper{background:#fff;border-radius:14px;box-shadow:0 30px 70px rgba(30,18,10,.20),0 6px 16px rgba(30,18,10,.10)}
.paper img{display:block;width:100%%;border-radius:14px}
.num{font-family:Fraunces,serif;font-weight:900;font-size:78px;color:%(A)s;line-height:1}
.rowitem{display:flex;gap:34px;align-items:flex-start;text-align:left}
.rowitem h3{font-family:Inter,sans-serif;font-weight:700;font-size:54px;color:%(INK)s}
.rowitem p{font-family:Inter,sans-serif;font-weight:500;font-size:40px;color:%(BODY)s;line-height:1.35;margin-top:8px}
.chip{font-family:Inter,sans-serif;font-weight:700;font-size:40px;color:#fff;background:%(A)s;
 padding:16px 34px;border-radius:999px;white-space:nowrap}
''' % dict(G=G,A=A,INK=INK,BODY=BODY)

def page(inner, extra=''):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">'
            '<style>%s%s</style></head><body>%s</body></html>' % (BASE, extra, inner))

IMGS = {}

# 01 HERO
IMGS['01_hero'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="mark"><i></i><i class="b"></i><i class="c"></i></div>'
 '<div class="eyebrow" style="margin-top:30px">Verb conjugation chart</div>'
 '<div class="big" style="margin-top:26px">SPANISH</div>'
 '<div class="sub" style="margin-top:10px">all 18 tenses</div>'
 + card_table('Present','Presente',fs=58,ph=300).replace('class="ct"','class="ct" style2=""',1)
 + '<div class="facts" style="margin-top:60px"><span>4 print files</span><span class="dot"></span>'
 '<span>18 tenses</span><span class="dot"></span><span>hablar · comer · vivir</span></div>'
 '</div></div>',
 '.ct{margin-top:66px}')

# 02 FULL SET
IMGS['02_full_set'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">Everything in the download</div>'
 '<div class="ttl" style="margin-top:20px">4 print files, 14 pages</div>'
 '<div class="fan">'
 '<div class="paper p1"><img src="assets/poster_0.png"></div>'
 '<div class="paper p2"><img src="assets/letter_0.png"></div>'
 '<div class="paper p3"><img src="assets/letter_3.png"></div>'
 '<div class="paper p4"><img src="assets/practice_0.png"></div>'
 '</div>'
 '<div class="facts" style="margin-top:44px"><span>18x24 poster</span><span class="dot"></span>'
 '<span>US Letter</span><span class="dot"></span><span>A4</span><span class="dot"></span>'
 '<span>Practice grids</span></div>'
 '</div></div>',
 '''.fan{position:relative;width:1600px;height:790px;margin-top:26px}
.fan .paper{position:absolute;bottom:0}
.p1{width:560px;left:60px;transform:rotate(-6deg);z-index:1}
.p2{width:440px;left:480px;transform:rotate(-1.5deg);z-index:2}
.p3{width:440px;left:790px;transform:rotate(3deg);z-index:3}
.p4{width:390px;left:1090px;transform:rotate(7deg);z-index:4}''')

# 03 THE POSTER
IMGS['03_poster'] = page(
 '<div class="canvas" style="background:#E7DAC6"><div class="safe">'
 '<div class="eyebrow">File 1 of 4</div>'
 '<div class="ttl" style="margin-top:20px">The 18x24 poster</div>'
 '<div class="paper" style="width:1080px;margin-top:44px"><img src="assets/poster_0.png"></div>'
 '<div class="facts" style="margin-top:44px"><span>Every tense on one sheet</span>'
 '<span class="dot"></span><span>Colour-coded by mood</span></div>'
 '</div></div>')

# 04 ONE PAGE PER VERB
IMGS['04_pages'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">Files 2 and 3 of 4</div>'
 '<div class="ttl" style="margin-top:20px">One page per verb</div>'
 '<div class="lead" style="margin-top:24px;max-width:1380px">US Letter and A4, three pages plus a '
 'quick-reference page. Same chart, sized for a binder.</div>'
 '<div class="three">'
 '<div class="paper"><img src="assets/letter_0.png"></div>'
 '<div class="paper"><img src="assets/letter_1.png"></div>'
 '<div class="paper"><img src="assets/letter_2.png"></div>'
 '</div>'
 '<div class="facts" style="margin-top:40px"><span>hablar</span><span class="dot"></span>'
 '<span>comer</span><span class="dot"></span><span>vivir</span></div>'
 '</div></div>',
 '.three{display:flex;gap:44px;margin-top:44px;width:100%}.three .paper{width:calc((100% - 88px)/3)}')

# 05 DETAIL CROP
IMGS['05_detail'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">Actual type size</div>'
 '<div class="ttl" style="margin-top:20px">Readable across<br>the room</div>'
 + card_table('Preterite','Pretérito perfecto simple',fs=62,ph=320)
 + '<div class="facts" style="margin-top:52px"><span>Six persons</span><span class="dot"></span>'
 '<span>Three model verbs</span><span class="dot"></span><span>No abbreviations</span></div>'
 '</div></div>',
 '.ct{margin-top:56px}')

# 06 IN CONTEXT / SCALE
IMGS['06_scale'] = page(
 '<div class="canvas" style="background:#E3D6C1"><div class="safe">'
 '<div class="eyebrow">Printed size</div>'
 '<div class="wallwrap">'
 '<div class="dimtop"><span class="dl"></span><span class="dnum">18 in</span><span class="dl"></span></div>'
 '<div class="wallrow">'
 '<div class="paper wall"><img src="assets/poster_0.png"></div>'
 '<div class="dimside"><span class="dlv"></span><span class="dnum">24 in</span><span class="dlv"></span></div>'
 '</div></div>'
 '<div class="facts" style="margin-top:50px"><span>Print at home on Letter or A4</span>'
 '<span class="dot"></span><span>Or send the 18x24 to a print shop</span></div>'
 '</div></div>',
 '''.wallwrap{margin-top:46px;display:flex;flex-direction:column;align-items:center}
.wallrow{display:flex;align-items:stretch;gap:34px}
.wall{width:900px}
.dimtop{display:flex;align-items:center;gap:22px;width:900px;margin-bottom:24px;margin-right:120px}
.dl{flex:1;height:4px;background:rgba(28,26,23,.35)}
.dlv{flex:1;width:4px;background:rgba(28,26,23,.35);margin:0 auto}
.dimside{display:flex;flex-direction:column;align-items:center;gap:22px}
.dnum{font-family:Inter,sans-serif;font-weight:700;font-size:44px;color:#1C1A17;white-space:nowrap}''')

# 07 FORMATS
IMGS['07_formats'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">Sizes included</div>'
 '<div class="ttl" style="margin-top:20px">Three sizes,<br>one download</div>'
 '<div class="szrow">'
 '<div class="sz"><div class="box b1"></div><div class="szl">18 x 24 in</div><div class="szs">Wall poster</div></div>'
 '<div class="sz"><div class="box b2"></div><div class="szl">8.5 x 11 in</div><div class="szs">US Letter</div></div>'
 '<div class="sz"><div class="box b3"></div><div class="szl">210 x 297 mm</div><div class="szs">A4</div></div>'
 '</div>'
 '<div class="facts" style="margin-top:56px"><span>PDF</span><span class="dot"></span>'
 '<span>Vector text, sharp at any size</span></div>'
 '</div></div>',
 '''.szrow{display:flex;gap:80px;align-items:flex-end;margin-top:70px}
.sz{display:flex;flex-direction:column;align-items:center;gap:24px}
.box{background:#fff;border:5px solid #A34234;border-radius:10px;
 box-shadow:0 20px 44px rgba(30,18,10,.16)}
.b1{width:390px;height:520px}.b2{width:270px;height:350px}.b3{width:258px;height:365px}
.szl{font-family:Inter,sans-serif;font-weight:700;font-size:48px;color:#1C1A17}
.szs{font-family:Inter,sans-serif;font-weight:500;font-size:38px;color:#3A342C;margin-top:-14px}''')

# 08 WHAT'S INSIDE
INSIDE = [("11 simple tenses","Present, imperfect, preterite, future, conditional, three subjunctives, two commands."),
          ("8 compound tenses","Every haber form, laid out once so you can build them all."),
          ("The endings on their own","The -ar, -er and -ir patterns behind every form on the sheet."),
          ("Voseo","The vos forms, and exactly which tenses they change."),
          ("Blank practice grids","The same layout, empty, for any verb you want to drill.")]
IMGS['08_inside'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">What is inside</div>'
 '<div class="ttl" style="margin-top:20px">Five things,<br>not one table</div>'
 '<div class="list">' + ''.join(
   '<div class="rowitem"><div class="num">%02d</div><div><h3>%s</h3><p>%s</p></div></div>' % (i+1,t,d)
   for i,(t,d) in enumerate(INSIDE)) + '</div>'
 '</div></div>',
 '.list{display:flex;flex-direction:column;gap:44px;margin-top:60px;width:100%}')

# 09 HOW IT WORKS
STEPS=[("Buy and download","The files are yours the moment payment clears. Nothing ships."),
       ("Print what you need","18x24 at a print shop, or Letter and A4 at home."),
       ("Drill with the blank grids","Fill one in from memory, then check it against the chart.")]
IMGS['09_how'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">How it works</div>'
 '<div class="ttl" style="margin-top:20px">Three steps</div>'
 '<div class="list">' + ''.join(
   '<div class="rowitem"><div class="num">%d</div><div><h3>%s</h3><p>%s</p></div></div>' % (i+1,t,d)
   for i,(t,d) in enumerate(STEPS)) + '</div>'
 '<div class="facts" style="margin-top:70px"><span>No account needed</span><span class="dot"></span>'
 '<span>No software to install</span></div>'
 '</div></div>',
 '.list{display:flex;flex-direction:column;gap:52px;margin-top:64px;width:100%}')

# 10 FILE LIST
FILES=[("1_poster_18x24.pdf","1 page","18 x 24 in"),
       ("2_charts_us_letter.pdf","4 pages","8.5 x 11 in"),
       ("3_charts_a4.pdf","4 pages","210 x 297 mm"),
       ("4_practice_grids.pdf","2 pages","Letter + A4")]
IMGS['10_files'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">Your download</div>'
 '<div class="ttl" style="margin-top:20px">4 PDFs</div>'
 '<div class="ftable">' + ''.join(
   '<div class="frow"><span class="fn">%s</span><span class="fp">%s</span><span class="fs">%s</span></div>'
   % f for f in FILES) + '</div>'
 '<div class="chip" style="margin-top:56px">11 pages of reference + 2 of practice + the poster</div>'
 '</div></div>',
 '''.ftable{margin-top:60px;width:100%;background:#fff;border-radius:22px;overflow:hidden;
 box-shadow:0 30px 70px rgba(30,18,10,.18)}
.frow{display:flex;align-items:center;justify-content:space-between;padding:38px 46px;
 border-bottom:2px solid rgba(28,26,23,.08);font-family:Inter,sans-serif}
.frow:last-child{border-bottom:none}
.fn{font-weight:700;font-size:46px;color:#1C1A17}
.fp{font-weight:600;font-size:40px;color:#A34234}
.fs{font-weight:500;font-size:40px;color:#3A342C}''')

os.makedirs('/home/claude/a1/build/lhtml', exist_ok=True)
for k,v in IMGS.items():
    open('/home/claude/a1/build/lhtml/%s.html'%k,'w').write(v)
print('wrote', len(IMGS), 'listing pages')
