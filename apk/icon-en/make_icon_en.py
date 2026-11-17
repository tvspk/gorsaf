"""Make the EN app icons: the original icons + a red 'EN' badge. Output: apk/icon-en/res/mipmap-*/ (overlaid by build_en.sh)."""
import os,sys
from PIL import Image,ImageDraw,ImageFont
root=sys.argv[1]
FONT=[f for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'] if os.path.exists(f)][0]
RED=(200,16,46,255);WHITE=(255,255,255,255)
def badge(im,cx,cy,w,h):
    d=ImageDraw.Draw(im);r=h*0.32;bw=max(1,round(h*0.07))
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],radius=r,fill=RED,outline=WHITE,width=bw)
    f=ImageFont.truetype(FONT,round(h*0.62));t='EN';b=d.textbbox((0,0),t,font=f)
    d.text((cx-(b[2]-b[0])/2-b[0],cy-(b[3]-b[1])/2-b[1]),t,font=f,fill=WHITE)
for dens in ['mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi']:
    src=f'{root}/apk/project/res/mipmap-{dens}';out=f'{root}/apk/icon-en/res/mipmap-{dens}';os.makedirs(out,exist_ok=True)
    fg=Image.open(f'{src}/ic_launcher_foreground.png').convert('RGBA');s=fg.size[0]/432
    big=fg.resize((432,432),Image.LANCZOS) if s!=1 else fg.copy()
    badge(big,216,312,100,48)   # inside the adaptive-icon safe circle (radius 132 around the centre)
    big.resize(fg.size,Image.LANCZOS).save(f'{out}/ic_launcher_foreground.png')
    lg=Image.open(f'{src}/ic_launcher.png').convert('RGBA');k=lg.size[0]/192
    up=lg.resize((768,768),Image.LANCZOS);badge(up,768*0.72,768*0.80,768*0.36,768*0.17)
    up.resize(lg.size,Image.LANCZOS).save(f'{out}/ic_launcher.png')
print('EN icons written')
