"""Monochrome, typed-feel profile README graphics. Black, grey, white. DM Mono everywhere.

    python scripts/mono.py            # static graphics
    GITHUB_TOKEN=... python scripts/mono.py stats   # live GitHub numbers (also run by the Action)
"""
import datetime as dt
import json
import math
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from typo import Face, reveal, txt, typed  # noqa: E402

M, MB = Face("DMMono-Regular.ttf"), Face("DMMono-Medium.ttf")
ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "icons.json")))
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "mono")

CARD, LINE, WHITE, GREY, DIM, SOFT = "#000000", "#30363d", "#f0f6fc", "#8b949e", "#6e7681", "#c9d1d9"

CSS = (
    "@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}"
    "@keyframes fade{from{opacity:0}to{opacity:1}}"
    "@keyframes pop{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:scale(1)}}"
    "@keyframes twk{0%,100%{opacity:.15}50%{opacity:.95}}"
    "@keyframes drift{0%,100%{transform:translateX(0)}50%{transform:translateX(46px)}}"
    "@keyframes flow{to{stroke-dashoffset:-60}}"
    "@keyframes spin{to{transform:rotate(360deg)}}"
    "@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}"
    "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
)


def doc(w, h, body, defs="", css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">'
            f'<style>{CSS}{css}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style><defs>{defs}</defs>{body}</svg>')


def save(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def box(x, y, w, h, r=8, fill=CARD, stroke=LINE):
    return f'<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'


# ---------------------------------------------------------------------------- hero
def smooth(pts):
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        d += f"Q{pts[i][0]:.1f} {pts[i][1]:.1f} {mx:.1f} {my:.1f}"
    return d + f"L{pts[-1][0]:.1f} {pts[-1][1]:.1f}"


def ridge(seed, base, amp, n=26, x0=-40, x1=1240):
    rnd = random.Random(seed)
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = base - amp * (.55 + .45 * math.sin(i * .62 + seed)) * (.7 + .3 * math.sin(i * .21 + seed * 2)) - rnd.uniform(0, amp * .25)
        pts.append((x, y))
    return pts


def hero():
    W, H, LOOP = 1200, 400, 14
    rnd = random.Random(12)
    far = ridge(3, 262, 78)
    mid = ridge(9, 290, 46, 22)
    near = ridge(15, 330, 30, 18)
    # winding river, horizon to viewer
    left, right, centre = [], [], []
    for i in range(61):
        t = i / 60
        y = 250 + 160 * t
        cx = 600 + 150 * math.sin(2.35 * math.pi * t + .35) * (.12 + .88 * t ** .9)
        w = 3 + 170 * t ** 1.35
        left.append((cx - w / 2, y))
        right.append((cx + w / 2, y))
        centre.append((cx, y))
    river = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in left) + "L" + "L".join(f"{x:.1f} {y:.1f}" for x, y in reversed(right)) + "Z"
    ground = ("M-10 288" + "".join(f"L{x:.1f} {y:.1f}" for x, y in near[1:-1]) + "L1210 292V410H-10Z")
    shimmer = "".join(
        f'<path d="M' + "L".join(f"{cx + off * (3 + 170 * (k / 60) ** 1.35) / 2:.1f} {y:.1f}" for k, (cx, y) in enumerate(centre) if k > 8)
        + f'" fill="none" stroke="#fff" stroke-opacity="{.35 - abs(off) * .25:.2f}" stroke-width="1.2" stroke-dasharray="14 46" style="animation:flow {5 + i}s linear infinite"/>'
        for i, off in enumerate((-.6, -.25, .1, .5))
    )
    stars = "".join(f'<circle cx="{rnd.uniform(10, 1190):.0f}" cy="{rnd.uniform(8, 180):.0f}" r="{rnd.choice([.6, .8, 1.1]):.1f}" fill="#fff" '
                    f'style="animation:twk {rnd.uniform(2.5, 6):.1f}s ease-in-out {rnd.uniform(0, 5):.1f}s infinite"/>' for _ in range(70))
    mist = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" opacity="{op}" style="animation:drift {dur}s ease-in-out {-d}s infinite"/>'
                   for cx, cy, rx, ry, op, dur, d in [(300, 270, 300, 18, .10, 26, 0), (820, 258, 340, 16, .09, 32, 9), (560, 300, 380, 20, .07, 38, 18), (1000, 292, 260, 14, .08, 30, 4)])
    mound_l = "M-10 400V350Q120 322 260 360T420 410V400Z"
    mound_r = "M1210 400V344Q1090 318 960 358T780 410V400Z"
    word = "Welcome to Laksh's GitHub </>"
    size = 34
    cw = M.width("M", size)
    x = (W - len(word) * cw) / 2
    clip, t, cur = typed("h", MB, x, 140, word, .8, .07, size, WHITE, WHITE, LOOP, keep_cursor=True)
    defs = (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050506"/><stop offset=".4" stop-color="#202023"/><stop offset=".62" stop-color="#6c6c72"/><stop offset=".72" stop-color="#b6b6bb"/><stop offset="1" stop-color="#8a8a90"/></linearGradient>'
        '<linearGradient id="far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a3f"/><stop offset="1" stop-color="#8d8d92"/></linearGradient>'
        '<linearGradient id="mid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#202024"/><stop offset="1" stop-color="#4c4c51"/></linearGradient>'
        '<radialGradient id="glowriv" cx=".5" cy="0" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient><linearGradient id="riv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f4f6"/><stop offset=".55" stop-color="#b9b9be"/><stop offset="1" stop-color="#5d5d62"/></linearGradient>'
        '<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".65"/></radialGradient>'
        '<filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>'
        '<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="3"/>'
        '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 -.17"/></filter>'
        '<clipPath id="card"><rect width="1200" height="400" rx="8"/></clipPath>' + clip
    )
    body = (
        f'<animate id="loop" attributeName="opacity" from="1" to="1" dur="{LOOP}s" begin="0s;loop.end"/>'
        '<g clip-path="url(#card)"><rect width="1200" height="400" fill="url(#sky)"/>'
        f'{stars}<path d="{smooth(far)}L1240 400H-40Z" fill="url(#far)"/><path d="{smooth(mid)}L1240 400H-40Z" fill="url(#mid)"/>'
        f'<path d="{ground}" fill="#0a0a0b"/><path d="{river}" fill="url(#riv)"/><path d="{river}" fill="url(#glowriv)"/>{shimmer}'
        f'<path d="{mound_l}" fill="#030304"/><path d="{mound_r}" fill="#030304"/>'
        f'<g filter="url(#blur)">{mist}</g>'
        f'{t}{cur}'
        '<rect width="1200" height="400" fill="url(#vig)"/><rect width="1200" height="400" filter="url(#grain)" opacity=".45"/></g>'
        f'<rect x=".75" y=".75" width="1198.5" height="398.5" rx="7.5" fill="none" stroke="{LINE}" stroke-width="1.5"/>'
    )
    return doc(W, H, body, defs, label="Welcome to Laksh's GitHub")


