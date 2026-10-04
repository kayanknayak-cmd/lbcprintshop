# -*- coding: utf-8 -*-
import json, os, glob, warnings
warnings.filterwarnings('ignore')
import pypdf
D = json.load(open('../data/verbs.json'))

# --- every number below is READ FROM THE BUILT PDFs, never typed by hand ---
PDF = {os.path.basename(f): len(pypdf.PdfReader(f).pages) for f in sorted(glob.glob('pdf/*.pdf'))}
N_TOTAL   = sum(PDF.values())
N_LETTER  = PDF['2_charts_us_letter.pdf']
N_A4      = PDF['3_charts_a4.pdf']
N_PRAC    = PDF['4_practice_grids.pdf']
N_POSTER  = PDF['1_poster_18x24.pdf']
N_FILES   = len(PDF)
N_FULL    = sum(len(f['verbs']) for f in D['families'])
N_INDEX   = len(D['index'])
N_FAM     = len(D['families'])
N_TENSES  = len(D['simple'])
print('COUNTS from built files:', dict(files=N_FILES, total=N_TOTAL, letter=N_LETTER,
      a4=N_A4, practice=N_PRAC, full=N_FULL, index=N_INDEX, tenses=N_TENSES))
C = dict(cream='#FFF6EC', ink='#241F1B', body='#6E645B',
         coral='#FF6B4A', coralD='#D0330F', amber='#FFC24A', amberD='#A85C00',
         violet='#B49CFF', violetD='#6B46E0', teal='#5FD9C4', tealD='#0B7A6E',
         blue='#8AC4F5', blueD='#1A6FB5',
         p1='#FFE3DA', p2='#FFF3D1', p3='#EDE4FF', p4='#D7F5EC', p5='#DCEDFF')

BASE = '''
@font-face{font-family:'Fredoka';font-weight:300 700;src:url('fonts/Fredoka_700.woff2') format('woff2-variations');font-display:block}
@font-face{font-family:'Nunito';font-weight:200 900;src:url('fonts/Nunito_700.woff2') format('woff2-variations');font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:2000px;height:2000px}
.canvas{width:2000px;height:2000px;position:relative;overflow:hidden;background:%(cream)s;
 font-family:Nunito,sans-serif;color:%(ink)s}
.safe{position:absolute;left:200px;top:0;width:1600px;height:2000px;display:flex;
 flex-direction:column;justify-content:center;align-items:center;text-align:center}
.eyebrow{font-family:Nunito,sans-serif;font-weight:800;font-size:56px;letter-spacing:.20em;
 text-transform:uppercase;color:%(coralD)s}
.h1{font-family:Fredoka,sans-serif;font-weight:600;font-size:272px;line-height:.92;
 letter-spacing:-.018em;color:%(ink)s}
.h2{font-family:Fredoka,sans-serif;font-weight:600;font-size:132px;line-height:1;color:%(ink)s}
.lead{font-weight:700;font-size:58px;line-height:1.36;color:%(body)s}
.strip{display:flex;gap:26px;align-items:center;justify-content:center;flex-wrap:wrap}
.chip{font-weight:800;font-size:46px;padding:20px 40px;border-radius:999px;white-space:nowrap;
 color:%(ink)s}
.paper{background:#fff;border-radius:20px;box-shadow:0 26px 60px rgba(70,45,25,.18),0 6px 14px rgba(70,45,25,.08);
 overflow:hidden}
.paper img{display:block;width:100%%}
.badge{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;
 border-radius:50%%;background:%(coralD)s;color:#fff;box-shadow:0 18px 40px rgba(120,40,15,.28);
 font-family:Fredoka,sans-serif;font-weight:600;text-align:center;line-height:.98}
.badge .n{font-size:150px}
.badge .l{font-family:Nunito,sans-serif;font-weight:800;font-size:48px;letter-spacing:.10em;
 text-transform:uppercase;margin-top:8px}
.rowitem{display:flex;gap:36px;align-items:flex-start;text-align:left}
.rowitem .num{font-family:Fredoka,sans-serif;font-weight:600;font-size:84px;color:%(coralD)s;line-height:.95;
 min-width:110px}
.rowitem h3{font-family:Fredoka,sans-serif;font-weight:600;font-size:62px;line-height:1.1}
.rowitem p{font-weight:700;font-size:46px;color:%(body)s;line-height:1.32;margin-top:10px}
''' % C

