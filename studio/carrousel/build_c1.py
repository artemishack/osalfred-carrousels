import os, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/home/claude/carrousel"
OUT = f"{BASE}/out/c01-devis"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
NAVY = (11, 19, 43); BLUE = (0, 102, 255); GREY = (70, 80, 100); WHITE = (255, 255, 255)

def font(kind, size, weight):
    f = ImageFont.truetype(f"{BASE}/fonts/{kind}.ttf", size)
    try:
        axes = f.get_variation_axes()
        vals = [weight if a["name"] in (b"Weight", "Weight") else a.get("default", 14) for a in axes]
        if kind == "Inter":
            vals = [min(max(size / 2, 14), 32) if a["name"] in (b"Optical size", "Optical size") else weight for a in axes]
        f.set_variation_by_axes(vals)
    except Exception as e:
        print("var", e)
    return f

# ---------- décor : retrait du logo + recadrage 1080x1350
def decor():
    im = Image.open(f"{BASE}/assets/decor.png").convert("RGB")
    w, h = im.size
    im = im.crop((0, 0, w, int(h * 0.92)))  # retire la bande du logo
    r = max(W / im.size[0], H / im.size[1])
    im = im.resize((int(im.size[0] * r) + 1, int(im.size[1] * r) + 1), Image.LANCZOS)
    x = (im.size[0] - W) // 2
    return im.crop((x, im.size[1] - H, x + W, im.size[1]))

BG = decor()
POSE = {n: Image.open(f"{BASE}/assets/pose-{n}.png") for n in ("bras-croises", "telephone", "classeur")}

def wrap_rich(d, text, f, maxw):
    """text with *mot* for blue. returns lines of [(word, blue)]"""
    words = []
    for i, part in enumerate(text.split("*")):
        for wd in part.split():
            words.append((wd, i % 2 == 1))
    lines, cur = [], []
    for wd in words:
        trial = " ".join(w for w, _ in cur + [wd])
        if cur and d.textlength(trial, font=f) > maxw:
            lines.append(cur); cur = [wd]
        else:
            cur.append(wd)
    if cur: lines.append(cur)
    return lines

def draw_rich(d, xy, text, f, maxw, color=NAVY, accent=BLUE, lh=1.12, align="left"):
    x0, y = xy
    sp = d.textlength(" ", font=f)
    for line in wrap_rich(d, text, f, maxw):
        lw = sum(d.textlength(w, font=f) for w, _ in line) + sp * (len(line) - 1)
        x = x0 + (maxw - lw) / 2 if align == "center" else x0
        for w, b in line:
            d.text((x, y), w, font=f, fill=accent if b else color)
            x += d.textlength(w, font=f) + sp
        y += int(f.size * lh)
    return y

def base(n, total, dark=False):
    if dark:
        im = Image.new("RGB", (W, H), NAVY)
        g = BG.convert("L").point(lambda v: v * 0.18).convert("RGB")
        im = Image.blend(im, Image.merge("RGB", (g.split()[0],) * 3), 0.35)
    else:
        im = BG.copy()
        # voile clair en haut pour la lisibilité
        veil = Image.new("RGBA", (W, H), (255, 255, 255, 0))
        vd = ImageDraw.Draw(veil)
        for yy in range(H):
            a = int(140 * max(0, 1 - yy / (H * 0.62)))
            vd.line([(0, yy), (W, yy)], fill=(255, 255, 255, a))
        im = Image.alpha_composite(im.convert("RGBA"), veil).convert("RGB")
    d = ImageDraw.Draw(im)
    # pastille de numéro : mêmes coordonnées partout
    fp = font("Inter", 26, 700)
    lab = f"{n}/{total}"
    tw = d.textlength(lab, font=fp)
    d.rounded_rectangle((60, 54, 60 + tw + 44, 54 + 52), radius=26, fill=(BLUE if not dark else WHITE))
    d.text((60 + 22, 54 + 11), lab, font=fp, fill=(WHITE if not dark else NAVY))
    # signature
    fs = font("Inter", 26, 600)
    sig = "OsAlfred"
    d.text((W - 60 - d.textlength(sig, font=fs), 66), sig, font=fs, fill=(NAVY if not dark else WHITE))
    return im, d

def put_pose(im, name, x, bottom, height, flip=False, shadow=True):
    p = POSE[name]
    r = height / p.size[1]
    p = p.resize((int(p.size[0] * r), height), Image.LANCZOS)
    if flip: p = p.transpose(Image.FLIP_LEFT_RIGHT)
    if shadow:
        sh = Image.new("RGBA", (p.size[0] + 80, 60), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse((20, 10, sh.size[0] - 20, 50), fill=(20, 30, 60, 70))
        sh = sh.filter(ImageFilter.GaussianBlur(12))
        im.paste(sh, (x - 40, bottom - 30), sh)
    im.paste(p, (x, bottom - height), p)

def card(d, box, radius=28, fill=(255, 255, 255), outline=None):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=3 if outline else 0)

TOTAL = 7
slides = []

# 1 — HOOK
im, d = base(1, TOTAL)
fk = font("Inter", 30, 700)
d.text((80, 190), "ARTISANS DU 2ND ŒUVRE", font=fk, fill=BLUE)
y = draw_rich(d, (80, 245), "Les 3 messages qui *font signer* un devis déjà envoyé.", font("Montserrat", 92, 800), 900)
draw_rich(d, (80, y + 20), "Mot pour mot. À copier ce soir.", font("Inter", 38, 500), 700, color=GREY)
put_pose(im, "telephone", 610, 1310, 560)
slides.append(im)

