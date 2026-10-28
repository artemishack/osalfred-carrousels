import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/home/claude/carrousel"
W, H = 1080, 1350
NAVY = (11, 19, 43); BLUE = (0, 102, 255); GREY = (70, 80, 100); WHITE = (255, 255, 255)
LBLUE = (90, 160, 255)

_fc = {}
def font(kind, size, weight):
    k = (kind, size, weight)
    if k in _fc: return _fc[k]
    f = ImageFont.truetype(f"{BASE}/fonts/{kind}.ttf", size)
    axes = f.get_variation_axes()
    vals = []
    for a in axes:
        n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
        vals.append(min(max(size / 2, 14), 32) if "ptical" in n else weight)
    f.set_variation_by_axes(vals)
    _fc[k] = f
    return f

def decor():
    im = Image.open(f"{BASE}/assets/decor.png").convert("RGB")
    w, h = im.size
    im = im.crop((0, 0, w, int(h * 0.92)))
    r = max(W / im.size[0], H / im.size[1])
    im = im.resize((int(im.size[0] * r) + 1, int(im.size[1] * r) + 1), Image.LANCZOS)
    x = (im.size[0] - W) // 2
    return im.crop((x, im.size[1] - H, x + W, im.size[1]))

BG = decor()
VEIL = Image.new("RGBA", (W, H), (255, 255, 255, 0))
_vd = ImageDraw.Draw(VEIL)
for yy in range(H):
    _vd.line([(0, yy), (W, yy)], fill=(255, 255, 255, int(140 * max(0, 1 - yy / (H * 0.62)))))
LIGHT = Image.alpha_composite(BG.convert("RGBA"), VEIL).convert("RGB")
_g = BG.convert("L").point(lambda v: v * 0.18).convert("RGB")
DARK = Image.blend(Image.new("RGB", (W, H), NAVY), _g, 0.35)
POSE = {n: Image.open(f"{BASE}/assets/pose-{n}.png") for n in ("bras-croises", "telephone", "classeur")}

import re
_AFTER = {":", ";", "?", "!", "»", "%", "€", "k€", "€.", "%.", "€,", "k€.", "km", "h", "€/h", "%,", "?»", "jours", "jours.", "ans", "salariés"}
def _tokens(text):
    toks = []
    for i, part in enumerate(text.split("*")):
        for wd in part.split(" "):
            if wd: toks.append([(wd, i % 2 == 1)])
    out = []
    for t in toks:
        w = t[0][0]
        if out:
            prev = "".join(x for x, _ in out[-1])
            glue = (w in _AFTER or w[0] in ":;?!»") or prev == "«" \
                or (re.search(r"\d$", prev) and (re.match(r"^\d{3}\b", w) or w.rstrip(".,") in {"€", "k€", "%", "km", "h", "jours", "ans", "m²", "salariés", "lignes", "fois"}))
            if glue:
                out[-1] = out[-1] + [(" " + w, t[0][1])]
                continue
        out.append(t)
    return out

def _wlen(d, w, f): return sum(d.textlength(x, font=f) for x, _ in w)

def wrap_rich(d, text, f, maxw):
    words = _tokens(text)
    sp = d.textlength(" ", font=f)
    lines, cur, cw = [], [], 0
    for wd in words:
        l = _wlen(d, wd, f)
        if cur and cw + sp + l > maxw:
            lines.append(cur); cur, cw = [wd], l
        else:
            cw = cw + sp + l if cur else l; cur.append(wd)
    if cur: lines.append(cur)
    if len(lines) > 1 and len(lines[-1]) == 1 and len(lines[-2]) > 2:
        lines[-1].insert(0, lines[-2].pop())
    return lines

def text_h(d, text, f, maxw, lh):
    return len(wrap_rich(d, text, f, maxw)) * int(f.size * lh)

def draw_rich(d, xy, text, f, maxw, color=NAVY, accent=BLUE, lh=1.12, dry=False):
    x0, y = xy
    sp = d.textlength(" ", font=f)
    for line in wrap_rich(d, text, f, maxw):
        x = x0
        for wd in line:
            for seg, b in wd:
                if not dry: d.text((x, y), seg, font=f, fill=accent if b else color)
                x += d.textlength(seg, font=f)
            x += sp
        y += int(f.size * lh)
    return y

