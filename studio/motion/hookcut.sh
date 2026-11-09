#!/bin/bash
# hookcut.sh src.mp4 t_audio t_video hold out.mp4
# Retire l'interjection d'ouverture d'un reel déjà rendu (test « ouverture sans interjection », semaine du 09/11).
# Audio coupé juste avant le premier mot utile (t_audio) ; image figée sur l'accroche complète (t_video) pendant hold = t_video - t_audio.
# r05b : 0.70 1.30 0.60 · r07b : 0.92 1.50 0.58 (sources : reels-v8/)
ffmpeg -v error -y -i "$1" -filter_complex "[0:v]trim=start=$3,setpts=PTS-STARTPTS,tpad=start_duration=$4:start_mode=clone[v];[0:a]atrim=start=$2,asetpts=PTS-STARTPTS,afade=t=in:d=0.03[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$5"