def page(inner, extra=''):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>%s%s</style></head>'
            '<body>%s</body></html>' % (BASE, extra, inner))

def chip(txt, bg):
    return '<span class="chip" style="background:%s">%s</span>' % (bg, txt)

def badge(n, label, style):
    return ('<div class="badge" style="%s"><span class="n">%s</span><span class="l">%s</span></div>'
            % (style, n, label))

# two simple, original flat figures for warmth
PEOPLE = '''
<svg class="folks" viewBox="0 0 420 260" fill="none">
 <ellipse cx="210" cy="243" rx="196" ry="15" fill="%(ink)s" opacity=".07"/>
 <g><rect x="96" y="120" width="104" height="118" rx="46" fill="%(violet)s"/>
    <circle cx="148" cy="82" r="42" fill="%(amber)s"/>
    <path d="M112 74a36 36 0 0 1 72 0v6c-14-8-24-16-36-24-10 12-22 20-36 24z" fill="%(ink)s" opacity=".78"/>
    <rect x="82" y="140" width="34" height="76" rx="17" fill="%(violetD)s" opacity=".85"/>
    <rect x="180" y="140" width="34" height="76" rx="17" fill="%(violetD)s" opacity=".85"/></g>
 <g><rect x="228" y="132" width="98" height="106" rx="44" fill="%(teal)s"/>
    <circle cx="277" cy="96" r="39" fill="%(coral)s"/>
    <path d="M243 90c0-20 15-36 34-36s34 16 34 36c-10-6-20-6-34-14-12 10-22 12-34 14z" fill="%(ink)s" opacity=".78"/>
    <rect x="214" y="150" width="32" height="70" rx="16" fill="%(tealD)s" opacity=".85"/>
    <rect x="308" y="150" width="32" height="70" rx="16" fill="%(tealD)s" opacity=".85"/></g>
 <rect x="252" y="150" width="86" height="60" rx="10" fill="#fff" stroke="%(ink)s" stroke-width="5" opacity=".95"/>
 <path d="M266 168h58M266 182h44M266 196h50" stroke="%(coralD)s" stroke-width="6" stroke-linecap="round"/>
</svg>''' % C

IM = {}

# ---- 01 HERO : volume + badge + promise ----
FAN = ''.join(
 '<div class="paper f%d"><img src="assets/%s.png"></div>' % (i+1, n)
 for i,n in enumerate(['idx1','fam1','tener','pensar','poder','ver','practice']))
IM['01_hero'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">Spanish grammar</div>'
 '<div class="h1" style="margin-top:18px">Irregular<br>Verbs</div>'
 '<div class="strip" style="margin-top:28px">'
 + chip('%d conjugated in full'%N_FULL, C['p1']) + chip('%d in the index'%N_INDEX, C['p3'])
 + chip('Grouped by pattern', C['p4']) + '</div>'
 '<div class="stack">' + FAN
 + badge(str(N_INDEX), 'verbs', 'right:26px;top:36px;width:326px;height:326px;transform:rotate(9deg)')
 + badge(str(N_TOTAL), 'pages', 'left:52px;top:120px;width:282px;height:282px;background:%s;transform:rotate(-8deg)'%C['violetD'])
 + '</div>'
 '</div></div>',
 '''.stack{position:relative;width:1600px;height:820px;margin-top:26px}
.stack .paper{position:absolute;bottom:0}
.f1{width:395px;left:52px;transform:rotate(-9deg);z-index:1}
.f2{width:395px;left:245px;transform:rotate(-5deg);z-index:2}
.f3{width:400px;left:440px;transform:rotate(-1deg);z-index:3}
.f4{width:410px;left:635px;transform:rotate(2deg);z-index:5}
.f5{width:400px;left:835px;transform:rotate(5deg);z-index:4}
.f6{width:385px;left:1020px;transform:rotate(8deg);z-index:3}
.f7{width:360px;left:1180px;transform:rotate(11deg);z-index:2}''')

