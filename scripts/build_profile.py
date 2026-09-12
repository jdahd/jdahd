"""Build GitHub-compatible image sequences; no runtime scripts or external assets."""
from pathlib import Path
import base64
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent.parent
assets = root / 'assets'
gallery = assets / 'gallery'
names = ['underwater.jpg', 'blue-sky.jpg', 'cloud-sea.jpg', 'sunset.jpg', 'floating-city.jpg']
wordmark = (gallery / 'wordmark-path.txt').read_text()

STYLE = '''
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:monospace;font-size:15px;letter-spacing:2px}
.photo{transform-origin:600px 337px;animation:drift 5s ease-out both}
.p1{animation-duration:4s}.p2{animation-delay:4s}.p3{animation-delay:8s}.p4{animation-delay:12s}.p5{animation-delay:16s}.p6{animation-delay:20s}
.blade{transform-box:fill-box;transform-origin:center;animation:open-y .75s cubic-bezier(.22,1,.36,1) both}
.iris{transform-origin:830px 330px;animation:iris 1.05s 8s cubic-bezier(.22,1,.36,1) both}
.diagonal{animation:diagonal .95s 12s cubic-bezier(.65,0,.35,1) both}
.dissolve{animation:dissolve 1.25s 16s ease-in-out both}
.top-half{animation:from-left .95s 20s cubic-bezier(.65,0,.35,1) both}
.bottom-half{animation:from-right .95s 20s cubic-bezier(.65,0,.35,1) both}
.wordmark{animation:arrive 1.1s cubic-bezier(.22,1,.36,1) both}
@keyframes drift{from{transform:scale(1.035)}to{transform:scale(1)}}
@keyframes open-y{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes iris{from{transform:scale(0)}to{transform:scale(1)}}
@keyframes diagonal{from{transform:translateX(-1750px)}to{transform:translateX(0)}}
@keyframes dissolve{from{opacity:0}to{opacity:1}}
@keyframes from-left{from{transform:translateX(-1201px)}to{transform:translateX(0)}}
@keyframes from-right{from{transform:translateX(1201px)}to{transform:translateX(0)}}
@keyframes arrive{from{opacity:0;transform:translateX(-18px)}to{opacity:1;transform:translateX(0)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.sequence{display:none}.photo,.wordmark{transform:none}}
'''

def make(static=False):
    images = ''.join(f'<image id="photo{i}" width="1200" height="675" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{base64.b64encode((gallery/name).read_bytes()).decode()}"/>' for i,name in enumerate(names[:1] if static else names))
    blades=''.join(f'<rect x="{i*100}" width="101" height="675" class="blade" style="animation-delay:{4+i*.025:.3f}s"/>' for i in range(12))
    clips=f'''<clipPath id="blinds">{blades}</clipPath>
<clipPath id="circle"><circle cx="830" cy="330" r="1100" class="iris"/></clipPath>
<clipPath id="diagonal"><path class="diagonal" d="M0 0H1750L1350 675H-400Z"/></clipPath>
<clipPath id="split"><rect width="1200" height="338" class="top-half"/><rect y="337" width="1200" height="338" class="bottom-half"/></clipPath>'''
    sequence='' if static else '''<g class="sequence">
<g clip-path="url(#blinds)"><use href="#photo1" class="photo p2"/></g>
<g clip-path="url(#circle)"><use href="#photo2" class="photo p3"/></g>
<g clip-path="url(#diagonal)"><use href="#photo3" class="photo p4"/></g>
<g class="dissolve"><use href="#photo4" class="photo p5"/></g>
<g clip-path="url(#split)"><use href="#photo0" class="photo p6"/></g></g>'''
    extra='*{animation:none!important}.photo,.wordmark{transform:none}' if static else ''
    out=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675" role="img" aria-labelledby="title desc">
<title id="title">jux — selected images</title><desc id="desc">Five wallpapers with vertical shutters, a circular reveal, a diagonal wipe, a dissolve, and a split return to Makoto Yuki. Italic jux and a separate subtitle sit at the left. Project links follow the image.</desc>
<style>{STYLE}{extra}</style><defs>{images}{clips}
<linearGradient id="shade"><stop stop-color="#041329" stop-opacity=".78"/><stop offset=".5" stop-color="#071c32" stop-opacity=".24"/><stop offset="1" stop-color="#071c32" stop-opacity="0"/></linearGradient>
<clipPath id="frame"><rect width="1200" height="675"/></clipPath><path id="logo" d="{wordmark}"/></defs>
<g clip-path="url(#frame)"><use href="#photo0" class="photo p1"/>{sequence}<path fill="url(#shade)" d="M0 0h1200v675H0z"/>
<g fill="#f4faff"><text x="52" y="52" class="mono">JUX / @JDAHD</text><text x="1148" y="52" class="mono" text-anchor="end">VISUAL COLLECTION</text>
<g id="wordmark-box" transform="translate(126 322) scale(.28)"><g class="wordmark"><use href="#logo"/></g></g>
<text id="subtitle" x="58" y="480" font-size="19" letter-spacing="5">CODE / IMAGES / IDEAS</text></g></g></svg>'''
    ET.fromstring(out)
    return out

for filename,static in [('double-sided.svg',False),('double-sided-static.svg',True)]:
    svg=make(static); (assets/filename).write_text(svg)
    print(filename, f'{len(svg.encode())/1024:.0f} KB')
