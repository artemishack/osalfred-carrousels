import json,sys
sys.path.insert(0,'.')
from captions7 import caption
from mk import SLUG,SL
IDS=json.load(open('ids8.json'))
TT={"r03":"5 tâches qui volent tes soirées","r04":"Il te doit de l'argent et c'est toi qui es gêné ?","r05":"Un logiciel entier pour 3 boutons ?","r06":"Le même mail, tous les jours ?","r07":"Ton site t'apporte des clients ?","r08":"Combien de clients tu perds en ne décrochant pas ?","r09":"Le même client, tapé 4 fois ?","r10":"Ta vraie marge sur ton dernier projet ?","r11":"Ton dernier logiciel, au placard ?","r12":"Tu pars une semaine, ton entreprise s'arrête ?","r13":"Automatiser, mais par où commencer ?","r14":"Encore un projet sans acompte ?","r15":"22 h, et encore sur tes mails ?"}
def info(r,net):
    url=f"https://raw.githubusercontent.com/artemishack/osalfred-carrousels/main/reels-v8/{SLUG[r]}.mp4"
    d=dict(autoPublish=True,descendants=[],draft=False,firstCommentText="",hasNotReadNotes=False,media=[url],mediaAltText=[],
      publicationDate=dict(dateTime=SL[r]["date"]+"T18:00:00",timezone="Europe/Paris"),shortener=False,smartLinkData=dict(ids=[]),videoCoverMilliseconds=1200)
    if net=="ig": d["text"]=caption(r,"ig"); d["providers"]=[dict(network="instagram")]; d["instagramData"]=dict(type="REEL",showReelOnFeed=True,isAiGenerated=True)
    elif net=="fb": d["text"]=caption(r,"fb"); d["providers"]=[dict(network="facebook")]; d["facebookData"]=dict(type="REEL")
    else:
        d["text"]=caption(r,"ig").replace("Écris KIT en commentaire, ou lien en bio.","Écris KIT en commentaire, lien en bio.").replace(" #gestiondentreprise"," #gestiondentreprise #fyp")
        d["providers"]=[dict(network="tiktok")]
        d["tiktokData"]=dict(title=TT[r],disableComment=False,disableDuet=False,disableStitch=False,privacyOption="PUBLIC_TO_EVERYONE",commercialContentThirdParty=False,commercialContentOwnBrand=True,autoAddMusic=False,isAigc=True)
    return json.dumps(d,ensure_ascii=False)
for a in sys.argv[1:]:
    for net in ("ig","fb","tt"):
        print(a,net,IDS[a][net][0],IDS[a][net][1]); print(info(a,net))
