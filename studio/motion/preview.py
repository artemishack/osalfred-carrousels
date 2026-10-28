import json, sys, re
sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from render import tok, timeline
from reels2 import REELS2
key=sys.argv[1]; times=[float(x) for x in sys.argv[2:]]
r=REELS2[key]
try: words=json.load(open(f'audio/{key}.json'))['words']
except Exception:
    allw=[w for s in r['scenes'] for w in tok(s['say'])]; words=[dict(text=w,start=i*0.36,end=i*0.36+0.3) for i,w in enumerate(allw)]
r=timeline(r,words); r['dur']=words[-1]['end']+1.6
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/motion/engine.html'); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready')
    pg.evaluate('c=>build(c)', r)
    for t in times:
        pg.evaluate(f'render({t})'); pg.screenshot(path=f'prev_{t}.jpg',type='jpeg',quality=80)
    b.close()
from PIL import Image
ims=[Image.open(f'prev_{t}.jpg').resize((270,480)) for t in times]
s=Image.new('RGB',(len(ims)*276,480),'white')
for k,i in enumerate(ims): s.paste(i,(k*276,0))
s.save('prev.jpg')
print([ (round(sc['t0'],2)) for sc in r['scenes']])
