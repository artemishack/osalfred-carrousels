import json, sys, subprocess, os
sys.path.insert(0, "/home/claude/motion")
from playwright.sync_api import sync_playwright
import reels7 as reels4
BASE = "/home/claude/motion"; FPS = 60

def cfg(key):
    voice = f"{BASE}/audio7/{key}.mp3"; words = json.load(open(voice.replace(".mp3", ".json")))["words"]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice]))
    END = dur + 2.6
    c = reels4.ALL[key](lambda i: float(words[i]["start"]), END); c["dur"] = END; reels4.blueline(c)
    return c, voice, END

def page(p, c):
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(f"file://{BASE}/engine5.html"); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
    pg.evaluate("c=>build(c)", c); return b, pg

def shots(key, times, out):
    from PIL import Image; import io
    c, _, _ = cfg(key)
    with sync_playwright() as p:
        b, pg = page(p, c); ims = []
        for t in times: pg.evaluate(f"render({t})"); ims.append(Image.open(io.BytesIO(pg.screenshot(type="jpeg", quality=80))).resize((270, 480)))
        b.close()
    s = Image.new("RGB", (len(ims) * 276, 480), "white")
    for k, im in enumerate(ims): s.paste(im, (k * 276, 0))
    s.save(out)

def render(key):
    c, voice, total = cfg(key)
    os.makedirs(f"{BASE}/out7", exist_ok=True)
    out = f"{BASE}/out7/{c['slug']}.mp4"; silent = out.replace(".mp4", ".v.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, pg = page(p, c)
        for f in range(int(total * FPS)): pg.evaluate(f"render({f / FPS})"); ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
        b.close()
    ff.stdin.close(); ff.wait()
    music = f"{BASE}/audio/nappe.mp3"; wh = f"{BASE}/audio/whoosh.mp3"
    cuts = [x["t"] for x in c.get("bg", [])] + c.get("swoosh", [])
    inputs = ["-i", silent, "-i", voice, "-stream_loop", "-1", "-i", music]; n = 3
    fc = ["[1:a]apad=pad_dur=2,asplit=2[v][vsc]",
          f"[2:a]atrim=0:{total:.2f},volume=0.24,afade=t=in:d=0.5,afade=t=out:st={total-1.5:.2f}:d=1.5[m0]",
          "[m0][vsc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=350[m]"]
    mix = ["[v]", "[m]"]
    for j, t in enumerate(cuts):
        inputs += ["-i", wh]; n += 1; d = int(max(0, t - .25) * 1000)
        fc.append(f"[{n-1}:a]adelay={d}|{d},volume=0.5[w{j}]"); mix.append(f"[w{j}]")
    fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.2f}", "-movflags", "+faststart", out], check=True)
    os.remove(silent); return out

if __name__ == "__main__":
    if sys.argv[1] == "shots": shots(sys.argv[2], [float(x) for x in sys.argv[3:]], f"{BASE}/check/v7_{sys.argv[2]}.jpg")
    else:
        for k in sys.argv[1:]: print(render(k), flush=True)
