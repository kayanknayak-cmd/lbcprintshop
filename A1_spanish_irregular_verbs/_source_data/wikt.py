# -*- coding: utf-8 -*-
"""Second, independent source for Spanish conjugation: Wiktionary.

THE TRAP (found 4 Sep 2026): a Wiktionary page stacks many languages. Parsing the first
conjugation table on 'tener' returns tiengo/tiens/tien/tenez, which is ARAGONESE.
Everything here is scoped to the Spanish section before any table is touched."""
import urllib.request, urllib.parse, re, html, json, time, sys

UA = {'User-Agent': 'LBCPrintShop-conjugation-verify/1.0 (contact via etsy shop)'}

def fetch(title):
    u = 'https://en.wiktionary.org/api/rest_v1/page/html/' + urllib.parse.quote(title)
    for attempt in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode()
        except Exception as e:
            if attempt == 2: raise
            time.sleep(1.5)

def spanish_section(h):
    """Return only the Spanish language section. Raises if it cannot be isolated."""
    m = re.search(r'<h2[^>]*\bid="Spanish"[^>]*>', h)
    if not m:
        raise ValueError('no Spanish h2 on this page')
    start = m.start()
    nxt = re.search(r'<h2[^>]*\bid="[^"]+"', h[m.end():])
    end = m.end() + nxt.start() if nxt else len(h)
    seg = h[start:end]
    # sanity: the Spanish section must not contain another language's h2
    return seg

def conj_table(seg):
    i = seg.find('Conjugation of')
    if i < 0: raise ValueError('no conjugation table in the Spanish section')
    t0 = seg.find('<table', i)
    if t0 < 0: raise ValueError('no <table> after the conjugation heading')
    depth, k = 0, t0
    while k < len(seg):
        if seg.startswith('<table', k): depth += 1
        elif seg.startswith('</table>', k):
            depth -= 1
            if depth == 0: return seg[t0:k+8]
        k += 1
    raise ValueError('unbalanced table')

TAG = re.compile(r'<(?:[^>"\']|"[^"]*"|\'[^\']*\')*>')

def clean(c):
    c = TAG.sub(' ', c)          # attribute values can contain '>', so a naive <[^>]+> breaks
    c = html.unescape(c)
    return re.sub(r'\s+', ' ', c).strip()

def tu_form(cell):
    """Wiktionary packs the tuteo and voseo forms into one cell: 'tienes tú tenés vos'.
    Keep the tuteo form, drop footnote markers."""
    c = cell
    for marker in (' tú ', ' vos ', ' tú', ' vos'):
        if marker in c:
            c = c.split(marker)[0]
            break
    c = re.sub(r'\s*\d+\s*$', '', c).strip()
    return c.split()[0] if c.split() else c

def rows_of(tbl):
    out = []
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', tbl, re.S):
        cells = [clean(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)]
        if cells: out.append(cells)
    return out

# Wiktionary row label -> our tense key
LABEL = {
 'present': 'Present', 'imperfect': 'Imperfect', 'preterite': 'Preterite',
 'future': 'Future', 'conditional': 'Conditional',
}
SUBJ = {'present': 'Present Subjunctive', 'imperfect (ra)': 'Imperfect Subj. (-ra)',
        'imperfect (se)': 'Imperfect Subj. (-se)', 'future': 'Future Subjunctive'}

def parse(title):
    seg = spanish_section(fetch(title))
    rows = rows_of(conj_table(seg))
    # locate the indicative / subjunctive / imperative bands by their header rows
    band, out = None, {}
    for r in rows:
        first = r[0].lower().strip()
        if first.startswith('indicative'): band = 'ind'; continue
        if first.startswith('subjunctive'): band = 'sub'; continue
        if first.startswith('imperative'): band = 'imp'; continue
        if band == 'ind' and first in LABEL and len(r) >= 7:
            out[LABEL[first]] = [tu_form(x) for x in r[1:7]]
        elif band == 'sub' and first in SUBJ and len(r) >= 7:
            out[SUBJ[first]] = [tu_form(x) for x in r[1:7]]
    return out

if __name__ == '__main__':
    for v in sys.argv[1:] or ['tener','ser','ir','pensar','poder','pedir']:
        try:
            d = parse(v)
            print('==', v, '| tenses parsed:', len(d))
            for k in ['Present','Preterite','Present Subjunctive']:
                if k in d: print('   %-20s %s' % (k, d[k]))
        except Exception as e:
            print('==', v, 'FAILED:', e)
