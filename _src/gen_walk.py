"""Generate the hero scene: a human and an AI walk hand in hand toward
"Progress & Alignment", passing the three pillars on the way.

Writes the SVG between <!--walk--> and <!--/walk--> in _src/pages/index.html.
Animation lives in assets/style.css (.walkscene ...). Run: python3 _src/gen_walk.py
"""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).parent))
from gen_sprite import limb  # same tapered limbs as every other figure

PAGE = Path(__file__).parent / "pages" / "index.html"
TORSO = ('<path d="M48.7 41 C47.4 52 45.4 64 45 77 C44.7 85 45.6 90 47 92 L53 92 '
         'C54.4 90 55.3 85 55 77 C54.6 64 52.6 52 51.3 41 Z"/>')


def leg(cls):
    # a straight leg hanging from the hip (50, 90); CSS swings it about the hip
    return (f'<g class="{cls}">{limb((50, 89), (50.4, 118), (50, 146), 6.6, 5.0, 4.2)}'
            f'<ellipse cx="53.5" cy="148.6" rx="6.4" ry="3.1"/></g>')


def swing_arm(cls):
    # a free arm hanging from the shoulder (50, 46); CSS swings it about the shoulder
    return (f'<g class="{cls}">{limb((50, 46), (49.5, 63), (50, 79), 4.8, 3.9, 3.3)}'
            f'<circle cx="50" cy="81" r="3.7"/></g>')


def held_arm(direction):
    # an arm reaching to the partner's hand at local x = 50 + 28*direction
    hx = 50 + 28 * direction
    mid = (50 + 15 * direction, 64)
    return f'{limb((50, 46), mid, (hx, 74), 4.8, 3.9, 3.3)}<circle cx="{hx}" cy="75" r="3.9"/>'


def walker(kind, x_off, direction):
    head = "h-human" if kind == "human" else "h-ai"
    # back leg first, then torso, then front leg
    return (f'<g class="walker {kind}" transform="translate({x_off} 0)">'
            f'<ellipse class="wshadow" cx="50" cy="151" rx="19" ry="2.6"/>'
            f'<g class="bob" fill="currentColor">'
            f'{leg("leg-b")}{swing_arm("arm-b" if direction > 0 else "arm-a")}{TORSO}'
            f'{held_arm(direction)}{leg("leg-a")}<use href="#{head}" width="100" height="160"/></g></g>')


def milestone(x, word):
    hw = 14 + len(word) * 6.3  # half width fits the word
    return (f'<g transform="translate({x} 0)">'
            f'<rect x="-2" y="226" width="4" height="40" rx="2" fill="#5b3a1e"/>'
            f'<rect x="{-hw:.1f}" y="206" width="{2 * hw:.1f}" height="26" rx="5" fill="#fbf6ef" stroke="#24170d" stroke-width="1.6"/>'
            f'<text x="0" y="223.5" text-anchor="middle" class="msign">{word}</text></g>')


def tufts(x):
    return (f'<path d="M{x} 268 q2 -9 4 0 q2 -12 4 0 q2 -8 4 0" fill="none" stroke="#7b8a3a" '
            f'stroke-width="1.8" stroke-linecap="round"/>')


def near_tile(ox):
    out = [milestone(ox + 110, "SAFETY"), milestone(ox + 510, "TRUST"), milestone(ox + 910, "RESPONSIBILITY")]
    for i, x in enumerate(range(30, 1200, 95)):
        out.append(tufts(ox + x + (i * 37) % 40))
    for i, x in enumerate(range(60, 1200, 140)):
        c = ("#e07a1f", "#3f7d4a", "#c9a03a", "#5b3a1e")[i % 4]
        out.append(f'<ellipse cx="{ox + x + (i * 53) % 60}" cy="{284 + (i * 7) % 10}" rx="4" ry="2.2" fill="{c}" opacity=".55"/>')
    return "".join(out)


def hills_tile(ox):
    return (f'<path d="M{ox} 236 C{ox+90} 214 {ox+180} 214 {ox+260} 228 C{ox+340} 242 {ox+430} 206 {ox+560} 212 '
            f'C{ox+680} 218 {ox+760} 236 {ox+860} 226 C{ox+960} 216 {ox+1060} 210 {ox+1200} 236 L{ox+1200} 250 L{ox} 250 Z" '
            f'fill="#ead3b4"/>')


