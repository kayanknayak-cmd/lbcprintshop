# -*- coding: utf-8 -*-
import json, os, re, sys, html
D = json.load(open('../data/verbs.json'))
FAM = D['families']
FKEY = {f['key']: i+1 for i,f in enumerate(FAM)}
VFAM = {v['verb']: f for f in FAM for v in f['verbs']}
BYVERB = {v['verb']: v for f in FAM for v in f['verbs']}
SIMPLE = [tuple(x) for x in D['simple']]
GLOSS = {'ser':'to be (permanent)','estar':'to be (state)','ir':'to go','haber':'to have (auxiliary)',
 'dar':'to give','ver':'to see','saber':'to know (facts)','tener':'to have','hacer':'to do, make',
 'poner':'to put','salir':'to leave','venir':'to come','decir':'to say','traer':'to bring',
 'oír':'to hear','conocer':'to know (people)','pensar':'to think','querer':'to want',
 'empezar':'to begin','sentir':'to feel','poder':'to be able','dormir':'to sleep','volver':'to return',
 'encontrar':'to find','pedir':'to ask for','seguir':'to follow','servir':'to serve',
 'jugar':'to play','comenzar':'to begin','perder':'to lose','entender':'to understand',
 'mostrar':'to show','recordar':'to remember','contar':'to count, tell','morir':'to die',
 'repetir':'to repeat','vestir':'to dress','caer':'to fall','valer':'to be worth',
 'conducir':'to drive','traducir':'to translate','construir':'to build','huir':'to flee',
 'elegir':'to choose','sonreír':'to smile'}

def fvars(key):
    n = FKEY[key]
    return '--bg:var(--f%dbg);--hd:var(--f%dhd);--ac:var(--f%dac)' % (n,n,n)

def cell(c):
    if not c['form']: return ''
    if not c['mark']: return html.escape(c['form'])
    a,b,d = c['mark']
    return '%s<span class="hl">%s</span>%s' % (html.escape(a), html.escape(b), html.escape(d))

SHORT = {'yo':'yo','tú':'tú','él/ella/Ud.':'él','nosotros':'nos.','vosotros':'vos.',
         'ellos/Uds.':'ellos','Ud.':'Ud.','Uds.':'Uds.'}

def block(verb, en, es, extra='', title=None, short=False):
    v = BYVERB[verb]; fam = VFAM[verb]
    rows = ''.join('<tr><th>%s</th><td>%s</td></tr>'
                   % (SHORT[c['person']] if short else c['person'], cell(c))
                   for c in v['tenses'][en])
    return ('<div class="blk" style="%s;%s"><div class="bh"><span class="bt">%s</span>'
            '<span class="be">%s</span></div><table>%s</table></div>'
            % (fvars(fam['key']), extra, title or en, es, rows))

def block_multi(en, es, verbs, famkey, extra=''):
    """One tense, several verbs of the same family side by side. Shows the pattern."""
    people = [c['person'] for c in BYVERB[verbs[0]]['tenses'][en]]
    rows = ''
    for i,p in enumerate(people):
        rows += '<tr><th>%s</th>%s</tr>' % (p, ''.join(
            '<td>%s</td>' % cell(BYVERB[v]['tenses'][en][i]) for v in verbs))
    head = ''.join('<td class="vh">%s</td>' % v for v in verbs)
    return ('<div class="blk" style="%s;%s"><div class="bh"><span class="bt">%s</span>'
            '<span class="be">%s</span></div>'
            '<table><tr class="vhr"><th></th>%s</tr>%s</table></div>'
            % (fvars(famkey), extra, en, es, head, rows))

# ---------------- page shells ----------------
SZ = {'letter':('8.5in','11in','.45in'), 'a4':('210mm','297mm','11mm')}

def scale(css, S):
    def f(m): return '%.4f%s' % (float(m.group(1))*S, m.group(2))
    head, sep, tail = css.partition('}')
    return head + sep + re.sub(r'([\d.]+)(pt|in)', f, tail)