def fit(d, text, kind, weight, maxw, maxh, start, lh=1.12, minsize=34):
    s = start
    while s > minsize:
        f = font(kind, s, weight)
        if text_h(d, text, f, maxw, lh) <= maxh: return f
        s -= 2
    return font(kind, minsize, weight)

def frame(n, total, dark=False):
    im = (DARK if dark else LIGHT).copy()
    d = ImageDraw.Draw(im)
    fp = font("Inter", 26, 700)
    lab = f"{n}/{total}"
    tw = d.textlength(lab, font=fp)
    d.rounded_rectangle((L - 10, 64, L - 10 + tw + 44, 116), radius=26, fill=(WHITE if dark else BLUE))
    d.text((L + 12, 75), lab, font=fp, fill=(NAVY if dark else WHITE))
    fs = font("Inter", 26, 600)
    d.text((R - d.textlength("OsAlfred", font=fs), 76), "OsAlfred", font=fs, fill=(WHITE if dark else NAVY))
    return im, d

def put_pose(im, name, x, bottom, height, flip=False):
    p = POSE[name]
    r = height / p.size[1]
    p = p.resize((int(p.size[0] * r), height), Image.LANCZOS)
    if flip: p = p.transpose(Image.FLIP_LEFT_RIGHT)
    sh = Image.new("RGBA", (p.size[0] + 80, 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((20, 10, sh.size[0] - 20, 50), fill=(20, 30, 60, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    im.paste(sh, (x - 40, bottom - 30), sh)
    im.paste(p, (x, bottom - height), p)

# ---------------- types de planches
L = 125            # marge gauche/droite (zone sûre recadrage 3:4)
R = W - L
TW = R - L         # largeur texte pleine
def s_hook(n, t, kicker, title, sub, pose="telephone"):
    im, d = frame(n, t)
    d.text((L, 190), kicker.upper(), font=font("Inter", 30, 700), fill=BLUE)
    f = fit(d, title, "Montserrat", 800, TW, 430, 88)
    y = draw_rich(d, (L, 245), title, f, TW)
    if sub: y = draw_rich(d, (L, y + 18), sub, font("Inter", 38, 500), 520, color=GREY, lh=1.25)
    h = min(600, 1310 - y - 30)
    put_pose(im, pose, 620 if pose != "classeur" else 660, 1310, max(h, 460))
    return im

def s_statement(n, t, title, sub, pose="bras-croises"):
    im, d = frame(n, t)
    f = fit(d, title, "Montserrat", 800, TW, 420, 76)
    y = draw_rich(d, (L, 200), title, f, TW)
    if sub: y = draw_rich(d, (L, y + 36), sub, font("Inter", 40, 500), 500, color=GREY, lh=1.3)
    if pose: put_pose(im, pose, 640 if pose != "classeur" else 680, 1300, 600)
    return im

def s_step(n, t, label, title, card, note="", pose=None, card_blue=True):
    im, d = frame(n, t)
    d.text((L, 190), label, font=font("Montserrat", 104, 800), fill=BLUE)
    ft = fit(d, title, "Montserrat", 800, TW, 150, 60)
    y = draw_rich(d, (L, 330), title, ft, TW)
    fc = font("Inter", 35, 500)
    cw = TW - 160
    ch = text_h(d, card, fc, cw, 1.34)
    top = max(y + 40, 500)
    d.rounded_rectangle((L, top, R, top + ch + 120), radius=30, fill=WHITE)
    d.rounded_rectangle((L + 30, top + 30, R - 30, top + ch + 90), radius=26, fill=(BLUE if card_blue else (238, 243, 251)))
    draw_rich(d, (L + 80, top + 60), card, fc, cw, color=(WHITE if card_blue else NAVY), accent=(WHITE if card_blue else BLUE), lh=1.34)
    y = top + ch + 160
    if note: draw_rich(d, (L, y), note, font("Inter", 37, 600), 500 if pose else TW, lh=1.3)
    if pose and y < 1050: put_pose(im, pose, 700, 1320, min(420, 1320 - y + 60), flip=True)
    return im

def s_list(n, t, title, items, pose="telephone", label=None):
    im, d = frame(n, t)
    y = 190
    if label:
        d.text((L, 190), label, font=font("Montserrat", 104, 800), fill=BLUE); y = 330
    tw = TW if not pose else 580
    ft = fit(d, title, "Montserrat", 800, tw, 170, 60)
    y = draw_rich(d, (L, y), title, ft, tw) + 30
    fi = font("Inter", 33, 500); fn = font("Montserrat", 40, 800)
    cw = 580 if pose else TW
    for i, it in enumerate(items, 1):
        h = max(110, text_h(d, it, fi, cw - 150, 1.28) + 56)
        d.rounded_rectangle((L, y, L + cw, y + h), radius=26, fill=WHITE)
        d.ellipse((L + 25, y + 25, L + 85, y + 85), fill=NAVY)
        d.text((L + 55 - d.textlength(str(i), font=fn) / 2, y + 30), str(i), font=fn, fill=WHITE)
        draw_rich(d, (L + 110, y + 28), it, fi, cw - 150, lh=1.28)
        y += h + 22
    if pose: put_pose(im, pose, 720, 1310, 600)
    return im

def s_dark(n, t, label, title, card, note=""):
    im, d = frame(n, t, dark=True)
    def lay(y0, dry):
        y = y0
        if label:
            if not dry: d.text((L, y), label, font=font("Montserrat", 104, 800), fill=LBLUE)
            y += 140
        ft = fit(d, title, "Montserrat", 800, TW, 300, 70)
        y = draw_rich(d, (L, y), title, ft, TW, color=WHITE, accent=LBLUE, dry=dry) + 40
        if card:
            fc = font("Inter", 35, 500)
            ch = text_h(d, card, fc, TW - 100, 1.36)
            if not dry:
                d.rounded_rectangle((L, y, R, y + ch + 100), radius=28, fill=WHITE)
                draw_rich(d, (L + 50, y + 50), card, fc, TW - 100, lh=1.36)
            y += ch + 160
        if note: y = draw_rich(d, (L, y), note, font("Inter", 41, 600), TW, color=WHITE, accent=LBLUE, lh=1.3, dry=dry)
        return y
    h = lay(0, True)
    lay(max(190, (H - h) // 2 - 20), False)
    return im

def s_cta(n, t, question):
    im, d = frame(n, t)
    y = draw_rich(d, (L, 200), "Ma méthode pour faire signer tes devis : *gratuite.*", font("Montserrat", 72, 800), TW)
    fb = font("Inter", 40, 700)
    tw = d.textlength("Lien en bio", font=fb)
    d.rounded_rectangle((L, y + 40, L + tw + 90, y + 136), radius=48, fill=NAVY)
    d.text((L + 45, y + 64), "Lien en bio", font=fb, fill=WHITE)
    draw_rich(d, (L, y + 200), question, font("Inter", 42, 600), 520, lh=1.3)
    put_pose(im, "bras-croises", 680, 1300, 600)
    return im

def build(slug, slides):
    out = f"{BASE}/out/{slug}"
    os.makedirs(out, exist_ok=True)
    t = len(slides)
    ims = []
    for i, (fn, kw) in enumerate(slides, 1):
        ims.append(fn(i, t, **kw))
    for i, im in enumerate(ims, 1):
        im.save(f"{out}/planche-{i}.png", optimize=True)
    th = [s.resize((300, 375), Image.LANCZOS) for s in ims]
    cols = 4
    rows = (len(th) + cols - 1) // cols
    sheet = Image.new("RGB", (310 * cols + 10, 385 * rows + 10), (240, 242, 246))
    for i, tt in enumerate(th):
        sheet.paste(tt, (10 + (i % cols) * 310, 10 + (i // cols) * 385))
    sheet.save(f"{out}/contact.png")
    return out
