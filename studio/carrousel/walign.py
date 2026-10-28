"""Horodatage mot à mot local (faster-whisper) recalé sur le texte exact du script."""
import re, sys, json, difflib, unicodedata
from faster_whisper import WhisperModel

_M = None
def model():
    global _M
    if _M is None: _M = WhisperModel("small", device="cpu", compute_type="int8")
    return _M

def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", t)

def tokens(text):
    out = []
    for t in re.sub(r"\[[^\]]*\]", " ", text).split():
        if re.fullmatch(r"[?:!.,…]+", t) and out: out[-1] += t
        else: out.append(t)
    return out

def align(text, mp3):
    toks = tokens(text)
    import subprocess, numpy as np
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"])
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs, _ = model().transcribe(audio, language="fr", word_timestamps=True, beam_size=5)
    ww = [w for s in segs for w in s.words]
    # aligner caractère par caractère : chaque caractère normalisé porte le temps de son mot
    a_chars, a_idx = [], []
    for i, t in enumerate(toks):
        for c in norm(t): a_chars.append(c); a_idx.append(i)
    b_chars, b_time = [], []
    for w in ww:
        n = norm(w.word); L = max(1, len(n))
        for k, c in enumerate(n):
            b_chars.append(c); b_time.append(w.start + (w.end - w.start) * k / L)
    sm = difflib.SequenceMatcher(None, a_chars, b_chars, autojunk=False)
    t_of = [None] * len(a_chars)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): t_of[blk.a + k] = b_time[blk.b + k]
    starts = [None] * len(toks)
    for ci, ti in enumerate(a_idx):
        if starts[ti] is None and t_of[ci] is not None: starts[ti] = t_of[ci]
    # interpolation des trous
    known = [i for i, s in enumerate(starts) if s is not None]
    end_t = ww[-1].end if ww else 0
    for i in range(len(starts)):
        if starts[i] is None:
            p = max([k for k in known if k < i], default=None); q = min([k for k in known if k > i], default=None)
            sp = starts[p] if p is not None else 0.0; sq = starts[q] if q is not None else end_t
            ip = p if p is not None else -1; iq = q if q is not None else len(starts)
            starts[i] = sp + (sq - sp) * (i - ip) / (iq - ip)
    words = []
    for i, t in enumerate(toks):
        e = starts[i + 1] - 0.02 if i + 1 < len(toks) else end_t
        words.append(dict(text=t, type="word", start=round(starts[i], 3), end=round(max(e, starts[i] + 0.05), 3)))
    return words

if __name__ == "__main__":
    sys.path.insert(0, ".")
    from reels_data import REELS, script
    for key in sys.argv[1:]:
        r = [r for r in REELS if r["slug"].startswith(key)][0]
        w = align(script(r), f"reels/audio/{key}.mp3")
        json.dump({"words": w, "source": "whisper"}, open(f"reels/audio/{key}.json", "w"), ensure_ascii=False)
        print(key, len(w), flush=True)
