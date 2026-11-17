"""Rendu des reels v10 (moteur engine9.html : three.js 3D + textes DOM, seek déterministe).
python3 render8.py shots r15c 0 3 6 9 12 15 18   -> planche de contrôle
python3 render8.py r15c                            -> MP4
"""
import json, sys, subprocess, os
from playwright.sync_api import sync_playwright
BASE = "/home/claude/motion"; FPS = 30

REELS = {
    # r15 sans l'interjection « Regarde l'heure. » (coupe à 0,88 s), habillage 3D
    "r15c": dict(src="audio7/r15", cut=0.88, slug="r15d-vingt-deux-heures-verre",
                 lines=[[0, 10], [11, 18], [19, 23], [24, 29], [30, 32], [33, 38], [39, 41], [42, 48], [49, 53], [54, 60]],
                 key=[10, 23, 38, 41, 47, 53], rename={40: "OS"}),
}

def cfg(k):
    r = REELS[k]; os.makedirs(f"{BASE}/audio8", exist_ok=True)
    voice = f"{BASE}/audio8/{k}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(r["cut"]), "-i", f"{BASE}/{r['src']}.mp3", "-af", "afade=t=in:d=0.03", voice], check=True)
    words = json.load(open(f"{BASE}/{r['src']}.json"))["words"]
    first = next(i for i, w in enumerate(words) if float(w["start"]) >= r["cut"] - 0.01)
    ws = [{"text": w["text"], "start": max(0.0, float(w["start"]) - r["cut"])} for w in words[first:]]
    for i, t in r.get("rename", {}).items(): ws[i]["text"] = t
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice]))
    c = {"words": ws, "lines": r["lines"], "key": r["key"], "dur": dur + 2.6, "slug": r["slug"]}
    return c, voice

def page(p, c):
    b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(f"file://{BASE}/engine9.html"); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
    pg.evaluate("c=>build(c)", c); pg.evaluate("render(0)"); pg.wait_for_timeout(300)
    return b, pg

def shots(k, times, out):
    from PIL import Image; import io
    c, _ = cfg(k)
    with sync_playwright() as p:
        b, pg = page(p, c); ims = []
        for t in times:
            pg.evaluate(f"render({t})"); ims.append(Image.open(io.BytesIO(pg.screenshot(type="jpeg", quality=82))).resize((360, 640)))
        b.close()
    s = Image.new("RGB", (len(ims) * 366, 640), "white")
    for i, im in enumerate(ims): s.paste(im, (i * 366, 0))
    s.save(out); print(out)

def render(k):
    c, voice = cfg(k); total = c["dur"]
    os.makedirs(f"{BASE}/out9", exist_ok=True)
    out = f"{BASE}/out9/{c['slug']}.mp4"; silent = out.replace(".mp4", ".v.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, pg = page(p, c)
        for f in range(int(total * FPS)):
            pg.evaluate(f"render({f / FPS})"); ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
            if f % 60 == 0: print(f"  frame {f}/{int(total*FPS)}", flush=True)
        b.close()
    ff.stdin.close(); ff.wait()
    W = c["words"]; T = lambda i: W[i]["start"]
    hits = [T(11), T(12), T(13), T(14), T(30), T(39), T(54)]   # chute des cartes, retournement, solution, CTA
    music = f"{BASE}/audio/nappe.mp3"; wh = f"{BASE}/audio/whoosh.mp3"
    inputs = ["-i", silent, "-i", voice, "-stream_loop", "-1", "-i", music]; n = 3
    fc = ["[1:a]apad=pad_dur=2.6,asplit=2[v][vsc]",
          f"[2:a]atrim=0:{total:.2f},volume=0.24,afade=t=in:d=0.4,afade=t=out:st={total-1.5:.2f}:d=1.5[m0]",
          "[m0][vsc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=350[m]"]
    mix = ["[v]", "[m]"]
    for j, t in enumerate(hits):
        inputs += ["-i", wh]; n += 1; d = int(max(0, t - .18) * 1000)
        fc.append(f"[{n-1}:a]adelay={d}|{d},volume={0.32 if j < 4 else 0.5}[w{j}]"); mix.append(f"[w{j}]")
    fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.2f}", "-movflags", "+faststart", out], check=True)
    os.remove(silent); return out

if __name__ == "__main__":
    if sys.argv[1] == "shots": shots(sys.argv[2], [float(x) for x in sys.argv[3:]], f"{BASE}/check/v9_{sys.argv[2]}.jpg")
    else:
        for k in sys.argv[1:]: print(render(k), flush=True)
