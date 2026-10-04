import asyncio, sys, glob, os
from playwright.async_api import async_playwright
B='/home/claude/a3/build'
FILES = sys.argv[1:] or ['one_letter_ov.html','one_letter_fam.html','one_letter_verb.html',
                         'one_letter_idx.html','practice_letter.html',
                         'one_a4_verb.html','one_a4_idx.html']
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await br.new_page()
        for f in FILES:
            w,h = (1400,1900) if 'poster' in f else ((850,1120) if 'a4' not in f else (830,1180))
            await pg.set_viewport_size({'width':w,'height':h})
            await pg.goto('file://%s/html/%s'%(B,f)); await pg.wait_for_timeout(1300)
            r=await pg.evaluate("""()=>{
              const s=document.querySelector('.sheet'), cs=getComputedStyle(s);
              const sr=s.getBoundingClientRect();
              const right=sr.right-parseFloat(cs.paddingRight);
              const bot=sr.bottom-parseFloat(cs.paddingBottom);
              const bad=[];
              s.querySelectorAll('.blk,.idx,tr').forEach(e=>{
                const r=e.getBoundingClientRect();
                if(r.width<1) return;
                if(r.right>right+1.5) bad.push(['X',(e.querySelector('.bt')||e).textContent.slice(0,18),Math.round(r.right),Math.round(right)]);
              });
              // fill must be measured from the last CONTENT element. The footer uses
              // margin-top:auto so it is always pinned to the bottom and reads ~96% even
              // on a half-empty page. That bug hid real whitespace.
              let cb=0;
              s.querySelectorAll('.grid > *, .ovgrid > *, .idx tr').forEach(e=>{
                const r=e.getBoundingClientRect(); if(r.height>2) cb=Math.max(cb,r.bottom);
              });
              const ft={bottom: cb || document.querySelector('.ft').getBoundingClientRect().bottom};
              let small=1e9,txt='',bodyMin=1e9,bodyTxt='';
              s.querySelectorAll('*').forEach(e=>{
                if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())) return;
                const fs=parseFloat(getComputedStyle(e).fontSize);
                if(fs<small){small=fs;txt=e.textContent.trim().slice(0,22);}
                if(e.matches('td') && !e.closest('.ih')){
                  if(fs<bodyMin){bodyMin=fs;bodyTxt=e.textContent.trim().slice(0,22);}
                }
              });
              const pxPerIn = 96;
              return {bad:bad.slice(0,6), fill:+(ft.bottom/sr.height*100).toFixed(1),
                      over:+(ft.bottom>bot+1), smallPt:+(small*72/pxPerIn).toFixed(1), txt,
                      bodyPt:+(bodyMin*72/pxPerIn).toFixed(1), bodyTxt,
                      fonts:[...new Set([...document.fonts].map(x=>x.family+':'+x.status))]};
            }""")
            flag=[]
            if r['bad']: flag.append('OVERFLOW-X')
            if r['over']: flag.append('OVERFLOW-Y')
            if r['smallPt']<10: flag.append('ANY-TEXT<10pt')
            floor = 20 if 'poster' in f else 11
            if r['bodyPt']<floor: flag.append('BODY<%dpt:%s'%(floor,r['bodyTxt']))
            if not (85<=r['fill']<=97.5): flag.append('FILL=%s'%r['fill'])
            print('%-24s fill=%5s%% any>=%4spt body>=%4spt  %s'%(f,r['fill'],r['smallPt'],r['bodyPt'],
                  ' '.join(flag) or 'OK'))
            for b in r['bad']: print('      ',b)
            if 'ov' in f: print('       fonts:', r['fonts'])
        await br.close()
asyncio.run(main())
