"""Generate the hero scene: a human and an AI walk hand in hand toward
"Safety & Alignment", passing the three pillars on the way.

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


# ---- the human: an original flat cartoon (quiff, beard, round glasses, open orange jacket over a
# black hoodie, white tee, slim grey jeans, sneakers). Same pivots as the stick figures. ----
SKIN, SKIN_D = "#e8b48e", "#cf9470"
JKT, JKT_D, JKT_DD = "#ee7a2e", "#d4641f", "#b85318"
HOODIE, TEE = "#25211f", "#f6f2ea"
JEANS, JEANS_D, JEANS_L = "#565b64", "#43474f", "#6b717b"
HAIR, HAIR_L, BEARD = "#6a3420", "#9a4f2c", "#4a2618"
INK = "#1d1512"


def cartoon_leg(cls, front):
    c = JEANS if front else JEANS_D
    return (f'<g class="{cls}">'
            f'<path d="M44.4 84 L55.6 84 L54.4 114 L53.6 139 L46.6 139 L45.4 114 Z" fill="{c}"/>'
            f'<path d="M52.6 90 L52 134" stroke="{JEANS_D}" stroke-width=".8" opacity=".6"/>'
            f'<rect x="46.2" y="136.6" width="7.8" height="3" rx=".8" fill="{JEANS_L}"/>'
            f'<path d="M46 139.4 h8 q8.4 1.8 9.6 6.4 l.2 2.2 h-18 z" fill="#2c2a2e"/>'
            f'<path d="M57.4 142.2 q4.6 1.2 6 4.2 l-5.4 0 z" fill="#f4f1ea"/>'
            f'<path d="M45.6 147.6 h18.4 q.6 3 -2.4 3 h-14 q-2.2 0 -2 -3 z" fill="#f4f1ea"/>'
            f'<path d="M50.6 141.6 l3 1.6 M52.6 140.8 l3 1.8" stroke="#f4f1ea" stroke-width=".9" stroke-linecap="round"/></g>')


def cartoon_pocket_arm(side):
    # free arm, hand tucked into the pocket; side = -1 (left of body) or +1
    x = 50 + 13.2 * side
    return (f'<path d="M{x - 2.6 * side} 46.5 Q{x + 4.2 * side} 60 {x + 1.2 * side} 76 L{x - 4.6 * side} 83 '
            f'L{x - 7 * side} 62 Z" fill="{JKT_D}"/>'
            f'<path d="M{x + 1.6 * side} 73.6 L{x - 4 * side} 80.4" stroke="{JKT_DD}" stroke-width="2.6" stroke-linecap="round"/>')


def cartoon_held_arm(d):
    hx = 50 + 28 * d
    return (f'<path d="M{50 + 10.5 * d} 49 Q{50 + 17 * d} 63 {hx - 4.6 * d} 71.4" fill="none" stroke="{JKT}" '
            f'stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M{hx - 7 * d} 69 l{4.6 * d} 4.8" stroke="{JKT_DD}" stroke-width="3.4" stroke-linecap="round"/>'
            f'<circle cx="{hx}" cy="75" r="3.9" fill="{SKIN}"/>')


CARTOON_TORSO = (
    # hood resting behind the neck
    f'<path d="M38.6 45.4 Q50 31.6 61.4 45.4 Q50 50 38.6 45.4 Z" fill="{HOODIE}"/>'
    f'<rect x="47.3" y="32.6" width="5.4" height="10.4" fill="{SKIN_D}"/>'
    # white tee, longest layer
    f'<path d="M43.6 42 H56.4 L57.2 93.4 Q50 95 42.8 93.4 Z" fill="{TEE}"/>'
    f'<path d="M46.4 42 Q50 47.4 53.6 42 Z" fill="{SKIN}"/>'
    # black hoodie, open
    f'<path d="M38.4 45.4 Q42.6 41.2 46.6 42 L47.6 91.6 L37.2 90.4 Z" fill="{HOODIE}"/>'
    f'<path d="M61.6 45.4 Q57.4 41.2 53.4 42 L52.4 91.6 L62.8 90.4 Z" fill="{HOODIE}"/>'
    f'<path d="M46.9 46 L46.6 58 M53.1 46 L53.4 58" stroke="{TEE}" stroke-width=".9" stroke-linecap="round"/>'
    # orange jacket, open over the hoodie
    f'<path d="M35.4 48.4 Q37.6 43.2 43.4 42.6 L44.8 62 L43.8 88.4 Q39 88.6 34.6 87 Z" fill="{JKT}"/>'
    f'<path d="M64.6 48.4 Q62.4 43.2 56.6 42.6 L55.2 62 L56.2 88.4 Q61 88.6 65.4 87 Z" fill="{JKT_D}"/>'
    f'<path d="M43.4 42.6 L45 54.6 L40 47.6 Z" fill="{JKT_DD}"/><path d="M56.6 42.6 L55 54.6 L60 47.6 Z" fill="{JKT_DD}"/>'
    f'<path d="M36.8 73 h5.4 M57.8 73 h5.4" stroke="{JKT_DD}" stroke-width="1.5" stroke-linecap="round"/>'
    f'<path d="M34.7 84.4 Q39 86 43.9 85.8 L43.8 88.4 Q39 88.6 34.6 87 Z" fill="{JKT_DD}"/>'
    f'<path d="M65.3 84.4 Q61 86 56.1 85.8 L56.2 88.4 Q61 88.6 65.4 87 Z" fill="{JKT_DD}"/>'
)

CARTOON_HEAD = (
    f'<circle cx="38.4" cy="23.6" r="2.7" fill="{SKIN_D}"/><circle cx="61.6" cy="23.6" r="2.7" fill="{SKIN_D}"/>'
    f'<path d="M39 20 Q39 9 50 9 Q61 9 61 20 L61 26 Q61 37.6 50 37.6 Q39 37.6 39 26 Z" fill="{SKIN}"/>'
    # full beard with a moustache and a hint of a smile
    f'<path d="M39 22.6 Q38.4 39.6 50 40.4 Q61.6 39.6 61 22.6 Q60 29.6 55.6 29.4 Q50 27.4 44.4 29.4 Q40 29.6 39 22.6 Z" fill="{BEARD}"/>'
    f'<path d="M47.4 32.6 Q50 34.4 52.6 32.6" fill="none" stroke="#e9a48f" stroke-width="1.1" stroke-linecap="round"/>'
    f'<path d="M50 21.4 q-1.9 4 .9 4.6" fill="none" stroke="{SKIN_D}" stroke-width="1.1" stroke-linecap="round"/>'
    # eyes, brows, round glasses
    f'<circle cx="45" cy="21.4" r="1.2" fill="{INK}"/><circle cx="55" cy="21.4" r="1.2" fill="{INK}"/>'
    f'<path d="M41.6 15.6 Q45 13.8 48 15.4 M52 15.4 Q55 13.8 58.4 15.6" fill="none" stroke="{BEARD}" stroke-width="1.6" stroke-linecap="round"/>'
    f'<circle cx="45" cy="21.4" r="4.1" fill="#fff" fill-opacity=".25" stroke="{INK}" stroke-width="1.5"/>'
    f'<circle cx="55" cy="21.4" r="4.1" fill="#fff" fill-opacity=".25" stroke="{INK}" stroke-width="1.5"/>'
    f'<path d="M49.1 21 H50.9 M40.9 20.8 L39 20.2 M59.1 20.8 L61 20.2" stroke="{INK}" stroke-width="1.3" stroke-linecap="round"/>'
    # tall swept quiff with short sides
    f'<path d="M38.6 21 Q36.4 12 41 7.4 Q43.6 1.2 52 1.6 Q60.6 -0.6 64.4 5.4 Q67.4 8.6 63.6 12.4 '
    f'Q63.4 17 61.4 21 Q61.2 14.4 57.4 12.6 Q49 13.8 42.6 12.2 Q39.6 15 38.6 21 Z" fill="{HAIR}"/>'
    f'<path d="M43.6 6.6 Q50 2.4 59.6 4.6 Q52.6 4.8 46.6 9 Z" fill="{HAIR_L}"/>'
    f'<path d="M47.6 10.2 Q54.6 6.8 62 8.6 Q55.4 8.8 50.2 11.4 Z" fill="{HAIR_L}" opacity=".75"/>'
)


def cartoon_human(x_off, direction):
    """The human walker. Legs use the shared walk cycle; one hand holds the AI's, the other is in a pocket."""
    return (f'<g class="walker human cartoon" transform="translate({x_off} 0)">'
            f'<ellipse class="wshadow" cx="50" cy="151" rx="19" ry="2.6"/>'
            f'<g class="bob">{cartoon_leg("leg-b", False)}{cartoon_leg("leg-a", True)}'
            f'{cartoon_pocket_arm(-direction)}{CARTOON_TORSO}{cartoon_held_arm(direction)}{CARTOON_HEAD}</g></g>')