def scene():
    human_x, ai_x = 0, 56          # local offsets; hands meet at local x 78
    walkers = walker("human", human_x, +1) + walker("ai", ai_x, -1)
    return f'''<svg class="walkscene" viewBox="0 0 1200 300" preserveAspectRatio="xMidYMax slice" role="img"
     aria-label="A human and an AI walk hand in hand toward a gate marked Progress and Alignment, passing signposts for Safety, Trust and Responsibility.">
  <defs>
    <linearGradient id="ws-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf3e6"/><stop offset="1" stop-color="#f6dcbc"/></linearGradient>
    <radialGradient id="ws-sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd59a"/><stop offset=".45" stop-color="#f7b867" stop-opacity=".55"/><stop offset="1" stop-color="#f7b867" stop-opacity="0"/></radialGradient>
    <clipPath id="ws-clip"><rect width="1200" height="300" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#ws-clip)">
    <rect width="1200" height="300" fill="url(#ws-sky)"/>
    <!-- sun rising behind the gate -->
    <g class="sun"><circle cx="905" cy="150" r="150" fill="url(#ws-sun)"/><circle cx="905" cy="150" r="40" fill="#f9b45c"/></g>
    <g class="rays" stroke="#f0a24a" stroke-width="3" stroke-linecap="round" opacity=".55">
      {"".join(f'<line x1="905" y1="84" x2="905" y2="66" transform="rotate({a} 905 150)"/>' for a in range(-80, 81, 20))}
    </g>
    <!-- a small satellite crossing the sky, for the day job -->
    <g class="sat"><g transform="translate(0 0)">
      <rect x="-5" y="-5" width="10" height="10" rx="2" fill="#24170d"/>
      <rect x="-25" y="-3.5" width="16" height="7" fill="#3f5f8a" stroke="#24170d" stroke-width="1"/>
      <rect x="9" y="-3.5" width="16" height="7" fill="#3f5f8a" stroke="#24170d" stroke-width="1"/>
      <line x1="-9" y1="0" x2="9" y2="0" stroke="#24170d" stroke-width="1.4"/>
      <circle class="blink" cx="0" cy="-8" r="2" fill="#e07a1f"/></g></g>
    <!-- clouds -->
    <g class="clouds" fill="#fffaf3" opacity=".9">
      <path d="M150 92 a16 16 0 0 1 30 -8 a20 20 0 0 1 36 4 a13 13 0 0 1 4 26 h-66 a12 12 0 0 1 -4 -22 z"/>
      <path d="M560 60 a12 12 0 0 1 22 -6 a15 15 0 0 1 27 3 a10 10 0 0 1 3 19 h-49 a9 9 0 0 1 -3 -16 z"/>
      <path d="M1350 100 a16 16 0 0 1 30 -8 a20 20 0 0 1 36 4 a13 13 0 0 1 4 26 h-66 a12 12 0 0 1 -4 -22 z"/>
      <path d="M1760 60 a12 12 0 0 1 22 -6 a15 15 0 0 1 27 3 a10 10 0 0 1 3 19 h-49 a9 9 0 0 1 -3 -16 z"/>
    </g>
    <!-- far hills drift slowly -->
    <g class="drift-far">{hills_tile(0)}{hills_tile(1200)}</g>
    <!-- the destination -->
    <g class="gate">
      <path d="M838 240 V150 Q905 70 972 150 V240" fill="none" stroke="#24170d" stroke-width="8" stroke-linecap="round"/>
      <path d="M838 240 V150 Q905 70 972 150 V240" fill="none" stroke="#e07a1f" stroke-width="3.4" stroke-linecap="round"/>
      <circle cx="905" cy="100" r="5" fill="#e07a1f" stroke="#24170d" stroke-width="2"/>
      <rect x="826" y="150" width="158" height="38" rx="7" fill="#24170d"/>
      <text x="905" y="165" text-anchor="middle" class="gsign">PROGRESS &amp;</text>
      <text x="905" y="181" text-anchor="middle" class="gsign">ALIGNMENT</text>
    </g>
    <!-- near ground scrolls at walking pace -->
    <rect y="248" width="1200" height="52" fill="#e6cba6"/>
    <line x1="0" y1="248" x2="1200" y2="248" stroke="#24170d" stroke-width="1.6"/>
    <g class="drift-near">{near_tile(0)}{near_tile(1200)}</g>
    <g class="drift-path"><line x1="0" y1="276" x2="2400" y2="276" stroke="#c9a77d" stroke-width="3" stroke-dasharray="26 34" stroke-linecap="round"/></g>
    <!-- the walkers -->
    <g transform="translate(372 76) scale(1.24)">
      {walkers}
      <g class="heart"><path d="M78 66 c-4 -6 -13 -2 -9 5 l9 8 l9 -8 c4 -7 -5 -11 -9 -5 z" fill="#e07a1f"/></g>
    </g>
  </g>
</svg>'''


def main():
    s = PAGE.read_text(encoding="utf-8")
    new, n = re.subn(r"<!--walk-->.*?<!--/walk-->", "<!--walk-->\n" + scene() + "\n<!--/walk-->", s, flags=re.S)
    if n != 1:
        raise SystemExit("index.html needs one <!--walk--><!--/walk--> marker pair")
    PAGE.write_text(new, encoding="utf-8")
    print("wrote walk scene into", PAGE)


if __name__ == "__main__":
    main()