# ---------------------------------------------------------------------------- link badges
def badge(label, icon=None, mono=None, w=176):
    t, tw_ = txt(MB, label, 12, 44, 24, WHITE, 1.6)
    ic = (f'<g transform="translate(15 10) scale(.75)"><path d="{ICONS[icon]}" fill="{WHITE}"/></g>' if icon else txt(MB, mono, 15, 24, 25, WHITE, 0, "m")[0])
    return doc(w, 38, box(0, 0, w, 38, 5) + ic + t, label=label)


# ---------------------------------------------------------------------------- headings
ICO = {
    "about": '<circle cx="11" cy="7" r="4"/><path d="M3 20c0-5 4-7 8-7s8 2 8 7"/>',
    "tech": '<path d="M8 6L2 11l6 5M14 6l6 5-6 5"/>',
    "work": '<rect x="3" y="5" width="16" height="13" rx="2"/><path d="M3 9h16"/>',
    "path": '<circle cx="5" cy="6" r="2"/><circle cx="17" cy="16" r="2"/><path d="M7 7c8 0 2 8 8 8"/>',
    "wins": '<path d="M11 3l2.4 5 5.4.7-4 3.8 1 5.4-4.8-2.7-4.8 2.7 1-5.4-4-3.8 5.4-.7z"/>',
    "stats": '<path d="M4 18V9M10 18V4M16 18v-6"/>',
    "connect": '<rect x="2" y="5" width="18" height="13" rx="2"/><path d="M2 7l9 6 9-6"/>',
}