WORDS = ["SAFETY", "ACCOUNTABILITY", "TRUST", "TRANSPARENCY", "FAIRNESS", "DATA PROTECTION",
         "RESPONSIBILITY", "EXPLAINABILITY", "ROBUSTNESS", "HUMAN OVERSIGHT", "INCLUSION"]
RAINBOW = ["#e53935", "#f57c00", "#c99700", "#2e9d4f", "#1e7bd6", "#4b3bb5", "#9b3bb5"]
NEAR_W = 3600  # one loop of signposts; CSS drifts it by this much


def sign_colours(n, seed=4):
    """Every rainbow colour in a random order before any repeats, never twice in a row."""
    import random
    rnd, out = random.Random(seed), []
    while len(out) < n:
        bag = RAINBOW[:]
        rnd.shuffle(bag)
        if out and bag[0] == out[-1]:
            bag.append(bag.pop(0))
        out += bag
    return out[:n]


def half_width(word):
    return 14 + len(word) * 6.3  # half width fits the word


def milestone(x, word, colour="#24170d"):
    hw = half_width(word)
    return (f'<g transform="translate({x} 0)">'
            f'<rect x="-2" y="226" width="4" height="40" rx="2" fill="#5b3a1e"/>'
            f'<rect x="{-hw:.1f}" y="206" width="{2 * hw:.1f}" height="26" rx="5" fill="#fbf6ef" stroke="#24170d" stroke-width="1.6"/>'
            f'<text x="0" y="223.5" text-anchor="middle" class="msign" style="fill:{colour}">{word}</text></g>')


