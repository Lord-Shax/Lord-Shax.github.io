"""Generate the stick-figure library (_src/partials/sprite.svg).

    python _src/gen_sprite.py

Style: thin-outlined round head, slim tapered torso, limbs drawn as tapered
shapes (thick at the body, thinner at hands and feet), mitten hands (open,
fist, pointing, thumb-up, flat palm) and long oval shoes. Bodies use
currentColor so CSS sets the colour. Canvas is 100 x 160.

A pose is two arms and two legs. An arm is (elbow, wrist, hand); a leg is
(knee, ankle, toe direction). Add poses to POSES and re-run.
"""

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent / "partials" / "sprite.svg"

SHOULDER = (50, 48)
HIPS = ((47.6, 89), (52.4, 89))
ARM_W = (4.6, 3.7, 3.1)     # shoulder, elbow, wrist
LEG_W = (6.2, 5.0, 4.2)     # hip, knee, ankle


def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def seg(a, b, wa, wb):
    """Tapered segment from a (width wa) to b (width wb) as a filled quad, rounded joints."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    p = [(a[0] + nx * wa / 2, a[1] + ny * wa / 2), (b[0] + nx * wb / 2, b[1] + ny * wb / 2),
         (b[0] - nx * wb / 2, b[1] - ny * wb / 2), (a[0] - nx * wa / 2, a[1] - ny * wa / 2)]
    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in p) + "Z"
    return (f'<path d="{d}"/><circle cx="{f(a[0])}" cy="{f(a[1])}" r="{f(wa / 2)}"/>'
            f'<circle cx="{f(b[0])}" cy="{f(b[1])}" r="{f(wb / 2)}"/>')


def limb(a, b, c, w0, w1, w2, n=18):
    """One smooth tapered limb: a quadratic curve that passes through a, b and c,
    with width easing from w0 (root) through w1 (joint) to w2 (end)."""
    P = (2 * b[0] - (a[0] + c[0]) / 2, 2 * b[1] - (a[1] + c[1]) / 2)
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * P[0] + t * t * c[0]
        y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * P[1] + t * t * c[1]
        dx = 2 * (1 - t) * (P[0] - a[0]) + 2 * t * (c[0] - P[0])
        dy = 2 * (1 - t) * (P[1] - a[1]) + 2 * t * (c[1] - P[1])
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        u = t * 2
        w = (w0 + (w1 - w0) * u) if u <= 1 else (w1 + (w2 - w1) * (u - 1))
        left.append((x + nx * w / 2, y + ny * w / 2))
        right.append((x - nx * w / 2, y - ny * w / 2))
    pts = left + right[::-1]
    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"
    return (f'<path d="{d}"/><circle cx="{f(a[0])}" cy="{f(a[1])}" r="{f(w0 / 2)}"/>'
            f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(w2 / 2)}"/>')


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    return dx / L, dy / L


def rot(v, deg):
    r = math.radians(deg)
    return v[0] * math.cos(r) - v[1] * math.sin(r), v[0] * math.sin(r) + v[1] * math.cos(r)


def add(p, v, k):
    return p[0] + v[0] * k, p[1] + v[1] * k


def hand(elbow, wrist, kind, side):
    """side = -1 for the figure's left (viewer's left), +1 for right; used to place thumbs."""
    d = unit(elbow, wrist)
    c = add(wrist, d, 3.2)
    out = []
    if kind == "fist":
        out.append(f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="4.7"/>')
    elif kind == "open":  # small palm, four fine splayed fingers, thumb
        out.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="4.6" ry="4.2"/>')
        for ang in (-34, -11, 11, 32):
            out.append(seg(add(c, rot(d, ang), 3.4), add(c, rot(d, ang), 9.6), 2.3, 1.5))
        t = rot(d, 78 * side)
        out.append(seg(add(c, t, 3), add(c, t, 7.6), 2.3, 1.7))
    elif kind == "point":
        out.append(f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="4.4"/>')
        out.append(seg(add(c, d, 2.6), add(c, d, 10.5), 2.7, 2))
    elif kind == "thumb":
        out.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="4.6" ry="5"/>')
        out.append(seg((c[0] - .6, c[1] - 3.4), (c[0] - .6, c[1] - 10.5), 3, 2.2))
    elif kind == "palm":
        cx, cy = c[0] + d[0] * 1.6, c[1] + d[1] * 1.6
        out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="7" ry="3.3" '
                   f'transform="rotate({f(math.degrees(math.atan2(d[1], d[0])))} {f(cx)} {f(cy)})"/>')
        t = rot(d, -60 * side)
        out.append(seg(add(c, t, 1.6), add(c, t, 5.6), 2.2, 1.6))
    elif kind == "wall":
        out.append(f'<ellipse cx="{f(c[0] + 1)}" cy="{f(c[1])}" rx="3.4" ry="6.6"/>')
    return "".join(out)


def shoe(ankle, toe):
    t = unit((0, 0), toe)
    c = add(ankle, t, 5.2)
    ang = math.degrees(math.atan2(t[1], t[0]))
    return (f'<ellipse cx="{f(c[0])}" cy="{f(c[1] + 1)}" rx="9.4" ry="3.6" '
            f'transform="rotate({f(ang if abs(ang) < 90 else ang - 180)} {f(c[0])} {f(c[1] + 1)})"/>')


TORSO = ("M48.7 41 C47.4 52 45.4 64 45 77 C44.7 85 45.6 90 47 92 L53 92 "
         "C54.4 90 55.3 85 55 77 C54.6 64 52.6 52 51.3 41 Z")


SKIRT = "M46 76 C43.5 88 38 101 33 111 Q50 116 67 111 C62 101 56.5 88 54 76 Z"


def figure(pose, skirt=False):
    la, ra, ll, rl = pose
    feet_y = max(ll[1][1], rl[1][1])
    parts = [f'<ellipse cx="50" cy="{f(feet_y + 6.5)}" rx="21" ry="2.4" opacity=".13"/>', f'<path d="{TORSO}"/>',
             '<path d="M48.4 47 C47.3 57 46.4 67 46.2 77" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1.3" stroke-linecap="round"/>']
    for (knee, ankle, toe), hip in ((ll, HIPS[0]), (rl, HIPS[1])):
        parts.append(limb(hip, knee, ankle, *LEG_W) + shoe(ankle, toe))
    for (elbow, wrist, kind), side in ((la, -1), (ra, 1)):
        parts.append(limb(SHOULDER, elbow, wrist, *ARM_W) + hand(elbow, wrist, kind, side))
    if skirt:
        parts.insert(2, f'<path d="{SKIRT}"/>')
    return "".join(parts)


# Legs that come up often
LEGS = {
    "stand": (((44, 117), (43, 144), (-1, .08)), ((56, 117), (57, 144), (1, .08))),
    "apart": (((40, 116), (35, 144), (-1, .1)), ((60, 116), (65, 144), (1, .1))),
    "cross": (((52, 118), (58, 144), (1, .05)), ((49, 117), (44, 144), (-1, .05))),
}
L_DOWN = ((42, 70), (39, 88), "fist")
R_DOWN = ((58, 70), (61, 88), "fist")
L_HIP = ((33, 66), (44, 82), "fist")
R_HIP = ((67, 66), (56, 82), "fist")

POSES = {
    "stand":   (L_DOWN, R_DOWN, *LEGS["stand"]),
    "cheer":   (((31, 40), (18, 19), "open"), ((69, 40), (82, 19), "open"), *LEGS["apart"]),
    "point":   (L_HIP, ((67, 54), (83, 51), "point"), *LEGS["apart"]),
    "think":   (((38, 70), (55, 75), "fist"), ((67, 70), (60, 49), "fist"), *LEGS["stand"]),
    "jump":    (((32, 38), (24, 18), "fist"), ((68, 40), (80, 24), "fist"),
                ((34, 106), (41, 126), (-1, .35)), ((66, 102), (71, 123), (1, .45))),
    "run":     (((38, 64), (27, 53), "fist"), ((63, 66), (77, 58), "fist"),
                ((37, 110), (21, 118), (-.5, .9)), ((63, 114), (60, 143), (1, .05))),
    "present": (L_DOWN, ((66, 70), (84, 68), "palm"), *LEGS["stand"]),
    "thumbs":  (((33, 70), (31, 55), "thumb"), ((67, 70), (69, 55), "thumb"), *LEGS["stand"]),
    "shrug":   (((32, 65), (20, 58), "palm"), ((68, 65), (80, 58), "palm"), *LEGS["stand"]),
    "reach":   (L_DOWN, ((62, 31), (70, 12), "open"), *LEGS["stand"]),
    "sneak":   (((57, 63), (72, 59), "fist"), ((62, 75), (79, 75), "fist"),
                ((37, 113), (42, 143), (-1, .05)), ((66, 113), (62, 144), (1, .05))),
    "shake":   (L_DOWN, ((67, 70), (88, 66), "fist"), *LEGS["stand"]),
    "wave":    (L_DOWN, ((70, 42), (76, 22), "open"), *LEGS["stand"]),
    "hips":    (L_HIP, R_HIP, *LEGS["apart"]),
    "lean":    (L_HIP, ((69, 47), (86, 45), "wall"), *LEGS["cross"]),
    "thumbup": (L_HIP, ((74, 58), (78, 40), "thumb"), *LEGS["apart"]),
    # dancing in a circle, hands linked with neighbours
    "dance-a": (((30, 60), (14, 66), "fist"), ((70, 60), (86, 66), "fist"),
                ((38, 108), (40, 130), (-1, .25)), ((55, 118), (58, 144), (1, .08))),
    "dance-b": (((30, 58), (14, 62), "fist"), ((70, 62), (86, 68), "fist"),
                ((45, 118), (42, 144), (-1, .08)), ((62, 108), (60, 130), (1, .25))),
    # writing on a board, chalk raised
    "write":   (L_DOWN, ((70, 52), (84, 36), "fist"), *LEGS["apart"]),
}
SKIRTED = {"dance-a-w": "dance-a", "dance-b-w": "dance-b", "stand-w": "stand"}

# The letters "AI" are the robot's hair. Centred on x=50, so a mirrored figure can reuse it unflipped.
HAIR_AI = ('<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M40.9 6.6 L44.5 -2.6 Q45.5 -5 46.5 -2.6 L50.1 6.6 M42.5 2.6 H48.5 M56.4 -3.6 V6.6 M54 -3.6 H58.8 M54 6.6 H58.8" '
           'stroke="#fffaf3" stroke-width="5"/>'
           '<path d="M40.9 6.6 L44.5 -2.6 Q45.5 -5 46.5 -2.6 L50.1 6.6 M42.5 2.6 H48.5 M56.4 -3.6 V6.6 M54 -3.6 H58.8 M54 6.6 H58.8" '
           'stroke="#120b06" stroke-width="2.5"/></g>')

HEADS = {
    "human": ('<circle cx="50" cy="24.5" r="16" fill="#fffaf3" stroke="currentColor" stroke-width="2"/>'
             '<circle cx="40.6" cy="29.4" r="2.6" fill="#e07a1f" opacity=".22"/><circle cx="59.4" cy="29.4" r="2.6" fill="#e07a1f" opacity=".22"/>'
             '<circle cx="45" cy="24.6" r="1.65" fill="#24170d"/><circle cx="55" cy="24.6" r="1.65" fill="#24170d"/>'
             '<path d="M46.4 30.2 Q50 33.4 53.6 30.2" fill="none" stroke="#24170d" stroke-width="1.5" stroke-linecap="round"/>'),
    "mask": ('<circle cx="50" cy="24.5" r="16" fill="#fffaf3" stroke="currentColor" stroke-width="2"/>'
             '<rect x="34.5" y="17.5" width="31" height="8.5" rx="4.25" fill="currentColor"/>'
             '<circle cx="44.5" cy="21.8" r="1.9" fill="#fffaf3"/><circle cx="55.5" cy="21.8" r="1.9" fill="#fffaf3"/>'),
    "gele": ('<circle cx="50" cy="24.5" r="16" fill="#fffaf3" stroke="currentColor" stroke-width="2"/>'
             '<path d="M32 21 C30.5 7 69.5 7 68 21 C63 15.5 37 15.5 32 21 Z" fill="#e07a1f" stroke="currentColor" stroke-width="1.6"/>'
             '<path d="M39.5 12 C37 -3 61.5 -8 66.5 6 C61.5 1.5 51.5 -.5 46.5 5 C44 7 41.5 9.5 39.5 12 Z" fill="#e07a1f" stroke="currentColor" stroke-width="1.6"/>'
             '<path d="M45.5 5 C49 -1 57.5 -3 62 1.5 M36 14.5 C45 11 55 11 64 14.5" fill="none" stroke="#24170d" stroke-width="1.1" opacity=".45"/>'
             '<circle cx="40.6" cy="29.4" r="2.6" fill="#e07a1f" opacity=".22"/><circle cx="59.4" cy="29.4" r="2.6" fill="#e07a1f" opacity=".22"/>'
             '<circle cx="45" cy="24.6" r="1.65" fill="#24170d"/><circle cx="55" cy="24.6" r="1.65" fill="#24170d"/>'
             '<path d="M46.4 30.2 Q50 33.4 53.6 30.2" fill="none" stroke="#24170d" stroke-width="1.5" stroke-linecap="round"/>'),
    "ai": (           '<rect x="36" y="11.5" width="28" height="27" rx="8" fill="#fffaf3" stroke="currentColor" stroke-width="2.2"/>'
           '<circle cx="44.6" cy="23" r="2.4" fill="#24170d"/><circle cx="55.4" cy="23" r="2.4" fill="#24170d"/>'
           '<path d="M45.4 30 Q50 33.6 54.6 30" fill="none" stroke="#24170d" stroke-width="1.9" stroke-linecap="round"/>'),
    "ai-sad": (               '<rect x="36" y="11.5" width="28" height="27" rx="8" fill="#fffaf3" stroke="currentColor" stroke-width="2.2"/>'
               '<circle cx="44.6" cy="23" r="2.4" fill="#24170d"/><circle cx="55.4" cy="23" r="2.4" fill="#24170d"/>'
               '<path d="M45.4 32.4 Q50 28.8 54.6 32.4" fill="none" stroke="#24170d" stroke-width="1.9" stroke-linecap="round"/>'),
}


def main() -> None:
    sym = []
    for name, pose in POSES.items():
        sym.append(f'<symbol id="b-{name}" viewBox="0 0 100 160" overflow="visible">'
                   f'<g fill="currentColor">{figure(pose)}</g></symbol>')
    for name, base in SKIRTED.items():
        sym.append(f'<symbol id="b-{name}" viewBox="0 0 100 160" overflow="visible">'
                   f'<g fill="currentColor">{figure(POSES[base], skirt=True)}</g></symbol>')
    for name in ("ai", "ai-sad"):
        HEADS[name + "-bare"] = HEADS[name]
        HEADS[name] = HAIR_AI + HEADS[name]
    HEADS["hair-ai"] = HAIR_AI
    for name, svg in HEADS.items():
        sym.append(f'<symbol id="h-{name}" viewBox="0 0 100 160" overflow="visible">{svg}</symbol>')
    OUT.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" '
                   'aria-hidden="true" focusable="false">\n<!-- generated by _src/gen_sprite.py -->\n<defs>\n'
                   + "\n".join(sym) + "\n</defs>\n</svg>\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(POSES)} poses, {len(HEADS)} heads)")


if __name__ == "__main__":
    main()