def shell(inner, css, W, H, S=1.0):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="tokens.css">'
            '<style>@page{size:%s %s;margin:0}html,body{width:%s}%s</style></head><body>%s</body></html>'
            % (W,H,W, scale(css,S), inner))

PAGE_CSS = '''
.sheet{width:%(W)s;height:%(H)s;padding:%(P)s;display:flex;flex-direction:column}
.hd{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:.10in;
    border-bottom:3px solid rgba(36,31,27,.10);margin-bottom:.13in}
.hd h1{font-family:Fredoka,sans-serif;font-weight:600;font-size:27pt;line-height:1;letter-spacing:-.01em}
.hd .gl{font-family:Nunito,sans-serif;font-weight:700;font-size:11pt;color:var(--body);margin-top:.05in}
.hd .rt{text-align:right}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.082in}
.blk{--r:.12in;--h:12pt;--he:10pt;--f:11pt;--ps:11pt;--pw:.86in;
     --cp:.095in;--rp:.038in;--hp:.048in}
.blk .vhr td{font-family:Fredoka,sans-serif;font-weight:600;font-size:11pt;color:var(--ac);
     padding:.075in .115in .02in;text-align:left}
.blk .vhr th{padding:.075in .115in .02in}
.blk .vhr td,.blk .vhr th{border-top:none!important}
.pill{--gp:.05in;--pp:.045in .12in;--pf:10pt}
.ft{--ff:10pt;--fp:.07in;margin-top:auto}
.lb{padding:.11in .13in .13in}.lb p{font-weight:700;font-size:10.5pt;line-height:1.42;color:var(--body)}.lb p+p{margin-top:.07in}
.note{font-weight:700;font-size:10.5pt;color:var(--body);margin-top:.10in;line-height:1.45}
.note b{color:var(--ink)}
'''

def verb_page(verb, size, S=1.0, pageno=None, total=None):
    W,H,P = SZ[size]; fam = VFAM[verb]
    blocks = ''.join(block(verb, en, es) for en,es,_ in SIMPLE)
    note = BYVERB[verb].get('note')
    inner = ('<div class="sheet"><div class="hd"><div>'
      '<h1>%s</h1><div class="gl">%s</div></div>'
      '<div class="rt"><span class="pill" style="%s">%s</span>'
      '<div class="gl" style="margin-top:.07in">%s</div></div></div>'
      '<div class="grid">%s<div class="blk legend" style="--bg:#F7F3ED;--hd:#E9E1D6;--ac:#6E645B"><div class="bh"><span class="bt">How to use this page</span></div><div class="lb"><p><span class="hl">Highlighted</span> letters are where this verb stops following the regular pattern.</p><p>Blank practice grids at the back use this same layout, so you can fill one in from memory and check it here.</p></div></div></div>%s'
      '<div class="ft"><span>27 verbs conjugated in full &middot; 45 in the index</span>'
      '<span>%s</span></div></div>'
      % (verb, GLOSS.get(verb,''), fvars(fam['key']), fam['name'],
         'page %s of %s' % (pageno,total) if pageno else '',
         blocks,
         ('<div class="note"><b>Note.</b> %s</div>' % note) if note else '',
         'LBCPrintShop'))
    return shell(inner, PAGE_CSS % {'W':W,'H':H,'P':P}, W, H, S)

MAXCOL = 5   # more than five verbs across a page stops being readable, so it splits

def fam_parts(fam):
    vs = [v['verb'] for v in fam['verbs']]
    return [vs[i:i+MAXCOL] for i in range(0, len(vs), MAXCOL)]