def heading(icon, title):
    W, H = 1200, 84
    tw_ = MB.width(title, 26, 0)
    x0 = 600 - (tw_ + 36) / 2
    t, _ = txt(MB, title, 26, x0 + 36, 48, WHITE, 0)
    body = (f'<g style="animation:fade .8s ease both"><g transform="translate({x0:.1f} 26)" fill="none" stroke="{WHITE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICO[icon]}</g>{t}'
            f'<rect x="40" y="70" width="1120" height="1.5" fill="{LINE}" style="transform-origin:600px 0;animation:grow 1s ease-out both"/></g>')
    return doc(W, H, body, label=title)


# ---------------------------------------------------------------------------- about art: a quiet wireframe globe
def about_art(size=400):
    cx = cy = size / 2
    R, tau, frames = 118, math.radians(20), 60
    rnd = random.Random(6)

    def proj(phi, lam):
        x0, y0, z0 = math.cos(phi) * math.sin(lam), math.sin(phi), math.cos(phi) * math.cos(lam)
        y1 = y0 * math.cos(tau) - z0 * math.sin(tau)
        z1 = y0 * math.sin(tau) + z0 * math.cos(tau)
        return cx + R * x0, cy - R * y1, z1

    def runs(points, front):
        paths, cur = [], []
        for x, y, z in points:
            if (z >= 0) == front:
                cur.append((x, y))
            elif cur:
                paths.append(cur)
                cur = []
        if cur:
            paths.append(cur)
        return "".join("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in p) for p in paths if len(p) > 1)

    lat_f = lat_b = ""
    for deg in (-60, -30, 0, 30, 60):
        pts = [proj(math.radians(deg), math.radians(l)) for l in range(0, 361, 4)]
        lat_f += runs(pts, True)
        lat_b += runs(pts, False)
    sector = [(rnd.uniform(-70, 70), rnd.uniform(0, 45)) for _ in range(5)]
    mer, dots = [], []
    for k in range(frames):
        th = k * 45 / frames
        mer.append("".join(runs([proj(math.radians(p), math.radians(th + m * 45)) for p in range(-90, 91, 6)], True) for m in range(8)))
        d = ""
        for m in range(8):
            for lat, lon in sector:
                x, y, z = proj(math.radians(lat), math.radians(th + m * 45 + lon))
                if z > .05:
                    d += f"M{x:.1f} {y:.1f}h.01"
        dots.append(d or "M0 0")
    anim_d = lambda vals: f'<animate attributeName="d" calcMode="discrete" dur="5s" repeatCount="indefinite" values="{";".join(vals)}"/>'
    stars = "".join(f'<circle cx="{rnd.uniform(14, size - 14):.0f}" cy="{rnd.uniform(14, size - 14):.0f}" r="{rnd.choice([.6, .9, 1.2]):.1f}" fill="#fff" '
                    f'style="animation:twk {rnd.uniform(2.5, 6):.1f}s ease-in-out {rnd.uniform(0, 5):.1f}s infinite"/>' for _ in range(46))
    orbit = (f'<circle cx="{cx}" cy="{cy}" r="{R + 34}" fill="none" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="2 6"/>'
             f'<circle r="3.2" fill="#fff"><animateMotion dur="18s" repeatCount="indefinite" path="M{cx + R + 34} {cy}A{R + 34} {R + 34} 0 1 1 {cx - R - 34} {cy}A{R + 34} {R + 34} 0 1 1 {cx + R + 34} {cy}"/></circle>')
    body = (box(0, 0, size, size, 8) + stars + orbit
            + f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#0a0a0b" stroke="#fff" stroke-opacity=".7" stroke-width="1.3"/>'
            f'<path d="{lat_b}" fill="none" stroke="#fff" stroke-opacity=".1"/><path d="{lat_f}" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="1.1"/>'
            f'<path fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.1">{anim_d(mer)}</path>'
            f'<path fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round">{anim_d(dots)}</path>')
    return doc(size, size, body, label="Wireframe globe")


# ---------------------------------------------------------------------------- tech badges
TECH = [("html5", "HTML"), ("css", "CSS"), ("javascript", "JavaScript"), ("typescript", "TypeScript"), ("react", "React"), ("nextdotjs", "Next.js"),
        ("tailwindcss", "Tailwind"), ("vite", "Vite"), ("threedotjs", "Three.js"), ("nodedotjs", "Node.js"), ("express", "Express"), ("python", "Python"),
        ("django", "Django"), ("postgresql", "PostgreSQL"), ("prisma", "Prisma"), ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("supabase", "Supabase"),
        ("firebase", "Firebase"), ("redis", "Redis"), ("numpy", "NumPy"), ("pandas", "Pandas"), ("scikitlearn", "scikit-learn"), ("googlegemini", "Gemini"),
        ("claude", "Claude"), ("git", "Git"), ("github", "GitHub"), ("docker", "Docker"), ("vercel", "Vercel"), ("netlify", "Netlify"), ("figma", "Figma")]


def tech():
    rows, cur, curw = [], [], 0
    items = [(s, n, MB.width(n.upper(), 12, 1.3) + 58) for s, n in TECH]
    for it in items:
        if curw + it[2] > 1120 and cur:
            rows.append(cur)
            cur, curw = [], 0
        cur.append(it)
        curw += it[2] + 10
    rows.append(cur)
    body, n = "", 0
    for r, row in enumerate(rows):
        total = sum(w for *_, w in row) + 10 * (len(row) - 1)
        x = (1200 - total) / 2
        for s, name, w in row:
            t, _ = txt(MB, name.upper(), 12, 40, 24, WHITE, 1.3)
            body += (f'<g transform="translate({x:.1f} {10 + r * 46})"><g style="animation:pop .4s ease-out {n * .03:.2f}s both;transform-origin:{w / 2:.0f}px 18px">'
                     f'{box(0, 0, w, 38, 5)}<g transform="translate(14 10) scale(.75)"><path d="{ICONS[s]}" fill="{WHITE}"/></g>{t}</g></g>')
            x += w + 10
            n += 1
    return doc(1200, 20 + len(rows) * 46, body, label="Technologies")


# ---------------------------------------------------------------------------- project cards (live from GitHub)
NOTES = json.load(open(os.path.join(os.path.dirname(__file__), "project-notes.json"), encoding="utf-8"))


def clean(text):
    t = re.sub(r"[^\x20-\x7E]", " ", text or "")
    return re.sub(r"\s+", " ", t).strip()


def first_sentence(t, limit=130):
    cut = t.find(". ")
    if 0 < cut < limit:
        return t[:cut + 1]
    return t[:limit].rstrip(" ,;") + ("..." if len(t) > limit else "")


def wrap2(t, width=60):
    lines, cur = [], ""
    words = t.split()
    for i, w in enumerate(words):
        if len(cur) + len(w) + (1 if cur else 0) <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
            if len(lines) == 2:
                break
    if len(lines) < 2 and cur:
        lines.append(cur)
    used = len(" ".join(lines).split())
    if used < len(words):
        lines[-1] = lines[-1][:width - 3].rstrip(" ,;.") + "..."
    return (lines + ["", ""])[:2]


def ago(iso):
    d = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).days
    if d < 1:
        return "today"
    if d < 2:
        return "yesterday"
    if d < 45:
        return f"{d}d ago"
    if d < 700:
        return f"{round(d / 30)}mo ago"
    return f"{round(d / 365)}y ago"


