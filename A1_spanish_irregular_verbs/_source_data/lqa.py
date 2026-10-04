import asyncio, glob, os
from playwright.async_api import async_playwright
B='/home/claude/a3/build'
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await br.new_page(viewport={'width':2000,'height':2000})
        os.makedirs(B+'/listing',exist_ok=True)
        for f in sorted(glob.glob(B+'/lhtml/*.html')):
            n=os.path.basename(f)[:-5]
            await pg.goto('file://'+f); await pg.wait_for_timeout(2000)
            r=await pg.evaluate("""()=>{
              const s=document.querySelector('.safe');
              let L=1e9,R=-1e9,T=1e9,Bm=-1e9,small=1e9,txt='';
              s.querySelectorAll('*').forEach(e=>{
                const r=e.getBoundingClientRect();
                if(r.width>=1&&r.height>=1){L=Math.min(L,r.left);R=Math.max(R,r.right);
                  T=Math.min(T,r.top);Bm=Math.max(Bm,r.bottom);}
                if([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())){
                  const fs=parseFloat(getComputedStyle(e).fontSize);
                  if(fs<small){small=fs;txt=e.textContent.trim().slice(0,24);}}
              });
              const h1=document.querySelector('.h1,.h2');
              return {L:Math.round(L),R:Math.round(R),T:Math.round(T),B:Math.round(Bm),
                      small:Math.round(small),txt,
                      title:h1?Math.round(parseFloat(getComputedStyle(h1).fontSize)):0,
                      fonts:[...new Set([...document.fonts].map(x=>x.family+':'+x.status))]};
            }""")
            await pg.screenshot(path='%s/listing/%s.png'%(B,n))
            fl=[]
            if r['L']<200 or r['R']>1800: fl.append('SAFE-ZONE')
            if r['T']<0 or r['B']>2000: fl.append('V-OVERFLOW')
            if r['small']<40: fl.append('TEXT<40px')
            floor = 260 if n=='01_hero' else 120
            if r['title']<floor: fl.append('TITLE<%dpx:%d'%(floor,r['title']))
            print('%-14s x[%4d..%4d] y[%4d..%4d] min=%3dpx title=%3dpx  %s'%(
                n,r['L'],r['R'],r['T'],r['B'],r['small'],r['title'],' '.join(fl) or 'OK'))
            if n=='01_hero': print('               fonts:',r['fonts'])
        await br.close()
asyncio.run(main())
