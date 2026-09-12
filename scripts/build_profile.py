"""Build the self-contained GitHub profile image (Python standard library only)."""
from pathlib import Path
import random
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent.parent
rng = random.Random(12)
cells = []
for row in range(10):
    for col in range(18):
        delay = rng.uniform(0, 0.18)
        cells.append(f'<rect class="pixel" x="{col*60}" y="{row*62}" width="61" height="63" style="animation-delay:{2.8+delay:.3f}s,{7.3+delay:.3f}s"/>')
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="620" viewBox="0 0 1080 620" role="img" aria-labelledby="title desc">
<title id="title">jux — personal and selected work</title><desc id="desc">A blue and white two-sided poster. The name jux appears, a pixel transition reveals Articles-Auto, then the image returns to the personal side. Project links are below the image.</desc>
<style>
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:'Courier New',monospace;letter-spacing:3px;font-size:16px}.personal{opacity:1;animation:personal 8s step-end both}.work{opacity:0;animation:work 8s step-end both}.pixel{fill:#92ccea;opacity:0;animation:cover .52s step-end,cover .52s step-end}.name{font-weight:900;font-size:280px;letter-spacing:-25px;fill:#064976}.letter{animation:letter .65s steps(1,end) both}.two{animation-delay:.12s}.three{animation-delay:.24s}
@keyframes personal{0%{opacity:1}38%{opacity:0}94.3%,100%{opacity:1}}
@keyframes work{0%{opacity:0}38%{opacity:1}94.3%,100%{opacity:0}}
@keyframes cover{0%{opacity:0}1%,55%{opacity:1}100%{opacity:0}}
@keyframes letter{0%{opacity:.1}20%{opacity:.8}35%{opacity:.15}55%{opacity:1}65%{opacity:.4}100%{opacity:1}}
@media(prefers-reduced-motion:reduce){.personal,.work,.pixel,.letter{animation:none}.personal{opacity:1}.work,.pixel{opacity:0}}
</style><defs><linearGradient id="water" x2=".3" y2="1"><stop stop-color="#c0f4ff"/><stop offset=".45" stop-color="#159cc5"/><stop offset="1" stop-color="#003f7b"/></linearGradient><radialGradient id="light"><stop stop-color="white" stop-opacity=".8"/><stop offset="1" stop-color="#9aefff" stop-opacity="0"/></radialGradient><clipPath id="art"><path d="M620 0H1080V620H510Z"/></clipPath></defs>
<g class="personal"><path fill="#f7fbfd" d="M0 0h1080v620H0z"/><g clip-path="url(#art)"><path fill="url(#water)" d="M480 0h600v620H480z"/><ellipse cx="1020" cy="110" rx="260" ry="290" fill="url(#light)"/><g stroke="#bbf3fa" fill="none" opacity=".35"><ellipse cx="930" cy="580" rx="420" ry="70"/><ellipse cx="930" cy="580" rx="350" ry="52"/><ellipse cx="930" cy="580" rx="230" ry="33"/></g><path d="M870 -60L690 620h90L1030 -20Z" fill="#e9ffff" opacity=".12"/><path d="M680 -60L535 620h35L760 -30Z" fill="#e9ffff" opacity=".13"/><circle cx="875" cy="260" r="125" fill="none" stroke="#efffff" opacity=".4"/></g>
<g fill="#113659"><text x="40" y="50" class="mono">01 / PERSONAL</text><text x="1034" y="48" text-anchor="end" font-size="28">✳</text><text class="name" x="28" y="325"><tspan class="letter">j</tspan><tspan class="letter two">u</tspan><tspan class="letter three">x</tspan></text><text x="42" y="455" font-size="23">@jdahd</text><text x="42" y="495" class="mono">CODE / IMAGES / IDEAS</text></g><path fill="#f7fbfd" opacity=".85" d="M0 542h1080v78H0z"/><path stroke="#113659" opacity=".15" d="M0 542h1080"/><g fill="#113659" class="mono"><text x="40" y="588">PERSONAL EDITION</text><text x="1040" y="588" text-anchor="end">JUX / 001</text></g></g>
<g class="work"><path fill="#102f4e" d="M0 0h1080v620H0z"/><text x="40" y="50" fill="#a6c2d9" class="mono">02 / SELECTED WORK</text><g fill="#ecf5fc"><text x="38" y="164" font-size="80" letter-spacing="-4">Articles</text><text x="38" y="247" font-size="80" letter-spacing="-4">— Auto.</text></g><g fill="#bdd2e4" font-size="22"><text x="42" y="333">Save articles and images.</text><text x="42" y="370">Keep a local copy.</text></g>
<g transform="translate(596 65) rotate(7)"><path fill="#29779d" d="M-18 18h425v426H-18z"/><path fill="#f5f2e9" d="M0 0h425v426H0z"/><g fill="#243e50"><text x="30" y="43" font-family="monospace" font-size="14" letter-spacing="2">ARTICLES-AUTO / EXPORT</text><text x="30" y="128" style="font-family:Georgia,serif" font-size="48">Articles.</text><text x="30" y="181" style="font-family:Georgia,serif" font-size="48">Kept locally.</text></g><g stroke="#243e50" opacity=".12" stroke-width="7"><path d="M30 227h365M30 249h365M30 271h265"/></g><g fill="#243e50" font-size="18"><text x="30" y="330">Markdown / HTML / Word</text></g></g>
<path stroke="#fff" opacity=".2" d="M0 542h1080"/><g fill="#ecf5fc" class="mono"><text x="40" y="588">SELECTED WORK</text><text x="1040" y="588" text-anchor="end">LINK BELOW ↗</text></g></g>
''' + '\n'.join(cells) + '</svg>\n'
ET.fromstring(svg)
(root / 'assets' / 'double-sided.svg').write_text(svg)
print(f'Built assets/double-sided.svg ({len(svg.encode()):,} bytes)')
static = svg.replace('</style>', '.personal,.work,.pixel,.letter{animation:none!important}.personal{opacity:1}.work,.pixel{opacity:0}</style>')
(root / 'assets' / 'double-sided-static.svg').write_text(static)