def describe(r):
    host = re.sub(r"^https?://|/$", "", r["homepageUrl"] or "")
    return NOTES.get(r["name"]) or first_sentence(clean(r["description"])) or (f"Live at {host}" if host else "")


def pick_projects(nodes, login):
    out = []
    for r in nodes:
        if r["name"].lower() == login.lower() or r["isArchived"] or r["isFork"]:
            continue
        if not describe(r):
            continue
        out.append(r)
    return out[:8]


def card(i, r):
    title = r["name"].replace("-", " ").replace("_", " ").upper()
    title = title if len(title) <= 24 else title[:23] + "."
    lines = wrap2(describe(r))
    kind = (r.get("primaryLanguage") or {}).get("name") or "REPO"
    topics = [t["topic"]["name"] for t in r["repositoryTopics"]["nodes"]]
    tags = topics[:3] or [e["node"]["name"] for e in r["languages"]["edges"]][:3]
    W, H = 580, 176
    chips, x = "", 24
    for c in tags:
        w = M.width(c.upper(), 11, 1.2) + 22
        chips += f'<rect x="{x + .5}" y="129.5" width="{w:.0f}" height="26" rx="4" fill="none" stroke="{LINE}"/>' + txt(M, c.upper(), 11, x + w / 2, 146, GREY, 1.2, "m")[0]
        x += w + 8
    star = f'<path d="M0 -6l1.8 3.9 4.2.5-3.1 2.9.8 4.2L0 3.4l-3.7 2.1.8-4.2L-6 -1.6l4.2-.5z" fill="none" stroke="{GREY}" stroke-width="1.2" stroke-linejoin="round"/>'
    meta = txt(M, f'{r["stargazerCount"]}', 12, 552, 146, GREY, 0, "r")[0]
    mw = M.width(str(r["stargazerCount"]), 12)
    meta += f'<g transform="translate({552 - mw - 12:.0f} 142)">{star}</g>' + txt(M, f'UPDATED {ago(r["pushedAt"]).upper()}', 10, 552 - mw - 26, 146, DIM, 1, "r")[0]
    body = (
        f'<g style="animation:rise .6s ease-out {i * .08:.2f}s both">{box(0, 0, W, H)}'
        + txt(M, kind.upper(), 11, 24, 36, DIM, 2)[0] + txt(M, f"{i + 1:02d}", 13, 556, 34, DIM, 1, "r")[0]
        + txt(MB, title, 22, 24, 72, WHITE, 0)[0] + txt(M, lines[0], 13, 24, 98, GREY)[0] + txt(M, lines[1], 13, 24, 118, GREY)[0]
        + chips + meta + "</g>"
    )
    return doc(W, H, body, label=title), title