def tufts(x):
    return (f'<path d="M{x} 268 q2 -9 4 0 q2 -12 4 0 q2 -8 4 0" fill="none" stroke="#7b8a3a" '
            f'stroke-width="1.8" stroke-linecap="round"/>')


def near_tile(ox):
    widths = [2 * half_width(w) for w in WORDS]
    gap = (NEAR_W - sum(widths)) / len(WORDS)
    out, x = [], gap / 2
    for word, w, colour in zip(WORDS, widths, sign_colours(len(WORDS))):
        out.append(milestone(ox + x + w / 2, word, colour))
        x += w + gap
    for i, x in enumerate(range(30, NEAR_W, 95)):
        out.append(tufts(ox + x + (i * 37) % 40))
    for i, x in enumerate(range(60, NEAR_W, 140)):
        c = ("#e07a1f", "#3f7d4a", "#c9a03a", "#5b3a1e")[i % 4]
        out.append(f'<ellipse cx="{ox + x + (i * 53) % 60}" cy="{284 + (i * 7) % 10}" rx="4" ry="2.2" fill="{c}" opacity=".55"/>')
    return "".join(out)


def hills_tile(ox):
    return (f'<path d="M{ox} 236 C{ox+90} 214 {ox+180} 214 {ox+260} 228 C{ox+340} 242 {ox+430} 206 {ox+560} 212 '
            f'C{ox+680} 218 {ox+760} 236 {ox+860} 226 C{ox+960} 216 {ox+1060} 210 {ox+1200} 236 L{ox+1200} 250 L{ox} 250 Z" '
            f'fill="#d9c69a"/>'
            + "".join(tree(ox + x, y, sc, k) for x, y, sc, k in
                      [(70, 228, .8, 0), (120, 224, .7, 1), (300, 232, .9, 2), (470, 214, .75, 0), (520, 213, .65, 1),
                       (700, 222, .8, 1), (780, 230, .85, 0), (990, 216, .7, 2), (1100, 222, .8, 0), (1150, 228, .7, 1)]))


