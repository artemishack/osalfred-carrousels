import sys, glob, shutil
from engine import build
from data import CAR
only = sys.argv[1:]
for slug, slides in CAR.items():
    if only and slug not in only: continue
    out = build(slug, slides)
    cv = glob.glob(f"out/covers/*-{slug}.png")[0]
    shutil.copy(cv, f"{out}/planche-1.png")
    print(slug, len(slides), flush=True)
