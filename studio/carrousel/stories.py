"""Stories 1080x1920 : 3 écrans par jour, même charte que les couvertures."""
import os, sys, re
from PIL import Image, ImageDraw, ImageOps
sys.path.insert(0, '.')
import engine as E
from engine import font, draw_rich, POSE, wrap_rich, _wlen
from data import CAR
import covers as C

W, H = 1080, 1920
M = 110
TOP, BOTTOM = 270, 1560          # zone sûre (hors barre IG en haut / champ réponse en bas)
NAVY, BLUE, WHITE = C.NAVY, C.BLUE, C.WHITE

src = C.src
def crop_decor(zoom, fx):
    w, h = src.size
    r = max(W / w, H / h) * zoom
    im = src.resize((int(w * r) + 1, int(h * r) + 1), Image.LANCZOS)
    x = int((im.size[0] - W) * fx); y = im.size[1] - H
    return im.crop((x, y, x + W, y + H))

def vgrad(c, a0, a1):
    g = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(g)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=(*c, int(a0 + (a1 - a0) * y / H)))
    return g

def bg(theme, i):
    base = crop_decor([1.0, 1.12, 1.25][i % 3], [0.5, 0.25, 0.75, 0.4][i % 4]); g = base.convert("L")
    if theme == "snow":
        im = Image.alpha_composite(base.convert("RGBA"), vgrad(WHITE, 225, 10))
    elif theme == "nuit":
        im = ImageOps.colorize(ImageOps.autocontrast(g), black=(6, 10, 26), white=(70, 95, 150)).convert("RGBA")
        im = Image.alpha_composite(im, vgrad(NAVY, 245, 50))
    elif theme == "bleu":
        im = ImageOps.colorize(ImageOps.autocontrast(g), black=(0, 50, 160), white=(150, 195, 255)).convert("RGBA")
        im = Image.alpha_composite(im, vgrad(BLUE, 250, 70))
    else:
        im = ImageOps.colorize(ImageOps.autocontrast(g), black=(95, 110, 140), white=(225, 230, 238)).convert("RGBA")
        im = Image.alpha_composite(im, vgrad((205, 212, 224), 250, 80))
    return im.convert("RGB")

def fit(d, text, kind, weight, maxw, maxh, start, lh=1.1, minsize=40):
    s = start
    while s > minsize:
        f = font(kind, s, weight)
        lines = wrap_rich(d, text, f, maxw); sp = d.textlength(" ", font=f)
        widest = max(sum(_wlen(d, w, f) for w in l) + sp * (len(l) - 1) for l in lines)
        if len(lines) * int(s * lh) <= maxh and widest <= maxw: return f
        s -= 2
    return font(kind, minsize, weight)

def header(d, t, label):
    fk = font("Inter", 30, 700); lab = label.upper(); tw = d.textlength(lab, font=fk)
    d.rounded_rectangle((M, TOP, M + tw + 52, TOP + 58), radius=29, fill=t["pill"])
    d.text((M + 26, TOP + 13), lab, font=fk, fill=t["pilltx"])
    fs = font("Montserrat", 32, 800)
    d.text((W - M - d.textlength("OsAlfred", font=fs), TOP + 10), "OsAlfred", font=fs, fill=t["fg"])

def pill(d, x, y, text, fg, bgc, size=34):
    f = font("Inter", size, 700); tw = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + tw + 64, y + size + 42), radius=(size + 42) // 2, fill=bgc)
    d.text((x + 32, y + 19), text, font=f, fill=fg)
    return y + size + 42

def theme_for(i, shift=0):
    name = C.ORDER[(i - 1 + shift) % 4]
    return name, C.TH[name]

# --- écran 1 : le sujet du jour
def s1(i, kicker, title, pose):
    name, t = theme_for(i); im = bg(name, i); d = ImageDraw.Draw(im)
    header(d, t, kicker)
    y = TOP + 150
    d.text((M, y), "LE POST DU JOUR", font=font("Inter", 30, 700), fill=t["acc"] if name != "bleu" else WHITE)
    y += 70
    hero = C.HERO.get(i)
    if hero:
        fh = fit(d, hero, "Montserrat", 800, W - 2 * M, 260, 260, lh=1.0, minsize=140)
        d.text((M - 6, y - 24), hero, font=fh, fill=t["hero"]); y += int(fh.size) + 30
    ft = fit(d, title, "Montserrat", 800, W - 2 * M, 400, 88, minsize=54)
    y = draw_rich(d, (M, y), title, ft, W - 2 * M, color=t["fg"], accent=t["acc"], lh=1.1)
    y = pill(d, M, y + 50, "Le carrousel est sur le profil  →", WHITE if name != "nuit" else NAVY, NAVY if name != "nuit" else WHITE)
    p = POSE[pose]; ph = 560; pw = int(p.size[0] * ph / p.size[1])
    E.put_pose(im, pose, W - M - pw + 30, H - 60, ph)
    return im

