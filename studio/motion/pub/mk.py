import json,sys
sys.path.insert(0,'.')
from captions7 import caption
SL=json.load(open('slots7.json'))
SLUG={"r01":"r01-devis-silence","r02":"r02-excel-soirees","r03":"r03-cinq-taches","r04":"r04-facture-impayee","r05":"r05-logiciel-trois-boutons","r06":"r06-ia-mails","r07":"r07-site-clients","r08":"r08-appel-manque","r09":"r09-saisie-unique","r10":"r10-marge-reelle","r11":"r11-logiciel-placard","r12":"r12-semaine-vacances","r13":"r13-par-ou-commencer","r14":"r14-acompte","r15":"r15-vingt-deux-heures"}
def info(r,net):
    url=f"https://raw.githubusercontent.com/artemishack/osalfred-carrousels/main/reels-v7/{SLUG[r]}.mp4"
    d=dict(autoPublish=True,descendants=[],draft=False,firstCommentText="",hasNotReadNotes=False,media=[url],mediaAltText=[],
           publicationDate=dict(dateTime=SL[r]["date"]+"T18:00:00",timezone="Europe/Paris"),shortener=False,smartLinkData=dict(ids=[]),
           text=caption(r,net),videoCoverMilliseconds=1200)
    if net=="ig": d["providers"]=[dict(network="instagram")]; d["instagramData"]=dict(type="REEL",showReelOnFeed=True,isAiGenerated=True)
    else: d["providers"]=[dict(network="facebook")]; d["facebookData"]=dict(type="REEL")
    return json.dumps(d,ensure_ascii=False)
for a in (sys.argv[1:] if __name__=="__main__" else []):
    r,net=a.split(':'); print(a, SL[r].get(net)); print(info(r,net))