def mountains_tile(ox, y0, color, peaks):
    d = f"M{ox} 250 L{ox} {y0}"
    for x, h in peaks:
        d += f" L{ox + x} {y0 - h}"
    d += f" L{ox + 1200} {y0} L{ox + 1200} 250 Z"
    return f'<path d="{d}" fill="{color}"/>'


def snow(ox, peaks, y0):
    out = []
    for x, h in peaks:
        if h > 70:
            px, py = ox + x, y0 - h
            out.append(f'<path d="M{px-9} {py+12} L{px} {py} L{px+9} {py+12} L{px+4} {py+9} L{px} {py+13} L{px-4} {py+9} Z" fill="#f7fbff"/>')
    return "".join(out)


def tree(x, y, s=1.0, kind=0):
    if kind == 0:   # round canopy
        return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-1.2" y="-10" width="2.4" height="10" fill="#6b5236"/>'
                f'<circle cx="0" cy="-14" r="7" fill="#7f9a52"/><circle cx="-4" cy="-11" r="4.5" fill="#738d49"/></g>')
    if kind == 1:   # acacia, flat top
        return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 V-11 M0 -8 L-5 -13 M0 -9 L5 -14" stroke="#6b5236" stroke-width="1.8" fill="none"/>'
                f'<ellipse cx="0" cy="-15" rx="12" ry="3.6" fill="#839c55"/></g>')
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-2.5 0 L-1.8 -12 L1.8 -12 L2.5 0 Z" fill="#7a5d3c"/>'   # baobab
            f'<path d="M-1.8 -12 L-6 -16 M0 -12 L0 -18 M1.8 -12 L6 -16" stroke="#7a5d3c" stroke-width="1.6"/>'
            f'<circle cx="-6" cy="-17" r="3.2" fill="#7f9a52"/><circle cx="0" cy="-19.5" r="3.6" fill="#7f9a52"/><circle cx="6" cy="-17" r="3.2" fill="#7f9a52"/></g>')


def cloud(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M0 22 a14 14 0 0 1 12 -20 a20 20 0 0 1 36 -2 a16 16 0 0 1 26 10 a12 12 0 0 1 2 24 h-70 a10 10 0 0 1 -6 -12 z" fill="#ffffff"/>'
            f'<path d="M4 30 h68 a10 10 0 0 1 -4 4 h-60 a8 8 0 0 1 -4 -4 z" fill="#d7e6f3"/></g>')


def plane(cls, y, s, flip=False):
    tr = f"scale(-1 1)" if flip else ""
    return (f'<g class="plane {cls}"><g transform="translate(0 {y}) scale({s})"><g transform="{tr}">'
            f'<line x1="-70" y1="0" x2="-8" y2="0" stroke="#ffffff" stroke-width="2" stroke-linecap="round" opacity=".85"/>'
            f'<path d="M-8 0 L10 -1.4 Q13 0 10 1.4 Z" fill="#4d5d70"/>'
            f'<path d="M0 -1 L-4 -7 L-1 -7 L4 -1 Z M0 1 L-4 6 L-1 6 L4 1 Z M-7 -0.6 L-9 -4 L-7.5 -4 L-5 -0.6 Z" fill="#4d5d70"/></g></g></g>')