def family_page(fam, size, S=1.0, pageno=None, total=None, part=1):
    W,H,P = SZ[size]
    parts = fam_parts(fam)
    vs = parts[part-1]
    blocks = (block_multi('Present','Presente',vs,fam['key'])
            + block_multi('Preterite','Pretérito',vs,fam['key'])
            + block_multi('Present Subj.','Presente subj.',vs,fam['key']))
    wide = len(vs) >= 5
    inner = ('<div class="sheet"><div class="hd"><div>'
      '<h1>%s</h1><div class="gl">%s</div></div>'
      '<div class="rt"><span class="pill" style="%s">the pattern</span>'
      '<div class="gl" style="margin-top:.07in">%s</div></div></div>'
      '<div class="grid fam">%s</div>'
      '<div class="ft"><span>Same tense, four verbs. The highlight shows the change.</span>'
      '<span>LBCPrintShop</span></div></div>'
      % (fam['name'], fam['blurb'], fvars(fam['key']),
         'page %s of %s' % (pageno,total) if pageno else '', blocks))
    css = PAGE_CSS % {'W':W,'H':H,'P':P}
    css += '.legend{display:none}.fam{grid-template-columns:1fr;gap:.14in}.fam .blk{--pw:1.20in;--f:12.5pt;--ps:11.5pt;--h:14pt;--he:10pt;--rp:.055in;--hp:.058in}'
    css += '.fam .blk .vhr td{font-size:%s;padding-top:.055in}' % ('12pt' if wide else '12.5pt')
    return shell(inner, css, W, H, S)

def overview_page(size, S=1.0, pageno=None, total=None):
    W,H,P = SZ[size]
    cards = ''
    for f in FAM:
        vs = ', '.join(v['verb'] for v in f['verbs'])
        ex = f['verbs'][0]['verb']
        exf = BYVERB[ex]['tenses']['Present'][0]
        cards += ('<div class="blk ov" style="%s"><div class="bh"><span class="bt">%s</span>'
                  '<span class="be">%d verbs</span></div>'
                  '<div class="ovb"><p class="ovd">%s</p>'
                  '<p class="ovv">%s</p>'
                  '<p class="ovx">%s &nbsp;&rarr;&nbsp; yo <b>%s</b></p></div></div>'
                  % (fvars(f['key']), f['name'], len(f['verbs']), f['blurb'], vs, ex, cell(exf)))
    inner = ('<div class="sheet"><div class="hd"><div>'
      '<h1>Five patterns</h1><div class="gl">Every irregular verb in this pack belongs to one of them.</div></div>'
      '<div class="rt"><span class="pill" style="%s">start here</span>'
      '<div class="gl" style="margin-top:.07in">%s</div></div></div>'
      '<div class="ovgrid">%s</div>'
      '<div class="ft"><span>27 verbs conjugated in full, 45 in the index.</span>'
      '<span>LBCPrintShop</span></div></div>'
      % (fvars('irregular'), 'page %s of %s'%(pageno,total) if pageno else '', cards))
    css = PAGE_CSS % {'W':W,'H':H,'P':P}
    css += ('.legend{display:none}.ovgrid{display:flex;flex-direction:column;gap:.16in}'
            '.ov{--r:.15in}.ovb{padding:.155in .17in .175in}'
            '.ovd{font-weight:700;font-size:12.5pt;line-height:1.4}'
            '.ovv{font-weight:800;font-size:12pt;color:var(--ac);margin-top:.085in}'
            '.ovx{font-weight:700;font-size:12.5pt;margin-top:.085in;color:var(--body)}'
            '.ovx b{color:var(--ink);font-size:15pt}')
    return shell(inner, css, W, H, S)

