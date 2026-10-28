"""Alignement local texte -> audio (sans STT) : silences + poids syllabiques."""
import re, json, subprocess, sys
import numpy as np

def envelope(mp3, sr=16000, hop=0.01):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"])
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = int(sr * hop); k = len(x) // n
    e = np.sqrt((x[:k * n].reshape(k, n) ** 2).mean(1))
    return e, hop

def gaps(e, hop, min_gap=0.14):
    db = 20 * np.log10(e + 1e-6); thr = max(db.max() - 38, -50)
    voiced = db > thr
    idx = np.where(voiced)[0]; start, end = idx[0] * hop, (idx[-1] + 1) * hop
    out, i = [], idx[0]
    while i < idx[-1]:
        if not voiced[i]:
            j = i
            while j < len(voiced) and not voiced[j]: j += 1
            if (j - i) * hop >= min_gap: out.append((i * hop, j * hop))
            i = j
        else: i += 1
    return start, end, out

def syl(w):
    w = w.lower()
    if re.search(r"\d", w): return 2.5
    if "." in w and len(w) > 6: return len(w) / 2.2   # url
    n = len(re.findall(r"[aeiouyéèêëàâîïôûùœ]+", w))
    if w.endswith("e") and n > 1: n -= 0.6
    return max(0.6, n)

def align(text, mp3):
    toks = [t for t in re.sub(r"\[[^\]]*\]", " ", text).split() if t]
    merged = []
    for t in toks:
        if re.fullmatch(r"[?:!.,…]+", t) and merged: merged[-1] += t
        else: merged.append(t)
    toks = merged
    e, hop = envelope(mp3)
    t0, t1, gs = gaps(e, hop)
    wts = [syl(t) for t in toks]
    brk = [bool(re.search(r"[.?!…:,]$", t)) for t in toks]
    # pause attendue après ponctuation
    pause = [0.45 if re.search(r"[.?!…]$", t) else 0.22 if brk[i] else 0 for i, t in enumerate(toks)]
    tot = sum(wts) + sum(pause)
    rate = (t1 - t0) / tot
    # timeline nominale
    cur, nominal = t0, []
    for w, p in zip(wts, pause):
        nominal.append([cur, cur + w * rate]); cur += (w + p) * rate
    # DP : appariement monotone frontières ponctuées <-> silences
    B = [i for i, b in enumerate(brk[:-1]) if b]
    E_ = [nominal[i][1] for i in B]
    strong = [bool(re.search(r"[.?!…]$", toks[i])) for i in B]
    m, n = len(B), len(gs)
    INF = 1e9
    dp = [[INF] * (n + 1) for _ in range(m + 1)]; bk = [[None] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = 0
    for i in range(m + 1):
        for j in range(n + 1):
            v = dp[i][j]
            if v >= INF: continue
            if i < m:  # frontière sans silence
                c = v + (1.2 if strong[i] else 0.25)
                if c < dp[i + 1][j]: dp[i + 1][j] = c; bk[i + 1][j] = (i, j, 0)
            if j < n:  # silence hors ponctuation
                c = v + (1.6 if gs[j][1] - gs[j][0] > 0.3 else 0.25)
                if c < dp[i][j + 1]: dp[i][j + 1] = c; bk[i][j + 1] = (i, j, 1)
            if i < m and j < n:
                dd = abs(gs[j][0] - E_[i])
                if dd < 3.5:
                    gl = gs[j][1] - gs[j][0]
                    c = v + dd * 0.45 + (0.7 if strong[i] and gl < 0.25 else 0) + (0.25 if not strong[i] and gl < 0.2 else 0)
                    if c < dp[i + 1][j + 1]: dp[i + 1][j + 1] = c; bk[i + 1][j + 1] = (i, j, 2)
    i, j, pairs = m, n, []
    while (i, j) != (0, 0):
        pi, pj, kind = bk[i][j]
        if kind == 2: pairs.append((B[pi], gs[pj]))
        i, j = pi, pj
    pairs.reverse()
    anchors = [(0, t0)] + [(bi + 1, g[1], g[0]) for bi, g in pairs]
    anchors.append((len(toks), t1 + 0.0, t1))
    words = []
    for k in range(len(anchors) - 1):
        i0, s = anchors[k][0], anchors[k][1]
        i1 = anchors[k + 1][0]; z = anchors[k + 1][2] if len(anchors[k + 1]) > 2 else anchors[k + 1][1]
        seg = list(range(i0, i1)); ws = sum(wts[j] for j in seg) or 1
        c = s
        for j in seg:
            d = (z - s) * wts[j] / ws
            words.append(dict(text=toks[j], type="word", start=round(c, 3), end=round(c + d, 3))); c += d
    return words

if __name__ == "__main__":
    sys.path.insert(0, ".")
    from reels_data import REELS, script
    for key in sys.argv[1:]:
        r = [r for r in REELS if r["slug"].startswith(key)][0]
        w = align(script(r), f"reels/audio/{key}.mp3")
        out = f"reels/audio/{key}.json"
        if key.endswith("-test"): pass
        json.dump({"words": w}, open(out if not sys.stdout.isatty() or True else out, "w"), ensure_ascii=False)
        print(key, len(w))