def write_readme_block(projects):
    path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    text = open(path, encoding="utf-8").read()
    links = "\n".join(
        f'<a href="{r["url"]}"><img src="assets/mono/card-{i + 1:02d}.svg" alt="{re.sub(chr(34), "", r["name"])}: {re.sub(chr(34), "", describe(r))}" width="49%"></a>'
        for i, r in enumerate(projects))
    new = re.sub(r"(<!-- projects:start -->).*?(<!-- projects:end -->)", lambda m: f"{m.group(1)}\n{links}\n{m.group(2)}", text, flags=re.S)
    if new != text:
        open(path, "w", encoding="utf-8").write(new)


# ---------------------------------------------------------------------------- terminal-style lists
def terminal(cmd, rows, row_h, col_x, extra_h=0, notes=None):
    W = 1200
    H = 74 + len(rows) * row_h + extra_h + 18
    head, _ = reveal(M, "laksh@github:~$ ", 15, 28, 42, GREY, .1, .02, .3)
    cmd_t, end = reveal(MB, cmd, 15, 28 + M.width("laksh@github:~$ ", 15), 42, WHITE, .5, .045, .3)
    body = box(0, 0, W, H) + f'<rect x="1" y="60" width="{W - 2}" height="1.5" fill="{LINE}"/>' + head + cmd_t
    for i, row in enumerate(rows):
        y = 62 + (i + 1) * row_h - row_h * .36
        cells = ""
        for j, (text, style) in enumerate(row):
            if not text:
                continue
            face, size, fill = style
            cells += txt(face, text, size, col_x[j], y, fill, 0)[0]
        body += f'<g style="animation:rise .5s ease-out {1.2 + i * .18:.2f}s both">{cells}</g>'
        if i < len(rows) - 1:
            body += f'<rect x="24" y="{62 + (i + 1) * row_h:.0f}" width="{W - 48}" height="1" fill="{LINE}" opacity=".6"/>'
    return body, H