def index_page(size, S=1.0, pageno=None, total=None, part=1, nparts=2):
    W,H,P = SZ[size]
    RP = '.075in' if size=='a4' else '.063in'
    entries = D['index']
    per = -(-len(entries)//nparts)
    entries = entries[(part-1)*per: part*per]
    rows = ''
    for e in entries:
        fam = VFAM.get(e['verb'])
        st = fvars(fam['key']) if fam else '--bg:#F3EEE7;--hd:#E4DCD1;--ac:#6E645B'
        rows += ('<tr style="%s"><th>%s</th><td class="g">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                 % (st, e['verb'], GLOSS.get(e['verb'],''), e['yo'], e['pret_yo'], e['sub_yo']))
    inner = ('<div class="sheet"><div class="hd"><div>'
      '<h1>%d verbs</h1><div class="gl">The forms people get wrong, for every verb in the pack.</div></div>'
      '<div class="rt"><span class="pill" style="%s">quick reference</span>'
      '<div class="gl" style="margin-top:.07in">%s</div></div></div>'
      '<table class="idx"><tr class="ih"><th>verb</th><td>meaning</td><td>yo, present</td>'
      '<td>yo, preterite</td><td>yo, subjunctive</td></tr>%s</table>'
      '<div class="ft"><span>Colour shows which pattern the verb belongs to.</span>'
      '<span>LBCPrintShop</span></div></div>'
      % (len(D['index']), fvars('ei'), 'page %s of %s'%(pageno,total) if pageno else '', rows))
    css = PAGE_CSS % {'W':W,'H':H,'P':P}
    css += ('.legend{display:none}.idx{width:100%;border-collapse:separate;border-spacing:0 .028in}'
            '.idx th{text-align:left;font-family:Fredoka,sans-serif;font-weight:600;font-size:11.5pt;'
            'padding:'+RP+' .13in;background:var(--hd);border-radius:.1in 0 0 .1in;width:1.15in}'
            '.idx td{font-weight:700;font-size:11.5pt;padding:'+RP+' .10in;background:var(--bg)}'
            '.idx td:last-child{border-radius:0 .1in .1in 0}'
            '.idx .g{font-weight:600;color:var(--body);font-size:11pt}'
            '.idx .ih th,.idx .ih td{background:none!important;font-family:Nunito,sans-serif;'
            'font-weight:800;font-size:10pt;text-transform:uppercase;letter-spacing:.09em;'
            'color:var(--body);padding-bottom:.02in}')
    return shell(inner, css, W, H, S)

def practice_page(size, S=1.0):
    W,H,P = SZ[size]
    blocks = ''
    for en,es,_ in SIMPLE:
        people = ['yo','tú','él/ella/Ud.','nosotros','vosotros','ellos/Uds.']
        if 'Command' in en: people = ['tú','Ud.','nosotros','vosotros','Uds.']
        rows = ''.join('<tr><th>%s</th><td class="fill"></td></tr>'%p for p in people)
        blocks += ('<div class="blk" style="--bg:#F7F3ED;--hd:#E9E1D6;--ac:#6E645B">'
                   '<div class="bh"><span class="bt">%s</span><span class="be">%s</span></div>'
                   '<table>%s</table></div>' % (en, es, rows))
    inner = ('<div class="sheet"><div class="hd"><div>'
      '<h1>your verb: <span class="wr"></span></h1>'
      '<div class="gl">Fill it in from memory, then check it against the verb pages.</div></div>'
      '<div class="rt"><span class="pill" style="--bg:#F7F3ED;--hd:#FFD98A;--ac:#A85C00">practice</span></div></div>'
      '<div class="grid">%s</div>'
      '<div class="ft"><span>Print as many as you need.</span><span>LBCPrintShop</span></div></div>' % blocks)
    css = PAGE_CSS % {'W':W,'H':H,'P':P}
    css += '.legend{display:none}.fill{height:.152in}.wr{display:inline-block;width:2.7in;border-bottom:3px solid rgba(36,31,27,.28)}'
    return shell(inner, css, W, H, S)



POSTER_CSS = '''
.sheet{width:18in;height:24in;padding:.72in .62in .6in;display:flex;flex-direction:column}
.hd{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:.20in;
    border-bottom:6px solid rgba(36,31,27,.11);margin-bottom:.24in}
.hd h1{font-family:Fredoka,sans-serif;font-weight:600;font-size:76pt;line-height:.98;letter-spacing:-.015em}
.hd .gl{font-family:Nunito,sans-serif;font-weight:700;font-size:21pt;color:var(--body);margin-top:.10in}
.hd .rt{text-align:right}
.key{display:flex;gap:.16in;justify-content:flex-end;flex-wrap:wrap;margin-top:.13in}
.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:.115in}
.blk{--r:.17in;--h:20pt;--he:0pt;--f:20pt;--ps:20pt;--pw:.56in;
     --cp:.095in;--rp:.054in;--hp:.082in}
.blk .be{display:none}
.pill{--gp:.07in;--pp:.075in .20in;--pf:15pt}
.ft{--ff:15pt;--fp:.16in;margin-top:auto}
'''

def poster_page(S=1.0):
    blocks = ''
    for f in FAM:
        for v in f['verbs']:
            blocks += block(v['verb'], 'Present', '', title=v['verb'], short=True)
    keys = ''.join('<span class="pill" style="%s">%s</span>' % (fvars(f['key']), f['name']) for f in FAM)
    inner = ('<div class="sheet"><div class="hd"><div>'
      '<h1>Spanish<br>Irregular Verbs</h1>'
      '<div class="gl">27 verbs in the present tense, grouped by what makes them irregular.</div></div>'
      '<div class="rt"><div class="gl" style="font-size:24pt;color:var(--ink)">'
      '<b>45 verbs</b> in the full pack</div><div class="key">%s</div></div></div>'
      '<div class="grid">%s</div>'
      '<div class="ft"><span>Underlined letters are where the verb stops following the regular pattern.</span>'
      '<span>LBCPrintShop</span></div></div>' % (keys, blocks))
    return shell(inner, POSTER_CSS, '18in', '24in', S)

# ---------------- combine into one paginated document ----------------
def combine(parts, W, H):
    out_css, out_body = [], []
    for i,p in enumerate(parts):
        st = p.split('<style>',1)[1].split('</style>',1)[0]
        bd = p.split('<body>',1)[1].rsplit('</body>',1)[0]
        st = '\n'.join(('.pg%d %s'%(i,r)) if r.strip().startswith('.') else r for r in st.split('\n'))
        out_css.append(st); out_body.append('<div class="pg pg%d">%s</div>'%(i,bd))
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="tokens.css">'
            '<style>@page{size:%s %s;margin:0}html,body{width:%s}.pg{break-after:page}'
            '.pg:last-child{break-after:auto}%s</style></head><body>%s</body></html>'
            % (W,H,W,'\n'.join(out_css),''.join(out_body)))

if __name__ == '__main__':
    S = float(sys.argv[1]) if len(sys.argv)>1 else 1.0
    os.makedirs('html', exist_ok=True)
    order = []
    IDX_PARTS = 2
    n_fam = sum(len(fam_parts(f)) for f in FAM)
    n_pages = 1 + n_fam + sum(len(f['verbs']) for f in FAM) + IDX_PARTS
    for size in ('letter','a4'):
        parts, i = [], 1
        parts.append(overview_page(size,S,i,n_pages)); i+=1
        for f in FAM:
            for k in range(1, len(fam_parts(f))+1):
                parts.append(family_page(f,size,S,i,n_pages,k)); i+=1
            for v in f['verbs']:
                parts.append(verb_page(v['verb'],size,S,i,n_pages)); i+=1
        for k in range(1, IDX_PARTS+1):
            parts.append(index_page(size,S,i,n_pages,k,IDX_PARTS)); i+=1
        W,H,_ = SZ[size]
        open('html/set_%s.html'%size,'w').write(combine(parts,W,H))
        open('html/practice_%s.html'%size,'w').write(practice_page(size,S))
        # single pages for QA
        open('html/one_%s_verb.html'%size,'w').write(verb_page('pensar',size,S,9,n_pages))
        open('html/one_%s_fam.html'%size,'w').write(family_page(FAM[2],size,S,8,n_pages,1))
        open('html/one_%s_famwide.html'%size,'w').write(family_page(FAM[0],size,S,2,n_pages,1))
        open('html/one_%s_famyogo.html'%size,'w').write(family_page(FAM[1],size,S,10,n_pages,1))
        open('html/one_%s_ov.html'%size,'w').write(overview_page(size,S,1,n_pages))
        open('html/one_%s_idx.html'%size,'w').write(index_page(size,S,n_pages,n_pages,1,IDX_PARTS))
    open('html/poster.html','w').write(poster_page(1.0))
    print('pages per size:', n_pages, '+ 1 practice')
    print('scale', S)