# ---- 02 WHAT YOU GET ----
IM['02_full_set'] = page(
 '<div class="canvas" style="background:%s"><div class="safe">' % C['p2']
 + '<div class="eyebrow">Everything in the download</div>'
 '<div class="h2" style="margin-top:22px">%d files &middot; %d pages</div>' % (N_FILES, N_TOTAL) +
 '<div class="grid4">'
 '<div><div class="paper"><img src="assets/poster.png"></div>'
 '<div class="cap"><b>18 &times; 24 poster</b><br>All %d verbs, one sheet</div></div>' % N_FULL +
 '<div><div class="paper"><img src="assets/ov.png"></div>'
 '<div class="cap"><b>%d pages, US Letter</b><br>One page per verb</div></div>' % N_LETTER +
 '<div><div class="paper"><img src="assets/pensar.png"></div>'
 '<div class="cap"><b>%d pages, A4</b><br>Same pages, international</div></div>' % N_A4 +
 '<div><div class="paper"><img src="assets/practice.png"></div>'
 '<div class="cap"><b>%d practice pages</b><br>Blank, for any verb</div></div>' % N_PRAC +
 '</div></div></div>',
 '''.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:44px;margin-top:56px;width:100%;align-items:start}
.cap{font-weight:700;font-size:44px;color:#6E645B;line-height:1.3;margin-top:26px;text-align:center}
.cap b{font-family:Fredoka,sans-serif;font-weight:600;font-size:50px;color:#241F1B}''')

# ---- 03 THE POSTER ----
IM['03_poster'] = page(
 '<div class="canvas" style="background:%s"><div class="safe">' % C['p1']
 + '<div class="eyebrow">File 1 of 4</div>'
 '<div class="h2" style="margin-top:20px">The 18 &times; 24 poster</div>'
 '<div class="paper" style="width:1010px;margin-top:46px;position:relative">'
 '<img src="assets/poster.png"></div>'
 '<div class="strip" style="margin-top:46px">'
 + chip('%d verbs'%N_FULL, '#fff') + chip('%d colour-coded patterns'%N_FAM, '#fff') + chip('20pt type', '#fff')
 + '</div></div></div>')

# ---- 04 ONE PAGE PER VERB ----
IM['04_pages'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">%d verb pages</div>' % N_FULL +
 '<div class="h2" style="margin-top:20px">Every tense,<br>one verb at a time</div>'
 '<div class="three">'
 '<div class="paper"><img src="assets/tener.png"></div>'
 '<div class="paper"><img src="assets/pensar.png"></div>'
 '<div class="paper"><img src="assets/poder.png"></div>'
 '</div>'
 '<div class="strip" style="margin-top:44px">'
 + chip('%d tenses'%N_TENSES, C['p1']) + chip('6 persons', C['p3']) + chip('11pt type', C['p4'])
 + '</div></div></div>',
 '.three{display:flex;gap:48px;margin-top:50px;width:100%}.three .paper{width:calc((100% - 96px)/3)}')