def journey():
    rows = [
        [("2025.06", (M, 14, DIM)), ("Hotel Kavana", (MB, 18, WHITE)), ("IT infrastructure intern. Networks, POS systems, workflow automation.", (M, 13.5, GREY))],
        [("2025.08", (M, 14, DIM)), ("IIT Madras", (MB, 18, WHITE)), ("AI and algorithmic problem solving. Eight weeks of data science.", (M, 13.5, GREY))],
        [("2025.08", (M, 14, DIM)), ("MoreYeahs", (MB, 18, WHITE)), ("Web developer. Built GigX, a Django gig-economy platform.", (M, 13.5, GREY))],
        [("2025.10", (M, 14, DIM)), ("Unified Mentor", (MB, 18, WHITE)), ("Full-stack developer. Four production apps shipped.", (M, 13.5, GREY))],
        [("2026.08", (M, 14, WHITE)), ("ShiftsDeal", (MB, 18, WHITE)), ("Tech head. Payments, bookings, features shipped daily.", (M, 13.5, SOFT))],
        [("2026.08", (M, 14, WHITE)), ("Masters' Union", (MB, 18, WHITE)), ("UG Data Science & AI, class of 2030.", (M, 13.5, SOFT))],
    ]
    body, H = terminal("git log --career", rows, 52, [28, 130, 360])
    for i in (4, 5):  # NOW tags
        y = 62 + (i + 1) * 52 - 52 * .36
        body += (f'<g style="animation:rise .5s ease-out {1.2 + i * .18:.2f}s both"><rect x="1088" y="{y - 17:.0f}" width="70" height="24" rx="4" fill="{WHITE}"/>'
                 + txt(MB, "NOW" if i == 4 else "NEW", 12, 1123, y, "#000", 1.5, "m")[0] + "</g>")
    return doc(1200, H, body, label="Career timeline")


def wins():
    rows = [
        [("AIR 54", (MB, 22, WHITE)), ("All-India rank in 10 m air pistol, U-17 Nationals. State rank 34.", (M, 14, GREY))],
        [("VVM 2023", (MB, 22, WHITE)), ("Regional winner of the national science competition, advanced to the nationals.", (M, 14, GREY))],
        [("2ND PLACE", (MB, 22, WHITE)), ("Web Wizards, AFS Tech Ramble. Special mention for deployment.", (M, 14, GREY))],
        [("TOP 100", (MB, 22, WHITE)), ("National quiz. Won an invite to watch an ISRO satellite launch.", (M, 14, GREY))],
        [("ALSO", (MB, 22, DIM)), ("Robowars '25 2nd  /  G20 MUN press corps  /  House Captain  /  CHEMUN, IIMUN, TISB MUN  /  Round Square", (M, 13, GREY))],
    ]
    body, H = terminal("cat achievements.txt", rows, 56, [28, 250])
    return doc(1200, H, body, label="Achievements")


# ---------------------------------------------------------------------------- connect + footer
def footer():
    t, _ = reveal(M, "thanks for stopping by", 16, 600 - M.width("thanks for stopping by </>", 16) / 2, 52, GREY, .2, .04, .4)
    code, _ = txt(MB, "</>", 16, 600 + M.width("thanks for stopping by ", 16) - M.width("thanks for stopping by </>", 16) / 2, 52, WHITE)
    return doc(1200, 90, f'<rect x="40" y="14" width="1120" height="1.5" fill="{LINE}"/>{t}<g style="animation:fade 1s ease 1.2s both">{code}</g>', label="Thanks for stopping by")


