"""Montage des reels 1080x1920 : fond charte animé, titre par séquence, sous-titres mot à mot, carte CTA."""
import os, sys, json, re, subprocess
from PIL import Image, ImageDraw
sys.path.insert(0, '.')
import engine as E
from engine import font, draw_rich, POSE, wrap_rich, _wlen
import covers as C
import stories as S
from reels_data import REELS, CTA

W, H, FPS = 1080, 1920, 30
M = 96
NAVY, BLUE, WHITE = C.NAVY, C.BLUE, C.WHITE
OUT = f"{E.BASE}/reels"
ORDER = C.ORDER
KIT = S.KIT
LOGO_INK = Image.open(f"{E.BASE}/../alfred-landing/site/assets/brand/logo-email-ink-v1.png").convert("RGBA")

def clean(t):
    return re.sub(r"\[[^\]]*\]\s*", "", t).replace("O.S.", "OS").strip()

def ntok(t):
    return len([x for x in clean(t).split() if not re.fullmatch(r"[?:!.,…]+", x)])

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ---------- calques statiques par séquence
def big_bg(theme, i):
    b = S.bg(theme, i)
    return b.resize((int(W * 1.08), int(H * 1.08)), Image.LANCZOS)

def headline_layer(theme, text, pose=None, hero_y=360):
    t = C.TH[theme]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    paras = text.split("\n")
    maxw = W - 2 * M
    size = 140
    while size > 64:
        f = font("Montserrat", size, 800)
        hgt = sum(len(wrap_rich(d, p, f, maxw)) for p in paras) * int(size * 1.08)
        widest = max(max(sum(_wlen(d, w, f) for w in l) + d.textlength(" ", font=f) * (len(l) - 1)
                         for l in wrap_rich(d, p, f, maxw)) for p in paras)
        if hgt <= 640 and widest <= maxw: break
        size -= 4
    y = 360 + max(0, (700 - hgt) // 2)
    for p in paras:
        y = draw_rich(d, (M, y), p, f, maxw, color=t["fg"], accent=t["acc"], lh=1.08)
        y += int(size * 0.15)
    if pose:
        p = POSE[pose]; ph = 470
        E.put_pose(lay, pose, W - M - int(p.size[0] * ph / p.size[1]) + 40, H - 40, ph)
    return lay, y

def chrome(d, theme, prog):
    t = C.TH[theme]
    fs = font("Montserrat", 34, 800)
    d.text((M, 236), "OS Alfred", font=fs, fill=t["fg"])
    d.rounded_rectangle((M, 296, W - M, 302), radius=3, fill=(*t["fg"][:3],) if False else (255, 255, 255) if theme in ("nuit", "bleu") else (11, 19, 43))
    d.rounded_rectangle((M, 296, M + int((W - 2 * M) * prog), 302), radius=3, fill=t["acc"] if theme != "bleu" else WHITE)

# ---------- sous-titres
def chunks(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 3 or re.search(r"[.?!…:,]$", w["text"]):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

def disp(t):
    t = t.replace("O.S.", "OS")
    return re.sub(r"[.,:;…]+$", "", t) if not t.endswith("?") else t

def draw_caption(d, theme, ch, now, y=1240):
    dark = theme in ("nuit", "bleu")
    f = font("Inter", 84, 800)
    words = [disp(w["text"]) for w in ch]
    sp = d.textlength(" ", font=f) + 22
    widths = [d.textlength(w, font=f) for w in words]
    total = sum(widths) + sp * (len(words) - 1)
    if total > W - 2 * M:
        f = font("Inter", int(84 * (W - 2 * M) / total), 800)
        widths = [d.textlength(w, font=f) for w in words]; sp = d.textlength(" ", font=f) + 22
        total = sum(widths) + sp * (len(words) - 1)
    x = (W - total) / 2
    for w, wd, wo in zip(words, widths, ch):
        active = wo["start"] <= now < max(wo["end"], wo["start"] + 0.12) + 0.08
        if active:
            d.rounded_rectangle((x - 14, y - 6, x + wd + 14, y + f.size + 18), radius=16,
                                fill=WHITE if theme == "bleu" else BLUE)
            col = BLUE if theme == "bleu" else WHITE
        else:
            col = WHITE if dark else NAVY
        d.text((x, y), w, font=f, fill=col)
        x += wd + sp

# ---------- carte CTA
def cta_layer(kind, theme="bleu"):
    t = C.TH[theme]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    word = "KIT" if kind == "kit" else "DIAG"
    f = font("Montserrat", 112, 800)
    y = draw_rich(d, (M, 360), f"Écris *« {word} »*", f, W - 2 * M, color=t["fg"], accent=t["acc"], lh=1.06)
    y = draw_rich(d, (M, y), "en commentaire", font("Montserrat", 80, 800), W - 2 * M, color=t["fg"], accent=t["acc"], lh=1.06)
    sub = ("Relances de devis, acompte, factures. Les messages mot pour mot. Gratuit." if kind == "kit"
           else "Audit gratuit de 30 min. Feuille de route sous 48h. Sans engagement.")
    y = draw_rich(d, (M, y + 30), sub, font("Inter", 44, 600), W - 2 * M, color=t["sub"], lh=1.35)
    if kind == "kit":
        kw = 420; k = KIT.resize((kw, int(KIT.size[1] * kw / KIT.size[0])), Image.LANCZOS).convert("RGBA").rotate(4, expand=True)
        lay.alpha_composite(k, ((W - k.size[0]) // 2, y + 60)); url = "osalfred.com/kit"
    else:
        p = POSE["telephone"]; ph = 560
        E.put_pose(lay, "telephone", (W - int(p.size[0] * ph / p.size[1])) // 2, y + 80 + ph, ph); url = "osalfred.com/rendez-vous"
    fu = font("Inter", 40, 700); tw = d.textlength(url, font=fu)
    d.rounded_rectangle(((W - tw) // 2 - 36, 1500, (W + tw) // 2 + 36, 1580), radius=40, fill=WHITE if theme in ("nuit", "bleu") else NAVY)
    d.text(((W - tw) // 2, 1517), url, font=fu, fill=NAVY if theme in ("nuit", "bleu") else WHITE)
    return lay

# ---------- montage
def segments(r, words):
    """Découpe en séquences (beats + CTA) à partir des mots horodatés."""
    counts = [ntok(t) for t, _ in r["beats"]] + [ntok(CTA[r["cta"]][0])]
    scale = len(words) / sum(counts)
    segs, i = [], 0
    for k, c in enumerate(counts):
        j = len(words) if k == len(counts) - 1 else min(len(words) - 1, i + round(c * scale))
        segs.append((i, j)); i = j
    return segs

def render(r, idx):
    slug = r["slug"]
    raw = [w for w in json.load(open(f"{OUT}/audio/{slug[:3]}.json"))["words"] if w["type"] == "word"]
    words = []
    for w in raw:
        t = w["text"]
        if t.startswith("[") or t.endswith("]"): continue
        if re.fullmatch(r"[?:!.,…]+", t) and words:
            words[-1] = dict(words[-1], text=words[-1]["text"] + t, end=w["end"]); continue
        words.append(dict(w))
    audio = f"{OUT}/audio/{slug[:3]}.mp3"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]))
    total = dur + 1.4
    segs = segments(r, words)
    t0 = ORDER.index(r["theme"])
    plan = []
    for k, (a, b) in enumerate(segs):
        start = 0.0 if k == 0 else words[a]["start"] - 0.05
        is_cta = k == len(segs) - 1
        theme = "bleu" if is_cta else ORDER[(t0 + k) % 4]
        if is_cta and r["theme"] == "bleu" and False: theme = "nuit"
        if not is_cta and k > 0 and theme == "bleu" and k == len(segs) - 2: theme = ORDER[(t0 + k + 1) % 4]
        bgk = big_bg(theme, idx * 3 + k)
        if is_cta:
            lay = cta_layer(r["cta"], theme)
        else:
            pose = ["telephone", "bras-croises", "classeur"][idx % 3] if k == 0 else None
            lay, _ = headline_layer(theme, r["beats"][k][1], pose)
        plan.append(dict(start=start, theme=theme, bg=bgk, lay=lay, words=words[a:b], cta=is_cta))
    allch = chunks(words)
    os.makedirs(f"{OUT}/mp4", exist_ok=True)
    out = f"{OUT}/mp4/{slug}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", audio, "-filter_complex", "[1:a]apad=pad_dur=1.4,loudnorm=I=-14:TP=-1.5:LRA=7[a]", "-map", "0:v", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.2f}", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(total * FPS)
    for fi in range(n):
        now = fi / FPS
        k = max(i for i, s in enumerate(plan) if s["start"] <= now)
        s = plan[k]; nxt = plan[k + 1]["start"] if k + 1 < len(plan) else total
        p = (now - s["start"]) / max(0.5, nxt - s["start"])
        bw, bh = s["bg"].size
        zoom_off = int((bw - W) * (0.15 + 0.7 * p))
        frame = s["bg"].crop((zoom_off, int((bh - H) * 0.5), zoom_off + W, int((bh - H) * 0.5) + H)).convert("RGBA")
        a = ease((now - s["start"]) / 0.35) if k > 0 else 1.0
        lay = s["lay"]
        if a < 1:
            lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            frame.alpha_composite(lay, (0, int(50 * (1 - a))))
        else:
            frame.alpha_composite(lay)
        d = ImageDraw.Draw(frame)
        chrome(d, s["theme"], now / total)
        if not s["cta"]:
            cur = [c for c in allch if c[0]["start"] - 0.05 <= now and (c is allch[-1] or now < allch[allch.index(c) + 1][0]["start"] - 0.05)]
            if cur and cur[-1][0] in s["words"] or (cur and any(w in s["words"] for w in cur[-1])):
                draw_caption(d, s["theme"], cur[-1], now)
        pr.stdin.write(frame.convert("RGB").tobytes())
    pr.stdin.close(); pr.wait()
    return out

if __name__ == "__main__":
    only = sys.argv[1:]
    for i, r in enumerate(REELS):
        if only and r["slug"][:3] not in only: continue
        if not os.path.exists(f"{OUT}/audio/{r['slug'][:3]}.json"): print("skip", r["slug"]); continue
        print(render(r, i), flush=True)