# --- écran 2 : la question
def s2(i, question):
    name, t = theme_for(i, 1); im = bg(name, i + 7); d = ImageDraw.Draw(im)
    header(d, t, "Ta réponse")
    q = re.sub(r"\s*\*?Dis-le en commentaire\.\*?", "", question).strip()
    ft = fit(d, q, "Montserrat", 800, W - 2 * M, 640, 104, minsize=60)
    lines = len(wrap_rich(d, q, ft, W - 2 * M)) * int(ft.size * 1.1)
    y = (TOP + BOTTOM) // 2 - lines // 2 - 120
    y = draw_rich(d, (M, y), q, ft, W - 2 * M, color=t["fg"], accent=t["acc"], lh=1.1)
    sub = t["sub"]
    y = draw_rich(d, (M, y + 50), "Réponds à cette story. *Je lis tout,* et les meilleures réponses feront un prochain post.",
                  font("Inter", 40, 600), W - 2 * M, color=sub, accent=t["acc"] if name != "bleu" else WHITE, lh=1.35)
    d.rounded_rectangle((M, BOTTOM - 150, W - M, BOTTOM - 40), radius=55, outline=t["fg"], width=4)
    fr = font("Inter", 36, 600); s = "Ta réponse ici  ↓"
    d.text(((W - d.textlength(s, font=fr)) // 2, BOTTOM - 117), s, font=fr, fill=t["fg"])
    return im

# --- écran 3 : le kit (ou le diagnostic un jour sur 7)
KIT = Image.open(f"{E.BASE}/../alfred-landing/site/assets/img/kit-couverture-800.jpg").convert("RGB")
def s3(i, diag=False):
    name, t = theme_for(i, 2); im = bg(name, i + 3); d = ImageDraw.Draw(im)
    header(d, t, "Diagnostic offert" if diag else "Kit gratuit")
    y = TOP + 150
    if diag:
        title = "Et si tes relances partaient *toutes seules ?*"
        body = "30 minutes au téléphone pour voir où partent ton temps et ton argent. Feuille de route sous 48h. Gratuit, sans engagement."
        cta1, cta2 = "Réponds « DIAG »", "osalfred.com/rendez-vous"
    else:
        title = "Les messages mot pour mot sont *dans le kit.*"
        body = "Relances de devis, acompte, relance de facture, retenue de garantie. 11 pages, gratuit."
        cta1, cta2 = "Réponds « KIT »", "ou osalfred.com/kit"
    ft = fit(d, title, "Montserrat", 800, W - 2 * M, 330, 96, minsize=60)
    y = draw_rich(d, (M, y), title, ft, W - 2 * M, color=t["fg"], accent=t["acc"], lh=1.1)
    y = draw_rich(d, (M, y + 34), body, font("Inter", 40, 500), W - 2 * M, color=t["sub"], lh=1.35)
    if not diag:
        kw = 420; k = KIT.resize((kw, int(KIT.size[1] * kw / KIT.size[0])), Image.LANCZOS).rotate(4, expand=True, fillcolor=(0, 0, 0))
        mask = Image.new("L", KIT.resize((kw, int(KIT.size[1] * kw / KIT.size[0]))).size, 255).rotate(4, expand=True)
        sh = Image.new("RGBA", (k.size[0] + 80, k.size[1] + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((40, 60, k.size[0] + 40, k.size[1] + 40), radius=20, fill=(11, 19, 43, 90))
        from PIL import ImageFilter
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        kx, ky = (W - k.size[0]) // 2, y + 60
        im.paste(sh, (kx - 40, ky - 30), sh); im.paste(k, (kx, ky), mask)
        y = ky + k.size[1] + 40
    else:
        p = POSE["telephone"]; ph = 600; pw = int(p.size[0] * ph / p.size[1])
        E.put_pose(im, "telephone", (W - pw) // 2, y + 60 + ph, ph); y = y + 60 + ph + 40
    y = max(y, BOTTOM - 230)
    on_dark = name in ("nuit", "bleu")
    y2 = pill(d, M, y, cta1, NAVY if on_dark else WHITE, WHITE if on_dark else BLUE, size=40)
    d.text((M + 8, y2 + 22), cta2, font=font("Inter", 34, 600), fill=t["fg"])
    return im

def all_days():
    days = []
    for k, (slug, slides) in enumerate(CAR.items(), start=1):
        kw = slides[0][1]; q = [s for s in slides if s[0].__name__ == "s_cta"][0][1]["question"]
        days.append((k, slug, kw["kicker"], kw["title"], kw["pose"], q))
    return days

if __name__ == "__main__":
    only = [int(a) for a in sys.argv[1:]]
    for k, slug, kicker, title, pose, q in all_days():
        if only and k not in only: continue
        out = f"out/stories/{k:02d}-{slug}"; os.makedirs(out, exist_ok=True)
        s1(k, kicker, title, pose).save(f"{out}/1.jpg", quality=90)
        s2(k, q).save(f"{out}/2.jpg", quality=90)
        s3(k, diag=(k % 7 == 0)).save(f"{out}/3.jpg", quality=90)
        print(k, slug, flush=True)