# ---- 05 THE HIGHLIGHT IDEA ----
IM['05_detail'] = page(
 '<div class="canvas" style="background:%s"><div class="safe">' % C['p3']
 + '<div class="eyebrow">The part nobody else marks</div>'
 '<div class="h2" style="margin-top:20px">See exactly which<br>letters change</div>'
 '<div class="demo">'
 '<div class="dcard"><div class="dh" style="background:%s">pensar</div>'
 '<table><tr><th>yo</th><td>p<u>i</u>enso</td></tr><tr><th>t&uacute;</th><td>p<u>i</u>ensas</td></tr>'
 '<tr><th>&eacute;l/ella/Ud.</th><td>p<u>i</u>ensa</td></tr><tr><th>nosotros</th><td>pensamos</td></tr>'
 '<tr><th>vosotros</th><td>pens&aacute;is</td></tr><tr><th>ellos/Uds.</th><td>p<u>i</u>ensan</td></tr></table></div>'
 '<div class="dcard"><div class="dh" style="background:%s">dormir</div>'
 '<table><tr><th>yo</th><td>d<u>ue</u>rmo</td></tr><tr><th>t&uacute;</th><td>d<u>ue</u>rmes</td></tr>'
 '<tr><th>&eacute;l/ella/Ud.</th><td>d<u>ue</u>rme</td></tr><tr><th>nosotros</th><td>dormimos</td></tr>'
 '<tr><th>vosotros</th><td>dorm&iacute;s</td></tr><tr><th>ellos/Uds.</th><td>d<u>ue</u>rmen</td></tr></table></div>'
 '</div>'
 '<div class="lead" style="margin-top:44px;max-width:1400px">The stem changes in four places and '
 'stays put in two. Once you see it, you stop guessing.</div>'
 '</div></div>' % (C['violet'], C['teal']),
 '''.demo{display:flex;gap:50px;margin-top:50px;width:100%}
.dcard{flex:1;background:#fff;border-radius:34px;overflow:hidden;box-shadow:0 26px 60px rgba(70,45,25,.16)}
.dh{font-family:Fredoka,sans-serif;font-weight:600;font-size:70px;padding:30px 44px;text-align:left}
.dcard table{width:100%;border-collapse:collapse}
.dcard th{text-align:left;font-weight:700;font-size:46px;color:#8C8177;padding:22px 44px;width:330px;white-space:nowrap}
.dcard td{font-weight:800;font-size:56px;padding:22px 44px;white-space:nowrap;text-align:left}
.dcard tr+tr th,.dcard tr+tr td{border-top:3px solid rgba(36,31,27,.07)}
.dcard u{text-decoration:none;color:#6B46E0;border-bottom:9px solid currentColor;padding-bottom:2px}
.dcard div.dh+table tr td u{color:inherit}''')

# ---- 06 GROUPED BY PATTERN ----
FAMCHIPS = ''.join(chip('%s &middot; %d' % (f['name'], len(f['verbs'])), p)
                   for f,p in zip(D['families'], [C['p1'],C['p2'],C['p3'],C['p4'],C['p5']]))
IM['06_patterns'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">Not an alphabetical list</div>'
 '<div class="h2" style="margin-top:20px">Grouped by what<br>makes them irregular</div>'
 '<div class="strip" style="margin-top:40px;max-width:1500px">' + FAMCHIPS + '</div>'
 '<div class="paper" style="width:900px;margin-top:44px"><img src="assets/fam3.png"></div>'
 '<div class="lead" style="margin-top:34px">Learn one pattern, get four verbs.</div>'
 '</div></div>')

# ---- 07 SIZES ----
IM['07_formats'] = page(
 '<div class="canvas" style="background:%s"><div class="safe">' % C['p4']
 + '<div class="eyebrow">Sizes included</div>'
 '<div class="h2" style="margin-top:20px">Print it big<br>or print it small</div>'
 '<div class="szrow">'
 '<div class="sz"><div class="box b1"></div><div class="szl">18 &times; 24 in</div><div class="szs">Wall poster</div></div>'
 '<div class="sz"><div class="box b2"></div><div class="szl">8.5 &times; 11 in</div><div class="szs">US Letter</div></div>'
 '<div class="sz"><div class="box b3"></div><div class="szl">210 &times; 297 mm</div><div class="szs">A4</div></div>'
 '</div>'
 '<div class="strip" style="margin-top:52px">' + chip('PDF', '#fff') + chip('Vector text, sharp at any size', '#fff') + '</div>'
 '</div></div>',
 '''.szrow{display:flex;gap:96px;align-items:flex-end;margin-top:72px}
.sz{display:flex;flex-direction:column;align-items:center;gap:28px}
.box{background:#fff;border:8px solid #0B7A6E;border-radius:16px;box-shadow:0 22px 46px rgba(70,45,25,.15)}
.b1{width:400px;height:534px}.b2{width:276px;height:357px}.b3{width:264px;height:373px}
.szl{font-family:Fredoka,sans-serif;font-weight:600;font-size:58px}
.szs{font-weight:700;font-size:46px;color:#6E645B;margin-top:-16px}''')

