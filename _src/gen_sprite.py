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

SHOULDER = (50, 49)
HIPS = ((46.5, 89), (53.5, 89))
ARM_W = (6.6, 5.4, 4.6)     # shoulder, elbow, wrist
LEG_W = (9.2, 7.6, 6.4)     # hip, knee, ankle


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
    c = add(wrist, d, 4.4)
    out = []
    if kind == "fist":
        out.append(f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="7.2"/>')
    elif kind == "open":  # palm + splayed fingers + thumb
        out.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="7" ry="6.4"/>')
        for ang in (-36, -12, 12, 34):
            b = add(c, rot(d, ang), 5)
            e = add(c, rot(d, ang), 13)
            out.append(seg(b, e, 4, 2.9))
        t = rot(d, 78 * side)
        out.append(seg(add(c, t, 4.5), add(c, t, 11), 4, 3))
    elif kind == "point":
        out.append(f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="6.8"/>')
        out.append(seg(add(c, d, 4), add(c, d, 14), 4.4, 3.4))
    elif kind == "thumb":  # fist with the thumb straight up
        out.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="7" ry="7.6"/>')
        out.append(seg((c[0] - 1, c[1] - 5), (c[0] - 1, c[1] - 15), 5, 3.8))
    elif kind == "palm":  # flat, open, palm up / forward
        out.append(f'<ellipse cx="{f(c[0] + d[0] * 2)}" cy="{f(c[1] + d[1] * 2)}" rx="10" ry="5" '
                   f'transform="rotate({f(math.degrees(math.atan2(d[1], d[0])))} {f(c[0] + d[0] * 2)} {f(c[1] + d[1] * 2)})"/>')
        t = rot(d, -60 * side)
        out.append(seg(add(c, t, 2), add(c, t, 7.5), 3.2, 2.4))
    elif kind == "wall":  # flat hand pressed on a wall: tall narrow mitten
        out.append(f'<ellipse cx="{f(c[0] + 1)}" cy="{f(c[1])}" rx="5" ry="9.5"/>')
    return "".join(out)


def shoe(ankle, toe):
    t = unit((0, 0), toe)
    c = add(ankle, t, 7.5)
    ang = math.degrees(math.atan2(t[1], t[0]))
    return (f'<ellipse cx="{f(c[0])}" cy="{f(c[1] + 1)}" rx="13.5" ry="5.8" '
            f'transform="rotate({f(ang if abs(ang) < 90 else ang - 180)} {f(c[0])} {f(c[1] + 1)})"/>')


TORSO = ("M48 42 C46.4 52 43.8 64 43 77 C42.6 85 43.8 90 45.6 92.5 L54.4 92.5 "
         "C56.2 90 57.4 85 57 77 C56.2 64 53.6 52 52 42 Z")


def figure(pose):
    la, ra, ll, rl = pose
    parts = [f'<path d="{TORSO}"/>']
    for (knee, ankle, toe), hip in ((ll, HIPS[0]), (rl, HIPS[1])):
        parts.append(seg(hip, knee, LEG_W[0], LEG_W[1]) + seg(knee, ankle, LEG_W[1], LEG_W[2]) + shoe(ankle, toe))
    for (elbow, wrist, kind), side in ((la, -1), (ra, 1)):
        parts.append(seg(SHOULDER, elbow, ARM_W[0], ARM_W[1]) + seg(elbow, wrist, ARM_W[1], ARM_W[2]) + hand(elbow, wrist, kind, side))
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
}

HEADS = {
    "human": '<circle cx="50" cy="22" r="19" fill="#fffaf3" stroke="currentColor" stroke-width="2.3"/>',
    "mask": ('<circle cx="50" cy="22" r="19" fill="#fffaf3" stroke="currentColor" stroke-width="2.3"/>'
             '<rect x="31.5" y="14" width="37" height="11" rx="5.5" fill="currentColor"/>'
             '<circle cx="44" cy="20" r="2.4" fill="#fffaf3"/><circle cx="56" cy="20" r="2.4" fill="#fffaf3"/>'),
    "ai": ('<path d="M50 8 V3.5" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
           '<circle cx="50" cy="3" r="3" fill="currentColor"/>'
           '<rect x="34" y="8" width="32" height="31" rx="9" fill="#fffaf3" stroke="currentColor" stroke-width="2.3"/>'
           '<circle cx="44" cy="21" r="3" fill="#24170d"/><circle cx="56" cy="21" r="3" fill="#24170d"/>'
           '<path d="M44.5 29 Q50 33.5 55.5 29" fill="none" stroke="#24170d" stroke-width="2.4" stroke-linecap="round"/>'),
    "ai-sad": ('<path d="M50 8 V3.5" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
               '<circle cx="50" cy="3" r="3" fill="currentColor"/>'
               '<rect x="34" y="8" width="32" height="31" rx="9" fill="#fffaf3" stroke="currentColor" stroke-width="2.3"/>'
               '<circle cx="44" cy="21" r="3" fill="#24170d"/><circle cx="56" cy="21" r="3" fill="#24170d"/>'
               '<path d="M44.5 32 Q50 27.5 55.5 32" fill="none" stroke="#24170d" stroke-width="2.4" stroke-linecap="round"/>'),
}


def main() -> None:
    sym = []
    for name, pose in POSES.items():
        sym.append(f'<symbol id="b-{name}" viewBox="0 0 100 160" overflow="visible">'
                   f'<g fill="currentColor">{figure(pose)}</g></symbol>')
    for name, svg in HEADS.items():
        sym.append(f'<symbol id="h-{name}" viewBox="0 0 100 160" overflow="visible">{svg}</symbol>')
    OUT.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" '
                   'aria-hidden="true" focusable="false">\n<!-- generated by _src/gen_sprite.py -->\n<defs>\n'
                   + "\n".join(sym) + "\n</defs>\n</svg>\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(POSES)} poses, {len(HEADS)} heads)")


if __name__ == "__main__":
    main()
