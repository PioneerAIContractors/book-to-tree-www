"""Draw variant C's hand-drawn SVG art and write it into ../index.html between the
<!-- art -->, <!-- check --> and <!-- sapling --> markers. The page itself stays static.

The art is drawn for whatever is in sample/. It is currently image 60 of the Daughters of
Founders and Patriots lineage book: Miss Lucy Palmer Butler and the Williams line she
descends from. Everything page-specific is a constant below -- the people (PEOPLE), the
subject's tag (SUBJECT), the entry's position on sample/page.jpg (FAMILY), and the line the
check illustration circles (CHECK_*). When sample/ is replaced again, update those to match
the new page and re-run:  python3 _src/gen_art_c.py

THE LABELS MUST FOLLOW THE FILES. Swapping sample/ and leaving these alone is not a cosmetic
mismatch: the check illustration then circles a real line on a real page and labels it with a
person who does not exist, which is the one claim this section of the page exists to deny.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]

BRANCH = "#86684e"
LEAVES = ["#8fa984", "#a7bd9a", "#7c9771"]
MIDRIB = "#5e7a55"
PENCIL = "#c0623f"          # terracotta pencil marks (illustration only)
TAG_FILL = "#fffdf8"
TAG_STROKE = "#c9d5bd"
HILITE = "#e2ebc4"

PEOPLE = [("Charles Butler", "1803-1878"), ("Lucy C. Williams", "1809-1891"),
          ("William Williams", "1772-1810"), ("Lydia Wheeler", "1778-1811"),
          ("Lieut. John Williams", "1744-1813"), ("Keturah Randall", "1748-1810")]
KIDS = PEOPLE                      # the tag row; ancestors here, children in another book
SUBJECT = [("Lucy Palmer Butler", "t-couple"), ("b. New London, Conn.", "t-note"),
           ("nine generations", "t-note")]

PAGE_W, PAGE_H = 900, 1434
FAMILY = (218, 238, 812, 812)   # the Butler entry and its Williams line, in page.jpg pixels
# "4. Lieut. John Williams (Dec. 23, 1744-Sept. 10, 1813)" -- the man the check art circles,
# and the one whose birth PLACE the extractor took from the prose at the foot of the page.
CHECK_CROP = (215, 440, 815, 600)
CHECK_LINE = (220, 800, 510, 530)
CHECK_TAG = [("Lieut. John Williams", "t-name", 20, 30), ("b. 23 Dec., 1744", "t-note", 17, 54)]


def n(v: float) -> str:
    s = f"{v:.1f}"
    if s.endswith(".0"):
        s = s[:-2]
    return "0" if s == "-0" else s


def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    mt = 1 - t
    a, b, c, d = mt ** 3, 3 * mt * mt * t, 3 * mt * t * t, t ** 3
    return a * x0 + b * x1 + c * x2 + d * x3, a * y0 + b * y1 + c * y2 + d * y3


def bez_d(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    mt = 1 - t
    return (3 * mt * mt * (x1 - x0) + 6 * mt * t * (x2 - x1) + 3 * t * t * (x3 - x2),
            3 * mt * mt * (y1 - y0) + 6 * mt * t * (y2 - y1) + 3 * t * t * (y3 - y2))


def angle_at(p, t):
    dx, dy = bez_d(p, t)
    return math.degrees(math.atan2(dy, dx))


def tapered(p, w0, w1, steps=30, fill=BRANCH):
    """A branch drawn as a filled shape that thins from w0 to w1, with a round tip."""
    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        x, y = bez(p, t)
        dx, dy = bez_d(p, t)
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length, dx / length
        w = (w0 + (w1 - w0) * t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    d = "M" + " ".join(f"{n(x)} {n(y)}" for x, y in pts) + "Z"
    ex, ey = bez(p, 1)
    sx, sy = bez(p, 0)
    return (f'<path d="{d}" fill="{fill}"/>'
            f'<circle cx="{n(ex)}" cy="{n(ey)}" r="{n(w1 / 2)}" fill="{fill}"/>'
            f'<circle cx="{n(sx)}" cy="{n(sy)}" r="{n(w0 / 2)}" fill="{fill}"/>')


def leaf(x, y, ang, length=20.0, width=9.0, fill=LEAVES[0], rib=True):
    """An almond leaf whose stalk sits at (x, y), pointing along ang degrees."""
    w = width / 2
    a, b, L = length * 0.22, length * 0.62, length
    d = (f"M0 0C{n(a)} {n(-w * 1.15)} {n(b)} {n(-w * 1.1)} {n(L)} 0"
         f"C{n(b)} {n(w * 1.1)} {n(a)} {n(w * 1.15)} 0 0Z")
    rib_s = (f'<path d="M1.5 0H{n(L * 0.78)}" stroke="{MIDRIB}" stroke-width="1" '
             f'stroke-linecap="round" opacity=".5"/>') if rib else ""
    return (f'<g transform="translate({n(x)} {n(y)}) rotate({n(ang)})">'
            f'<path d="{d}" fill="{fill}"/>{rib_s}</g>')


def leaves_on(p, spec):
    """spec: list of (t, side, length, colour index). side +1 = left of travel, -1 = right."""
    out = []
    for t, side, length, ci in spec:
        x, y = bez(p, t)
        out.append(leaf(x, y, angle_at(p, t) - side * 42, length, length * 0.44, LEAVES[ci % 3]))
    return "".join(out)


def brace(x0, y0, y1, d, width=2.8):
    ym = (y0 + y1) / 2
    r = min(18, (y1 - y0) / 6)
    path = (f"M{n(x0)} {n(y0)}Q{n(x0 + d)} {n(y0)} {n(x0 + d)} {n(y0 + r)}"
            f"L{n(x0 + d)} {n(ym - r)}Q{n(x0 + d)} {n(ym)} {n(x0 + 2 * d)} {n(ym)}"
            f"Q{n(x0 + d)} {n(ym)} {n(x0 + d)} {n(ym + r)}L{n(x0 + d)} {n(y1 - r)}"
            f"Q{n(x0 + d)} {n(y1)} {n(x0)} {n(y1)}")
    return (f'<path d="{path}" fill="none" stroke="{PENCIL}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def defs(pre):
    return (
        "<defs>"
        f'<filter id="{pre}-rough" x="-5%" y="-5%" width="110%" height="110%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/>'
        '<feDisplacementMap in="SourceGraphic" scale="2.4" xChannelSelector="R" yChannelSelector="G"/>'
        "</filter>"
        f'<filter id="{pre}-lift" x="-15%" y="-25%" width="130%" height="170%">'
        '<feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#3b2d1e" flood-opacity=".13"/>'
        "</filter>"
        f'<filter id="{pre}-paper" x="-15%" y="-20%" width="130%" height="170%">'
        '<feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#3b2d1e" flood-opacity=".17"/>'
        "</filter>"
        "</defs>"
    )


def page(pre, x, y, w, highlight_pad=4):
    s = w / PAGE_W
    h = PAGE_H * s
    fx0, fy0, fx1, fy1 = FAMILY
    hx0, hy0 = x + fx0 * s - highlight_pad, y + fy0 * s - highlight_pad
    hx1, hy1 = x + fx1 * s + highlight_pad, y + fy1 * s + highlight_pad
    clip = f"{pre}-clip"
    return (
        f'<clipPath id="{clip}"><rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="6"/></clipPath>'
        f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="6" fill="#fff" filter="url(#{pre}-paper)"/>'
        f'<image href="sample/page.jpg" x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" '
        f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip})"/>'
        f'<rect x="{n(hx0)}" y="{n(hy0)}" width="{n(hx1 - hx0)}" height="{n(hy1 - hy0)}" rx="8" '
        f'fill="{HILITE}" opacity=".8" style="mix-blend-mode:multiply"/>'
    ), (y + fy0 * s, y + fy1 * s, x + w, h)


def tag(pre, x, y, w, h, lines, rx=16, stroke=TAG_STROKE, stroke_w=1.5, glyph=False, pad=16, delay=None):
    """lines: list of (text, css class, font size, baseline offset from top)."""
    out = ["<g>"]
    out += [f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" fill="{TAG_FILL}" '
           f'stroke="{stroke}" stroke-width="{stroke_w}" filter="url(#{pre}-lift)"/>']
    tx = x + pad
    if glyph:
        out.append(leaf(x + 13, y + h / 2 + 7, -58, 17, 8, LEAVES[2], rib=False))
        tx = x + 34
    for text, cls, size, base in lines:
        out.append(f'<text x="{n(tx)}" y="{n(y + base)}" class="{cls}" font-size="{n(size)}" '
                   f'data-maxx="{n(x + w - 8)}">{text}</text>')
    out.append("</g>")
    return "".join(out)


# ---------------------------------------------------------------- hero, wide (desktop)
def hero_wide():
    pre = "aw"
    VB_W, VB_H = 1000, 544
    parts, branches, leafs = [], [], []
    page_svg, (fam_top, fam_bot, page_right, _) = page(pre, 18, 14, 336)
    parts.append(page_svg)

    bx0 = page_right + 10
    ym = (fam_top + fam_bot) / 2
    parts_brace = brace(bx0, fam_top - 2, fam_bot + 2, 10)
    tip = (bx0 + 20 + 2, ym)

    # the children, in a column on the right, in birth order
    kw, kh, gap = 200, 58, 22
    col_top = (VB_H - (6 * kh + 5 * gap)) / 2
    tops = [col_top + k * (kh + gap) for k in range(6)]
    mids = [t + kh / 2 for t in tops]
    offs = [26, 6, 0, 0, 6, 26]
    kx = 764

    cw, ch = 206, 100
    cx = 446
    c_mid = (mids[2] + mids[3]) / 2
    cy = c_mid - ch / 2
    main = [tip, (tip[0] + 32, tip[1]), (cx - 34, c_mid), (cx + 2, c_mid)]
    branches.append(tapered(main, 7.5, 5))
    leafs.append(leaves_on(main, [(0.3, 1, 24, 0), (0.58, -1, 21, 2)]))

    fork = (cx + cw + 22, c_mid)
    branches.append(tapered([(cx + cw - 2, c_mid), (cx + cw + 6, c_mid), (fork[0] - 6, c_mid), fork], 5.6, 5.2))

    def t_at_y(curve, y):
        lo, hi = 0.0, 1.0                      # the boughs are monotonic in y
        up_dir = bez(curve, 1)[1] < bez(curve, 0)[1]
        for _ in range(40):
            mid_t = (lo + hi) / 2
            if (bez(curve, mid_t)[1] > y) == up_dir:
                lo = mid_t
            else:
                hi = mid_t
        return (lo + hi) / 2

    kid_tags = []
    xs = [kx + o for o in offs]
    # two boughs sweep out to the eldest and youngest; the others leave them on short twigs
    for group, sgn in (((0, 1, 2), -1), ((5, 4, 3), 1)):
        outer = group[0]
        bough = [fork, (fork[0] + 56, c_mid), (xs[outer] - 96, mids[outer]), (xs[outer] + 2, mids[outer])]
        branches.append(tapered(bough, 5.2, 2.4))
        leafs.append(leaves_on(bough, [(0.22, sgn, 19, 0), (0.5, -sgn, 18, 1), (0.74, sgn, 17, 2)]))
        for k in group[1:]:
            t0 = t_at_y(bough, mids[k] - sgn * (30 if k in (1, 4) else 18))
            bx, by = bez(bough, t0)
            dx, dy = bez_d(bough, t0)
            ln = math.hypot(dx, dy)
            twig = [(bx, by), (bx + dx / ln * 14, by + dy / ln * 14), (xs[k] - 30, mids[k]), (xs[k] + 2, mids[k])]
            branches.append(tapered(twig, 3.2, 1.9))
            leafs.append(leaves_on(twig, [(0.62, -sgn, 15, k)]))
    for k, (name, born) in enumerate(KIDS):
        kid_tags.append(tag(pre, xs[k], tops[k], kw, kh,
                            [(name, "t-name", 19, 25.5), (born, "t-note", 15.5, 46.5)],
                            rx=18, glyph=True, delay=round(1.0 + 0.07 * k, 2)))
    leafs.append(leaf(fork[0] - 6, c_mid - 3, -116, 18, 8, LEAVES[0]))
    leafs.append(leaf(fork[0] - 6, c_mid + 3, 116, 18, 8, LEAVES[2]))
    couple = tag(pre, cx, cy, cw, ch,
                 [(SUBJECT[0][0], SUBJECT[0][1], 20, 35), (SUBJECT[1][0], SUBJECT[1][1], 16, 61),
                  (SUBJECT[2][0], SUBJECT[2][1], 15, 86)],
                 rx=22, stroke=PENCIL, stroke_w=2, pad=18, delay=0.55)

    svg = (
        f'<svg class="art-wide" viewBox="0 0 {VB_W} {VB_H}" role="img" aria-labelledby="aw-t">'
        f'<title id="aw-t">A scanned page from a real book, with one family\'s entry marked on it and a small '
        f'family tree growing out of it: {SUBJECT[0][0]}, {SUBJECT[1][0]}, and the line she descends from — '
        + ", ".join(f"{nm} {yr}" for nm, yr in PEOPLE) + '.</title>'
        + defs(pre) + "".join(parts)
        + f'<g filter="url(#{pre}-rough)">{parts_brace}{"".join(branches)}{"".join(leafs)}</g>'
        + couple + "".join(kid_tags) + "</svg>"
    )
    return svg


# ---------------------------------------------------------------- hero, tall (phones)
def hero_tall():
    pre = "at"
    VB_W, VB_H = 340, 494
    parts, branches, leafs = [], [], []
    page_svg, (fam_top, fam_bot, page_right, page_h) = page(pre, 4, 4, 146, highlight_pad=3)
    parts.append(page_svg)

    bx0 = page_right + 6
    ym = (fam_top + fam_bot) / 2
    parts_brace = brace(bx0, fam_top - 1, fam_bot + 1, 6.5, width=2.4)
    tip = (bx0 + 13 + 2, ym)

    cx, cy, cw, ch = 172, 122, 166, 82
    main = [tip, (tip[0] + 24, tip[1]), (cx + 40, cy - 30), (cx + 50, cy + 1)]
    branches.append(tapered(main, 5.6, 3.8))
    leafs.append(leaves_on(main, [(0.38, 1, 17, 0), (0.7, -1, 15, 2)]))

    stem_top = (cx + cw / 2, cy + ch - 1)
    s1 = [stem_top, (stem_top[0], stem_top[1] + 26), (170, 220), (170, 252)]
    s2 = [(170, 252), (166, 326), (174, 404), (170, 482)]
    branches.append(tapered(s1, 4.6, 3.8))
    branches.append(tapered(s2, 3.8, 2.0))

    kw, kh = 156, 52
    kid_tags = []
    for k, (name, born) in enumerate(KIDS):
        left = k % 2 == 0
        top = 256 + (k // 2) * 72 + (0 if left else 36)
        mid = top + kh / 2
        x = 1 if left else VB_W - 1 - kw
        edge = x + kw if left else x
        twig = [(170, mid - 14), (170, mid - 4), (edge + (6 if left else -6), mid), (edge + (-1 if left else 1), mid)]
        branches.append(tapered(twig, 2.6, 1.8))
        kid_tags.append(tag(pre, x, top, kw, kh,
                            [(name, "t-name", 16, 23), (born, "t-note", 14, 41.5)],
                            rx=14, glyph=False, pad=12, delay=round(0.85 + 0.1 * k, 2)))
    # leaves along the stem, between the tags
    for t, side, ci in [(0.12, 1, 0), (0.34, -1, 1), (0.5, 1, 2), (0.66, -1, 0), (0.86, 1, 1)]:
        x, y = bez(s2, t)
        leafs.append(leaf(x, y, angle_at(s2, t) - side * 40, 15, 6.6, LEAVES[ci]))
    couple = tag(pre, cx, cy, cw, ch,
                 [(SUBJECT[0][0], SUBJECT[0][1], 16.5, 28), (SUBJECT[1][0], SUBJECT[1][1], 14, 49),
                  ("married 1806", "t-note", 14, 69.5)],
                 rx=18, stroke=PENCIL, stroke_w=2, pad=12, delay=0.5)

    svg = (
        f'<svg class="art-tall" viewBox="0 0 {VB_W} {VB_H}" role="img" aria-labelledby="at-t">'
        f'<title id="at-t">A scanned page from a real book, with one family\'s entry marked on it and a small '
        f'family tree growing out of it: {SUBJECT[0][0]}, {SUBJECT[1][0]}, and the line she descends from — '
        + ", ".join(f"{nm} {yr}" for nm, yr in PEOPLE) + '.</title>'
        + defs(pre) + "".join(parts)
        + f'<g filter="url(#{pre}-rough)">{parts_brace}{"".join(branches)}{"".join(leafs)}</g>'
        + couple + "".join(kid_tags) + "</svg>"
    )
    return svg


# ---------------------------------------------------------------- "check it" illustration
def pencil_loop(cx, cy, rx, ry, start=200, sweep=395, wobble=0.035, steps=40):
    pts = []
    for i in range(steps + 1):
        a = math.radians(start + sweep * i / steps)
        k = 1 + wobble * math.sin(3.1 * a) + (0.06 * i / steps)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    d = f"M{n(pts[0][0])} {n(pts[0][1])}"
    for i in range(1, len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        d += f"Q{n(x1)} {n(y1)} {n((x1 + x2) / 2)} {n((y1 + y2) / 2)}"
    return (f'<path d="{d}" fill="none" stroke="{PENCIL}" stroke-width="2.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def check_art():
    pre = "ck"
    s = 0.53
    rx0, ry0, rx1, ry1 = CHECK_CROP                  # crop of page.jpg: around the circled line
    cardx, cardy, pad = 6, 8, 14
    cw, chh = (rx1 - rx0) * s + 2 * pad, (ry1 - ry0) * s + 2 * pad
    ix, iy = cardx + pad, cardy + pad
    clip = f"{pre}-clip"
    img = (f'<clipPath id="{clip}"><rect x="{n(ix)}" y="{n(iy)}" width="{n((rx1 - rx0) * s)}" '
           f'height="{n((ry1 - ry0) * s)}"/></clipPath>'
           f'<rect x="{n(cardx)}" y="{n(cardy)}" width="{n(cw)}" height="{n(chh)}" rx="16" fill="#fff" '
           f'filter="url(#{pre}-paper)"/>'
           f'<image href="sample/page.jpg" x="{n(ix - rx0 * s)}" y="{n(iy - ry0 * s)}" '
           f'width="{n(PAGE_W * s)}" height="{n(PAGE_H * s)}" clip-path="url(#{clip})"/>')
    lx0, lx1, ly0, ly1 = CHECK_LINE
    lcx = ix + ((lx0 + lx1) / 2 - rx0) * s
    lcy = iy + ((ly0 + ly1) / 2 - ry0) * s
    loop = pencil_loop(lcx, lcy, (lx1 - lx0) * s / 2 + 6, (ly1 - ly0) * s / 2 + 5)

    tx, ty, tw, th = 118, cardy + chh + 24, 270, 70
    t = tag(pre, tx, ty, tw, th,
            CHECK_TAG,
            rx=20, glyph=True)
    # a dashed line from the person back to the line that names her, ending in an arrowhead
    sx, sy = tx + 52, ty - 2
    ex, ey = lcx + 24, lcy + (ly1 - ly0) * s / 2 + 9
    conn = [(sx, sy), (sx, sy - 22), (ex + 6, ey + 26), (ex, ey)]
    d = f"M{n(sx)} {n(sy)}C{n(conn[1][0])} {n(conn[1][1])} {n(conn[2][0])} {n(conn[2][1])} {n(ex)} {n(ey)}"
    ang = angle_at(conn, 1)
    head = (f'<g transform="translate({n(ex)} {n(ey)}) rotate({n(ang)})">'
            f'<path d="M-9 -5.5 0 0-9 5.5" fill="none" stroke="{PENCIL}" stroke-width="2.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></g>')
    line = (f'<path d="{d}" fill="none" stroke="{PENCIL}" stroke-width="2.6" stroke-dasharray="1 7" '
            f'stroke-linecap="round"/>')
    vb_w, vb_h = max(cardx + cw, tx + tw) + 8, ty + th + 12
    return (
        f'<svg class="check-art" viewBox="0 0 {n(vb_w)} {n(vb_h)}" role="img" aria-labelledby="ck-t">'
        f'<title id="ck-t">{CHECK_TAG[0][0]}, a person in the tree, linked back to the line on the '
        f'scanned page that names him.</title>'
        + defs(pre) + img + f'<g filter="url(#{pre}-rough)">{loop}{line}{head}</g>' + t + "</svg>"
    )


# ---------------------------------------------------------------- closing sapling
def sapling():
    book = ('<path d="M60 74C48 66 30 64 12 67V84C30 81 48 83 60 91 72 83 90 81 108 84V67C90 64 72 66 60 74Z" '
            'fill="#fffdf8" stroke="#86684e" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path d="M60 74V91" stroke="#86684e" stroke-width="2" stroke-linecap="round"/>'
            '<path d="M22 72.5C32 71 44 72 52 75.5M22 78C32 76.5 44 77.5 52 81M98 72.5C88 71 76 72 68 75.5'
            'M98 78C88 76.5 76 77.5 68 81" fill="none" stroke="#c9bba5" stroke-width="1.6" stroke-linecap="round"/>')
    stem_p = [(60, 74), (58, 58), (63, 42), (60, 20)]
    stem = tapered(stem_p, 4.2, 2.4)
    lv = (leaf(59.5, 56, -150, 24, 11, LEAVES[0]) + leaf(61, 46, -32, 24, 11, LEAVES[2])
          + leaf(61.5, 34, -146, 20, 9, LEAVES[1]) + leaf(60.5, 24, -58, 18, 8, LEAVES[0]))
    return ('<svg class="sapling" viewBox="0 0 120 96" aria-hidden="true">'
            '<defs><filter id="sp-rough" x="-10%" y="-10%" width="120%" height="120%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="3"/>'
            '<feDisplacementMap in="SourceGraphic" scale="1.8" xChannelSelector="R" yChannelSelector="G"/>'
            '</filter></defs>'
            f'<g filter="url(#sp-rough)">{book}{stem}{lv}</g></svg>')


def inject(html: str, marker: str, content: str, indent: str) -> str:
    pat = re.compile(rf"<!-- {marker}:start -->.*?<!-- {marker}:end -->", re.S)
    assert len(pat.findall(html)) == 1, marker
    block = f"<!-- {marker}:start -->\n{indent}{content}\n{indent}<!-- {marker}:end -->"
    return pat.sub(lambda m: block, html)


def main():
    index = SITE / "index.html"
    html = index.read_text()
    html = inject(html, "art", hero_wide() + "\n          " + hero_tall(), "          ")
    html = inject(html, "check", check_art(), "          ")
    html = inject(html, "sapling", sapling(), "          ")
    index.write_text(html)
    print("injected", len(html), "bytes")


if __name__ == "__main__":
    main()
