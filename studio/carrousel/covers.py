import os, sys
from PIL import Image, ImageDraw, ImageOps, ImageFilter
sys.path.insert(0, '.')
import engine as E
from engine import font, draw_rich, text_h, POSE, W, H, wrap_rich, _wlen
from data import CAR

M = 130
NAVY=(11,19,43); BLUE=(0,102,255); LBLUE=(120,175,255); WHITE=(255,255,255); MIST=(233,238,245)

src = Image.open(f"{E.BASE}/assets/decor.png").convert("RGB")
src = src.crop((0,0,src.size[0],int(src.size[1]*0.92)))

def crop_decor(zoom, fx, fy):
    w,h = src.size
    r = max(W/w, H/h)*zoom
    im = src.resize((int(w*r)+1,int(h*r)+1), Image.LANCZOS)
    x = int((im.size[0]-W)*fx); y = int((im.size[1]-H)*fy)
    return im.crop((x,y,x+W,y+H))

def vgrad(top, bot, a0, a1):
    g = Image.new("RGBA",(W,H)); d=ImageDraw.Draw(g)
    for y in range(H):
        t=y/H; c=top
        d.line([(0,y),(W,y)], fill=(*c, int(a0+(a1-a0)*t)))
    return g

def bg(theme, i):
    z = [1.0,1.15,1.3][i%3]; fx=[0.5,0.2,0.8,0.35][i%4]
    base = crop_decor(z, fx, 1.0)
    g = base.convert("L")
    if theme=="snow":
        im = base.convert("RGBA"); im = Image.alpha_composite(im, vgrad(WHITE,WHITE,215,0))
    elif theme=="nuit":
        im = ImageOps.colorize(ImageOps.autocontrast(g), black=(6,10,26), white=(70,95,150)).convert("RGBA")
        im = Image.alpha_composite(im, vgrad(NAVY,NAVY,245,40))
    elif theme=="bleu":
        im = ImageOps.colorize(ImageOps.autocontrast(g), black=(0,50,160), white=(150,195,255)).convert("RGBA")
        im = Image.alpha_composite(im, vgrad(BLUE,BLUE,250,60))
    else:  # brume
        im = ImageOps.colorize(ImageOps.autocontrast(g), black=(95,110,140), white=(225,230,238)).convert("RGBA")
        im = Image.alpha_composite(im, vgrad((205,212,224),(205,212,224),250,70))
    return im.convert("RGB")

TH = {
 "snow": dict(fg=NAVY, acc=BLUE, hero=BLUE, pill=NAVY, pilltx=WHITE, sub=(70,80,100)),
 "nuit": dict(fg=WHITE, acc=LBLUE, hero=LBLUE, pill=WHITE, pilltx=NAVY, sub=(190,200,220)),
 "bleu": dict(fg=WHITE, acc=NAVY, hero=WHITE, pill=NAVY, pilltx=WHITE, sub=(225,235,255)),
 "brume":dict(fg=NAVY, acc=BLUE, hero=NAVY, pill=BLUE, pilltx=WHITE, sub=(70,80,100)),
}
ORDER = ["snow","nuit","bleu","brume"]

HERO = {1:"J+3",2:"100",3:"40 k€",4:"148 k€",7:"23h30",8:"J+45",10:"360 €",12:"30 %",13:"1,6 %",14:"4",
        16:"2 min",18:"-500 €",19:"110 m²",20:"5",21:"7h15",22:"3 vs 30",23:"35 %",24:"8 000 €",25:"40 km",
        26:"5 %",27:"500 €",28:"55 h",30:"21h"}

def fit(d, text, kind, weight, maxw, maxh, start, lh=1.12, minsize=34):
    sz = start
    while sz > minsize:
        f = font(kind, sz, weight)
        lines = wrap_rich(d, text, f, maxw)
        sp = d.textlength(" ", font=f)
        widest = max(sum(_wlen(d, w, f) for w in l) + sp*(len(l)-1) for l in lines)
        if len(lines)*int(sz*lh) <= maxh and widest <= maxw: return f
        sz -= 2
    return font(kind, minsize, weight)

def cover(i, kicker, title, pose):
    theme = ORDER[(i-1)%4]; t = TH[theme]
    im = bg(theme, i); d = ImageDraw.Draw(im)
    # top bar
    fk = font("Inter", 28, 700); lab = kicker.upper()
    tw = d.textlength(lab, font=fk)
    d.rounded_rectangle((M, 118, M+tw+48, 172), radius=27, fill=t["pill"])
    d.text((M+24, 130), lab, font=fk, fill=t["pilltx"])
    fs = font("Montserrat", 30, 800)
    d.text((W-M-d.textlength("OsAlfred", font=fs), 128), "OsAlfred", font=fs, fill=t["fg"])
    y = 230
    hero = HERO.get(i)
    if hero:
        fh = fit(d, hero, "Montserrat", 800, W-2*M, 230, 230, lh=1.0, minsize=120)
        d.text((M-6, y-20), hero, font=fh, fill=t["hero"])
        y += int(fh.size*1.0) + 10
        d.rectangle((M, y, M+90, y+10), fill=t["acc"] if theme!="bleu" else WHITE); y += 45
    maxh = 1350-560-y-20
    ft = fit(d, title, "Montserrat", 800, W-2*M, max(maxh, 200), 80 if hero else 96, lh=1.1, minsize=48)
    y = draw_rich(d, (M, y), title, ft, W-2*M, color=t["fg"], accent=t["acc"], lh=1.1)
    # character: alternate side
    right = i % 2 == 1
    ph = 540
    p = POSE[pose]; r = ph/p.size[1]; pw = int(p.size[0]*r)
    x = W-M-pw+40 if right else M-40
    E.put_pose(im, pose, x, 1335, ph, flip=not right)
    # swipe cue on the opposite side
    fsw = font("Inter", 30, 700); s = "Glisse  →"
    sw = d.textlength(s, font=fsw)
    sx = M if right else W-M-sw-50
    d.rounded_rectangle((sx, 1180, sx+sw+50, 1240), radius=30, outline=t["fg"], width=3)
    d.text((sx+25, 1192), s, font=fsw, fill=t["fg"])
    return im

def all_covers():
    out = {}
    out["c01-devis"] = (1, "Devis", "Les 3 messages qui *font signer* un devis déjà envoyé.", "telephone")
    for k, slug in enumerate([s for s in CAR if s != "c01-devis"], start=2):
        kw = CAR[slug][0][1]
        out[slug] = (k, kw["kicker"], kw["title"], kw["pose"])
    return out

if __name__ == "__main__":
    os.makedirs("out/covers", exist_ok=True)
    only = [int(a) for a in sys.argv[1:]]
    for slug,(i,k,t,p) in all_covers().items():
        if only and i not in only: continue
        cover(i,k,t,p).save(f"out/covers/{i:02d}-{slug}.png")
        print(i, slug)
