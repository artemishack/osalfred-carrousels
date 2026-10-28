#!/bin/bash
# getvoice.sh rNN url : télécharge + aligne avec le script v5
cd /home/claude/motion
curl -sS -o audio7/$1.mp3 "$2" && python3 - "$1" <<'PY' 2>&1 | grep -v Warn
import sys,json
sys.path.insert(0,'/home/claude/carrousel'); sys.path.insert(0,'/home/claude/motion')
import walign
from scripts7 import S
k=sys.argv[1]; w=walign.align(S[k],f'audio7/{k}.mp3')
json.dump({'words':w},open(f'audio7/{k}.json','w'),ensure_ascii=False,default=float)
print(k,len(w),' '.join(f"{i}:{x['text']}@{float(x['start']):.2f}" for i,x in enumerate(w)))
PY