# ---------------------------------------------------------------------------- live stats
QUERY = """query($login:String!){user(login:$login){
  repositories(ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false,first:100){totalCount nodes{stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}
  projects: repositories(first:40,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false,orderBy:{field:PUSHED_AT,direction:DESC}){nodes{name description url homepageUrl stargazerCount pushedAt isArchived isFork primaryLanguage{name} languages(first:3,orderBy:{field:SIZE,direction:DESC}){edges{node{name}}} repositoryTopics(first:3){nodes{topic{name}}}}}
  repositoriesContributedTo(first:1,includeUserRepositories:false,contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){totalCount}
  contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions
    contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


def fetch(login):
    import urllib.request
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]


def streaks(days):
    today = dt.date.today().isoformat()
    days = [d for d in days if d["date"] <= today]
    best, run, best_end = 0, 0, None
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        if run > best:
            best, best_end = run, d["date"]
    i = len(days) - 1
    if i >= 0 and days[i]["contributionCount"] == 0:
        i -= 1
    cur = 0
    while i >= 0 and days[i]["contributionCount"]:
        cur += 1
        i -= 1
    cur_end = days[-1]["date"] if cur else None
    fmt = lambda s, n: (dt.date.fromisoformat(s) - dt.timedelta(days=n - 1)).strftime("%b %d") + " - " + dt.date.fromisoformat(s).strftime("%b %d") if s and n else "no streak yet"
    return cur, fmt(cur_end, cur), best, fmt(best_end, best)


def stats(login="TheRealLaksh"):
    u = fetch(login)
    cc = u["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
    active = sum(1 for d in days if d["contributionCount"])
    cur, cur_r, best, best_r = streaks(days)
    first = dt.date.fromisoformat(days[0]["date"]).strftime("%b %Y")

    # left card
    rows = [("Total Stars Earned", stars), ("Total Commits (last year)", cc["totalCommitContributions"]), ("Total PRs", cc["totalPullRequestContributions"]),
            ("Total Issues", cc["totalIssueContributions"]), ("Contributed to (last year)", u["repositoriesContributedTo"]["totalCount"])]
    left = box(0, 0, 590, 250) + txt(MB, f"{login}'s GitHub Stats", 18, 28, 44, WHITE)[0]
    for i, (k, v) in enumerate(rows):
        y = 84 + i * 33
        left += f'<rect x="28" y="{y - 9}" width="6" height="6" fill="{WHITE}"/>' + txt(M, k, 14, 46, y, SOFT)[0] + txt(MB, str(v), 14, 330, y, WHITE, 0, "r")[0]
    ring_c = (480, 138)
    frac = min(active / 365, 1)
    circ = 2 * math.pi * 52
    left += (f'<circle cx="{ring_c[0]}" cy="{ring_c[1]}" r="52" fill="none" stroke="{LINE}" stroke-width="9"/>'
             f'<circle cx="{ring_c[0]}" cy="{ring_c[1]}" r="52" fill="none" stroke="{WHITE}" stroke-width="9" stroke-linecap="round" pathLength="1" stroke-dasharray="1" '
             f'style="--p:{frac:.3f};transform:rotate(-90deg);transform-origin:{ring_c[0]}px {ring_c[1]}px;animation:ringfill 1.6s ease-out both"/>'
             + txt(MB, str(active), 28, ring_c[0], ring_c[1] + 2, WHITE, 0, "m")[0] + txt(M, "ACTIVE DAYS", 9, ring_c[0], ring_c[1] + 22, GREY, 1, "m")[0])
    # right card
    right = box(0, 0, 590, 250)
    cols = [98, 295, 492]
    right += f'<rect x="197" y="46" width="1.5" height="158" fill="{LINE}"/><rect x="394" y="46" width="1.5" height="158" fill="{LINE}"/>'
    right += (txt(MB, f'{cal["totalContributions"]:,}', 38, cols[0], 126, WHITE, 0, "m")[0] + txt(M, "Total Contributions", 14, cols[0], 164, SOFT, 0, "m")[0]
              + txt(M, f"{first} - Present", 11.5, cols[0], 188, DIM, 0, "m")[0])
    right += (f'<circle cx="{cols[1]}" cy="112" r="40" fill="none" stroke="{WHITE}" stroke-width="5" stroke-dasharray="190 70" transform="rotate(-232 {cols[1]} 112)" stroke-linecap="round"/>'
              + txt(MB, str(cur), 38, cols[1], 126, WHITE, 0, "m")[0] + txt(MB, "Current Streak", 14, cols[1], 182, WHITE, 0, "m")[0] + txt(M, cur_r, 11.5, cols[1], 204, DIM, 0, "m")[0])
    right += txt(MB, str(best), 38, cols[2], 126, WHITE, 0, "m")[0] + txt(M, "Longest Streak", 14, cols[2], 164, SOFT, 0, "m")[0] + txt(M, best_r, 11.5, cols[2], 188, DIM, 0, "m")[0]
    css = "@keyframes ringfill{from{stroke-dashoffset:1}to{stroke-dashoffset:calc(1 - var(--p))}}"
    save("stats.svg", doc(1200, 250, f'<g>{left}</g><g transform="translate(610 0)">{right}</g>', css=css, label="GitHub stats"))

    # activity: contributions by month (last 12 months) + top languages
    last_day = dt.date.today().isoformat()
    by_month = {}
    for d in days:
        if d["date"] <= last_day:
            by_month[d["date"][:7]] = by_month.get(d["date"][:7], 0) + d["contributionCount"]
    months = sorted(by_month)[-12:]
    vals = [by_month[m] for m in months]
    mx = max(max(vals), 1)
    step = 1 if mx <= 5 else 5 if mx <= 25 else 10 if mx <= 60 else 25 if mx <= 150 else 50
    top = ((mx + step - 1) // step) * step
    X0, X1, Y0, Y1 = 78, 668, 84, 244
    slot = (X1 - X0) / len(vals)
    bw = min(34, slot * .6)
    grid = ""
    for g in range(0, top + 1, step):
        y = Y1 - (Y1 - Y0) * g / top
        grid += f'<path d="M{X0} {y:.1f}H{X1}" stroke="{LINE}" stroke-dasharray="3 5"/>' + txt(M, str(g), 11.5, X0 - 12, y + 4, GREY, 0, "r")[0]
    bars = ""
    for i, (m, v) in enumerate(zip(months, vals)):
        cx = X0 + slot * (i + .5)
        h = (Y1 - Y0) * v / top
        lab = dt.date.fromisoformat(m + "-01").strftime("%b").upper()
        hi = v == max(vals) and v > 0
        bars += (f'<g style="animation:fade .4s ease {i * .06:.2f}s both"><rect x="{cx - bw / 2:.1f}" y="{Y1 - h:.1f}" width="{bw:.1f}" height="{max(h, 1.5):.1f}" rx="3" fill="{WHITE if hi else "#8b949e"}" '
                 f'style="transform-box:fill-box;transform-origin:50% 100%;animation:growy .7s ease-out {i * .06:.2f}s both"><title>{lab}: {v}</title></rect>'
                 + (txt(MB, str(v), 12, cx, Y1 - h - 8, WHITE, 0, "m")[0] if v else "") + txt(M, lab, 11, cx, Y1 + 22, GREY, 0, "m")[0] + "</g>")
    chart = box(0, 0, 700, 300) + txt(MB, "Contributions by month", 18, 28, 44, WHITE)[0] + txt(M, "last 12 months", 12, 672, 44, DIM, 0, "r")[0] + grid + bars
    sizes = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    topl = sorted(sizes.items(), key=lambda kv: -kv[1])[:6]
    tot = sum(sizes.values()) or 1
    langs = box(0, 0, 480, 300) + txt(MB, "Top languages", 18, 28, 44, WHITE)[0] + txt(M, "public repos", 12, 452, 44, DIM, 0, "r")[0]
    for i, (name, v) in enumerate(topl):
        y = 86 + i * 34
        pct = 100 * v / tot
        langs += (txt(MB, name, 13.5, 28, y, WHITE)[0] + txt(M, f"{pct:.1f}%", 13, 452, y, GREY, 0, "r")[0]
                  + f'<rect x="28" y="{y + 8}" width="424" height="5" rx="2.5" fill="{LINE}"/>'
                  f'<rect x="28" y="{y + 8}" width="{max(424 * pct / 100, 3):.1f}" height="5" rx="2.5" fill="{WHITE}" style="transform-box:fill-box;transform-origin:0 50%;animation:grow .9s ease-out {i * .1:.1f}s both"/>')
    css2 = "@keyframes growy{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
    save("activity.svg", doc(1200, 300, f'<g>{chart}</g><g transform="translate(720 0)">{langs}</g>', css=css2, label="Contributions by month and top languages"))
    projects = pick_projects(u["projects"]["nodes"], login)
    for i, r in enumerate(projects):
        save(f"card-{i + 1:02d}.svg", card(i, r)[0])
    write_readme_block(projects)
    print("stats built", cur, best, [r["name"] for r in projects])


# ---------------------------------------------------------------------------- run
def main():
    save("hero.svg", hero())
    save("badge-linkedin.svg", badge("LINKEDIN", None, "in"))
    save("badge-email.svg", badge("EMAIL", "gmail"))
    save("badge-instagram.svg", badge("INSTAGRAM", "instagram"))
    for icon, title, name in [("about", "About me", "h-about"), ("tech", "Technologies", "h-tech"), ("work", "Projects", "h-work"), ("path", "Journey", "h-path"),
                              ("stats", "Statistics", "h-stats"), ("connect", "Let's connect", "h-connect")]:
        save(name + ".svg", heading(icon, title))
    save("about-art.svg", about_art())
    save("tech.svg", tech())
    save("journey.svg", journey())
    save("footer.svg", footer())
    print("mono assets built")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        stats()
    else:
        main()