def scene():
    human_x, ai_x = 0, 56          # local offsets; hands meet at local x 78
    walkers = cartoon_human(human_x, +1) + walker("ai", ai_x, -1)
    return f'''<svg class="walkscene" viewBox="0 0 1200 300" preserveAspectRatio="xMidYMax slice" role="img"
     aria-label="A human and an AI walk hand in hand toward a gate with an arrow sign marked Safety and Alignment, passing signposts for safety, trust, accountability, transparency, fairness, data protection, responsibility, explainability, robustness, human oversight and inclusion.">
  <defs>
    <linearGradient id="ws-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb0e3"/><stop offset=".5" stop-color="#b9dcf3"/><stop offset=".8" stop-color="#f3e6d2"/><stop offset="1" stop-color="#f7d9b4"/></linearGradient>
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
    <!-- planes far overhead -->
    {plane("p1", 46, .9)}
    {plane("p2", 26, .6, True)}
    <!-- clouds, two depths -->
    <g class="clouds-far" opacity=".85">{cloud(120, 70, .55)}{cloud(520, 40, .45)}{cloud(820, 86, .5)}{cloud(1320, 70, .55)}{cloud(1720, 40, .45)}{cloud(2020, 86, .5)}</g>
    <g class="clouds">{cloud(60, 96, .95)}{cloud(420, 112, .8)}{cloud(700, 30, .7)}{cloud(1260, 96, .95)}{cloud(1620, 112, .8)}{cloud(1900, 30, .7)}</g>
    <!-- distant mountains -->
    <g class="drift-mtn">{mountains_tile(0, 222, "#b7c9da", [(90, 60), (220, 95), (330, 50), (470, 110), (610, 70), (760, 40), (880, 88), (1020, 56), (1130, 80)])}{snow(0, [(90, 60), (220, 95), (330, 50), (470, 110), (610, 70), (760, 40), (880, 88), (1020, 56), (1130, 80)], 222)}{mountains_tile(1200, 222, "#b7c9da", [(90, 60), (220, 95), (330, 50), (470, 110), (610, 70), (760, 40), (880, 88), (1020, 56), (1130, 80)])}{snow(1200, [(90, 60), (220, 95), (330, 50), (470, 110), (610, 70), (760, 40), (880, 88), (1020, 56), (1130, 80)], 222)}</g>
    <g class="drift-mtn2">{mountains_tile(0, 236, "#9fb4a8", [(40, 30), (160, 48), (280, 26), (420, 54), (560, 34), (700, 58), (840, 30), (980, 50), (1120, 34)])}{mountains_tile(1200, 236, "#9fb4a8", [(40, 30), (160, 48), (280, 26), (420, 54), (560, 34), (700, 58), (840, 30), (980, 50), (1120, 34)])}</g>
    <!-- far hills drift slowly -->
    <g class="drift-far">{hills_tile(0)}{hills_tile(1200)}</g>
    <!-- the destination -->
    <g class="gate">
      <path d="M838 240 V150 Q905 70 972 150 V240" fill="none" stroke="#24170d" stroke-width="8" stroke-linecap="round"/>
      <path d="M838 240 V150 Q905 70 972 150 V240" fill="none" stroke="#e07a1f" stroke-width="3.4" stroke-linecap="round"/>
      <circle cx="905" cy="100" r="5" fill="#e07a1f" stroke="#24170d" stroke-width="2"/>
      <path d="M822 148 H972 L998 169 L972 190 H822 Q816 190 816 184 V154 Q816 148 822 148 Z" fill="#24170d" stroke="#e07a1f" stroke-width="2" stroke-linejoin="round"/>
      <text x="898" y="165" text-anchor="middle" class="gsign">SAFETY &amp;</text>
      <text x="898" y="181" text-anchor="middle" class="gsign">ALIGNMENT</text>
    </g>
    <!-- near ground scrolls at walking pace -->
    <rect y="248" width="1200" height="52" fill="#e6cba6"/>
    <line x1="0" y1="248" x2="1200" y2="248" stroke="#24170d" stroke-width="1.6"/>
    <g class="drift-near">{near_tile(0)}{near_tile(NEAR_W)}</g>
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
