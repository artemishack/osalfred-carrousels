import glob, sys
from PIL import Image, ImageDraw
files = sorted(glob.glob('out/covers/*.png'))
n = int(sys.argv[1]) if len(sys.argv)>1 else len(files)
files = files[:n][::-1]
tw, th, g = 300, 400, 4
rows = (len(files)+2)//3
s = Image.new('RGB', (3*tw+2*g, rows*th+(rows-1)*g), 'white')
for k,f in enumerate(files):
    im = Image.open(f); cw = int(im.size[1]*3/4); x=(im.size[0]-cw)//2
    im = im.crop((x,0,x+cw,im.size[1])).resize((tw,th), Image.LANCZOS)
    s.paste(im, ((k%3)*(tw+g), (k//3)*(th+g)))
s.save(sys.argv[2] if len(sys.argv)>2 else 'out/feed.png')
