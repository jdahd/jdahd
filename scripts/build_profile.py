"""Build self-contained profile SVGs from local artwork and an outlined wordmark."""
from pathlib import Path
import base64
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent.parent
assets = root / 'assets'
gallery = assets / 'gallery'

def data(name):
    return 'data:image/jpeg;base64,' + base64.b64encode((gallery / name).read_bytes()).decode()

names = ['underwater.jpg', 'blue-sky.jpg', 'cloud-sea.jpg']
imgs = [data(name) for name in names]
wordmark = (gallery / 'wordmark-path.txt').read_text()
style = '''
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:monospace;font-size:15px;letter-spacing:2px}.photo{transform-origin:600px 337px}.base-photo{animation:drift 13s ease-out both}.photo-two{animation:drift 5s 4s ease-out both}.photo-three{animation:drift 5s 8s ease-out both}.slice{transform-box:fill-box;transform-origin:center;transform:scaleY(0)}.slice-two{animation:open 700ms cubic-bezier(.22,1,.36,1) both}.slice-three{animation:open 700ms cubic-bezier(.22,1,.36,1) both,shut 600ms cubic-bezier(.65,0,.35,1) forwards}.scene-two{animation:hide-two 14s step-end both}.wordmark{animation:arrive 1.1s cubic-bezier(.22,1,.36,1) both}.echo{opacity:0;animation:echo .7s .15s ease-out both}.indicator-two{opacity:0;animation:active-two 14s step-end both}.indicator-three{opacity:0;animation:active-three 14s step-end both}.indicator-one{animation:active-one 14s step-end both}
@keyframes drift{from{transform:scale(1.055) translate(-7px,3px)}to{transform:scale(1)}}
@keyframes open{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes shut{from{transform:scaleY(1)}to{transform:scaleY(0)}}
@keyframes hide-two{0%,84%{opacity:1}84.1%,100%{opacity:0}}
@keyframes arrive{from{opacity:0;transform:translateX(-28px)}to{opacity:1;transform:translateX(0)}}
@keyframes echo{0%{opacity:.7;transform:translateX(18px)}100%{opacity:0;transform:translateX(0)}}
@keyframes active-one{0%{opacity:1}31%{opacity:0}92%,100%{opacity:1}}
@keyframes active-two{0%{opacity:0}31%{opacity:1}60%,100%{opacity:0}}
@keyframes active-three{0%{opacity:0}60%{opacity:1}92%,100%{opacity:0}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.scene-two,.scene-three,.echo,.indicator-two,.indicator-three{display:none}.photo,.wordmark{transform:none}.indicator-one{opacity:1}}
'''

# Each image is defined once; all artwork bytes live inside the SVG.
def make(static=False):
    extra = '*{animation:none!important}.scene-two,.scene-three,.echo,.indicator-two,.indicator-three{display:none}.photo,.wordmark{transform:none}.indicator-one{opacity:1}' if static else ''
    defs = ''.join(f'<image id="photo{i}" width="1200" height="675" preserveAspectRatio="xMidYMid slice" href="{src}"/>' for i,src in enumerate(imgs if not static else imgs[:1]))
    clips = ''
    for scene in [2,3]:
        cells = ''
        for i in range(12):
            delay = (4 if scene==2 else 8) + (i%3)*.075 + i*.012
            end = 12 + (11-i)*.024
            delays = f'{delay:.3f}s' if scene==2 else f'{delay:.3f}s,{end:.3f}s'
            cells += f'<rect x="{i*100}" y="0" width="101" height="675" class="slice slice-{["two","three"][scene-2]}" style="animation-delay:{delays}"/>'
        clips += f'<clipPath id="slices{scene}">{cells}</clipPath>'
    overlays = '' if static else '<g class="scene-two" clip-path="url(#slices2)"><use href="#photo1" class="photo photo-two"/></g><g class="scene-three" clip-path="url(#slices3)"><use href="#photo2" class="photo photo-three"/></g>'
    thumbs = ''
    # Thumbnails are actual selected frames, not decorative controls.
    if not static:
        for i in range(3):
            x=874+i*88
            thumbs += f'<svg x="{x}" y="692" width="72" height="40" viewBox="0 0 1200 675"><use href="#photo{i}"/></svg><path class="indicator-{["one","two","three"][i]}" d="M{x} 738h72" stroke="#237da0" stroke-width="3"/>'
    else:
        thumbs = '<text x="1145" y="720" text-anchor="end" class="mono" fill="#315269">01 / STILL</text>'
    out = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="752" viewBox="0 0 1200 752" role="img" aria-labelledby="title desc">
<title id="title">jux — a blue visual collection</title><desc id="desc">Three selected wallpapers: Makoto Yuki underwater, a blue-sky portrait, and a cloud-sea scene. Staggered vertical shutters reveal each image, then return to Makoto Yuki. The italic jux wordmark stays to the left. Links below lead to the projects.</desc>
<style>{style}{extra}</style><defs>{defs}{clips}<linearGradient id="shade"><stop stop-color="#041329" stop-opacity=".78"/><stop offset=".5" stop-color="#071c32" stop-opacity=".24"/><stop offset="1" stop-color="#071c32" stop-opacity="0"/></linearGradient><clipPath id="frame"><path d="M0 0h1200v675H0z"/></clipPath><path id="logo" d="{wordmark}"/></defs>
<path fill="#eef5f8" d="M0 0h1200v752H0z"/><g clip-path="url(#frame)"><use href="#photo0" class="photo base-photo"/>{overlays}<path fill="url(#shade)" d="M0 0h1200v675H0z"/></g>
<g fill="#f4faff"><text x="52" y="52" class="mono">JUX / @JDAHD</text><text x="1148" y="52" class="mono" text-anchor="end">VISUAL COLLECTION</text>
<g transform="translate(128 342) scale(.30)"><g class="echo" fill="#a2dfff"><use href="#logo"/></g><g class="wordmark"><use href="#logo"/></g></g>
<text x="57" y="430" font-size="19" letter-spacing="5">CODE / IMAGES / IDEAS</text><path d="M56 469h42" stroke="#c7e6f4"/><text x="56" y="630" class="mono">PERSONAL EDITION — 002</text></g>
<g fill="#29465b"><text x="52" y="717" font-size="20">jux.</text><text x="125" y="718" class="mono">SELECTED FRAMES</text></g>{thumbs}</svg>'''
    ET.fromstring(out)
    return out

for filename,static in [('double-sided.svg',False),('double-sided-static.svg',True)]:
    svg=make(static)
    (assets/filename).write_text(svg)
    print(filename, f'{len(svg.encode())/1024:.0f} KB')