# ---- 08 WHAT'S INSIDE ----
INSIDE = [("%d verbs in full" % N_FULL, "%d tenses, six persons, one page each." % N_TENSES),
          ("%d verbs in the index" % N_INDEX, "The forms people get wrong, for every verb in the pack."),
          ("%d patterns" % N_FAM, "Verbs side by side so the pattern is impossible to miss."),
          ("Blank practice grids","Same layout, empty. Fill one in and check yourself.")]
IM['08_inside'] = page(
 '<div class="canvas" style="background:%s"><div class="safe">' % C['p5']
 + '<div class="eyebrow">What is inside</div>'
 '<div class="h2" style="margin-top:20px">Four things,<br>not one chart</div>'
 '<div class="list">' + ''.join(
   '<div class="rowitem"><div class="num">%02d</div><div><h3>%s</h3><p>%s</p></div></div>' % (i+1,t,d)
   for i,(t,d) in enumerate(INSIDE)) + '</div>'
 '</div></div>',
 '.list{display:flex;flex-direction:column;gap:52px;margin-top:60px;width:100%}')

# ---- 09 HOW IT WORKS ----
STEPS=[("Download","The files are yours as soon as payment clears."),
       ("Print what you need","The poster at a print shop, the pages at home."),
       ("Drill and check","Fill in a blank grid, then check it against the verb page.")]
IM['09_how'] = page(
 '<div class="canvas"><div class="safe">'
 '<div class="eyebrow">How it works</div>'
 '<div class="h2" style="margin-top:18px">Three steps</div>'
 '<div class="folkswrap">' + PEOPLE + '</div>'
 '<div class="list">' + ''.join(
   '<div class="rowitem"><div class="num">%d</div><div><h3>%s</h3><p>%s</p></div></div>' % (i+1,t,d)
   for i,(t,d) in enumerate(STEPS)) + '</div>'
 '</div></div>',
 '''.list{display:flex;flex-direction:column;gap:48px;margin-top:44px;width:100%}
.folkswrap{width:640px;margin-top:36px}.folks{width:100%;display:block}''')

# ---- 10 FILE LIST ----
FILES=[("1_poster_18x24.pdf","%d page"%N_POSTER,"18 &times; 24 in"),
       ("2_charts_us_letter.pdf","%d pages"%N_LETTER,"8.5 &times; 11 in"),
       ("3_charts_a4.pdf","%d pages"%N_A4,"210 &times; 297 mm"),
       ("4_practice_grids.pdf","%d pages"%N_PRAC,"Letter + A4")]
IM['10_files'] = page(
 '<div class="canvas" style="background:%s"><div class="safe">' % C['p2']
 + '<div class="eyebrow">Your download</div>'
 '<div class="h2" style="margin-top:20px">%d PDFs</div>' % N_FILES +
 '<div class="ftable">' + ''.join(
   '<div class="frow"><span class="fn">%s</span><span class="fp">%s</span><span class="fs">%s</span></div>'
   % f for f in FILES) + '</div>'
 '<div class="strip" style="margin-top:52px">' + chip('%d pages in total'%N_TOTAL, '#fff')
 + chip('No account needed', '#fff') + '</div>'
 '</div></div>',
 '''.ftable{margin-top:56px;width:100%;background:#fff;border-radius:34px;overflow:hidden;
 box-shadow:0 26px 60px rgba(70,45,25,.16)}
.frow{display:flex;align-items:center;justify-content:space-between;padding:44px 52px;
 border-bottom:4px solid rgba(36,31,27,.07)}
.frow:last-child{border-bottom:none}
.fn{font-family:Fredoka,sans-serif;font-weight:600;font-size:52px}
.fp{font-weight:800;font-size:46px;color:#D0330F}
.fs{font-weight:700;font-size:46px;color:#6E645B}''')

os.makedirs('lhtml', exist_ok=True)
for k,v in IM.items(): open('lhtml/%s.html'%k,'w').write(v)
print('wrote', len(IM), 'listing pages')