# 2 — LE CONSTAT
im, d = base(2, TOTAL)
y = draw_rich(d, (80, 200), "Un devis sans relance ne meurt pas.", font("Montserrat", 74, 800), 940)
y = draw_rich(d, (80, y + 10), "*Il s'endort.*", font("Montserrat", 78, 800), 900)
draw_rich(d, (80, y + 40), "Le client n'a pas dit non. Il a oublié, il compare, ou il attend un déclic.", font("Inter", 40, 500), 560, color=GREY, lh=1.3)
put_pose(im, "bras-croises", 680, 1300, 620)
slides.append(im)

# 3 — J+3
im, d = base(3, TOTAL)
d.text((80, 190), "J+3", font=font("Montserrat", 120, 800), fill=BLUE)
draw_rich(d, (80, 330), "Le message court. SMS ou WhatsApp.", font("Montserrat", 64, 800), 900)
card(d, (80, 520, 1000, 900), fill=(255, 255, 255))
d.rounded_rectangle((120, 560, 960, 860), radius=34, fill=(0, 102, 255))
draw_rich(d, (160, 595), "« Bonjour [prénom], je reviens vers vous pour le devis [travaux] envoyé lundi. Vous avez pu le regarder ? Je reste dispo si une ligne n'est pas claire. »", font("Inter", 36, 500), 760, color=WHITE, accent=WHITE, lh=1.32)
draw_rich(d, (80, 950), "Court. Sans pression. *C'est celui qu'il lit vraiment.*", font("Inter", 38, 600), 520, color=NAVY, lh=1.3)
put_pose(im, "telephone", 700, 1320, 380, flip=True)
slides.append(im)

# 4 — J+7
im, d = base(4, TOTAL)
d.text((80, 190), "J+7", font=font("Montserrat", 120, 800), fill=BLUE)
draw_rich(d, (80, 330), "L'appel. Trois phrases, pas plus.", font("Montserrat", 64, 800), 620)
fi = font("Inter", 34, 500); fn = font("Montserrat", 40, 800)
rows = ["« Je vous appelle pour le devis [travaux], vous en êtes où ? »",
        "S'il hésite : « Qu'est-ce qui vous fait hésiter, le prix, le délai, ou autre chose ? »",
        "« Je bloque une date de démarrage, ou on se rappelle la semaine prochaine ? »"]
y = 520
for i, t in enumerate(rows, 1):
    card(d, (80, y, 700, y + 190), fill=(255, 255, 255))
    d.ellipse((105, y + 25, 165, y + 85), fill=NAVY)
    d.text((135 - d.textlength(str(i), font=fn) / 2, y + 30), str(i), font=fn, fill=WHITE)
    draw_rich(d, (190, y + 28), t, fi, 480, color=NAVY, lh=1.28)
    y += 215
put_pose(im, "telephone", 720, 1310, 600)
slides.append(im)

# 5 — J+15 (planche négative)
im, d = base(5, TOTAL, dark=True)
d.text((80, 190), "J+15", font=font("Montserrat", 120, 800), fill=(90, 160, 255))
draw_rich(d, (80, 330), "Le mail qui clôt. Souvent celui qui fait revenir le client.", font("Montserrat", 60, 800), 900, color=WHITE, accent=WHITE)
d.rounded_rectangle((80, 560, 1000, 900), radius=28, fill=(255, 255, 255))
draw_rich(d, (130, 610), "« Bonjour [prénom], sans nouvelles de votre part, je considère que le projet est en pause et je libère le créneau prévu. Si vous souhaitez le relancer, il suffit de répondre à ce mail. »", font("Inter", 36, 500), 820, color=NAVY, lh=1.36)
draw_rich(d, (80, 980), "Tu ne supplies pas. *Tu fermes la porte poliment.*", font("Inter", 40, 600), 900, color=WHITE, accent=(90, 160, 255), lh=1.3)
slides.append(im)

# 6 — QUAND LÂCHER
im, d = base(6, TOTAL)
y = draw_rich(d, (80, 200), "Après J+15, *tu passes au suivant.*", font("Montserrat", 80, 800), 900)
draw_rich(d, (80, y + 40), "Un client qu'on force à dire oui, c'est un chantier qui se passe mal.", font("Inter", 40, 500), 560, color=GREY, lh=1.3)
put_pose(im, "classeur", 700, 1300, 640)
slides.append(im)

# 7 — CTA
im, d = base(7, TOTAL)
y = draw_rich(d, (80, 200), "La méthode complète, *gratuite.*", font("Montserrat", 84, 800), 900)
fb = font("Inter", 40, 700)
lab = "Lien en bio"
tw = d.textlength(lab, font=fb)
d.rounded_rectangle((80, y + 40, 80 + tw + 90, y + 40 + 96), radius=48, fill=NAVY)
d.text((80 + 45, y + 40 + 24), lab, font=fb, fill=WHITE)
draw_rich(d, (80, y + 200), "Et toi, tu en signes combien sur 10 ? *Dis-le en commentaire.*", font("Inter", 42, 600), 560, color=NAVY, lh=1.3)
put_pose(im, "bras-croises", 680, 1300, 620)
slides.append(im)

for i, s in enumerate(slides, 1):
    s.save(f"{OUT}/planche-{i}.png")
# planche contact
th = [s.resize((360, 450), Image.LANCZOS) for s in slides]
sheet = Image.new("RGB", (360 * 4 + 50, 450 * 2 + 30), (240, 242, 246))
for i, t in enumerate(th):
    sheet.paste(t, (10 + (i % 4) * 370, 10 + (i // 4) * 460))
sheet.save(f"{OUT}/contact.png")
print("ok")
