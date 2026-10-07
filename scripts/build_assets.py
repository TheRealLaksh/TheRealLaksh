"""Builds every static graphic for the profile README into assets/light, assets/dark and assets/shared.

    python scripts/build_assets.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import *  # noqa: E402,F401,F403

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")


def write(folder, name, content):
    d = os.path.join(ROOT, folder)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w", encoding="utf-8") as f:
        f.write(content)


def accents(t):
    return [t["cobalt"], t["orange"], t["mint"], t["lavender"], t["pink"], t["yellow"]]


def tint_of(t, color):
    m = {t["cobalt"]: t["tint_cobalt"], t["orange"]: t["tint_orange"], t["mint"]: t["tint_mint"],
         t["lavender"]: t["tint_lav"], t["pink"]: t["tint_pink"], t["yellow"]: t["tint_yellow"]}
    return m[color]


# ---------------------------------------------------------------------------- banner
def banner(t):
    name = "Laksh Pradhwani"
    nw = tw(name, 80, True)
    roles = [("Full-stack developer", t["cobalt"]), ("Aspiring AI/ML engineer", t["orange"]),
             ("Tech head at ShiftsDeal", t["mint"]), ("Data Science & AI at Masters' Union", t["lavender"])]
    role_svg = ""
    for i, (txt, col) in enumerate(roles):
        role_svg += (
            f'<text x="68" y="272" font-size="34" font-weight="700" fill="{col}" opacity="0">{esc(txt)}'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;.2;.25;1" dur="14s" begin="{i * 3.5}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 12;0 0;0 0;0 -12;0 -12" keyTimes="0;.04;.2;.25;1" dur="14s" begin="{i * 3.5}s" repeatCount="indefinite"/>'
            f"</text>"
        )
    defs = (
        f'<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="{t["muted"]}" opacity=".28"/></pattern>'
        '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>'
        '<clipPath id="clip"><rect width="1200" height="380" rx="30"/></clipPath>'
    )
    body = (
        f'<g clip-path="url(#clip)"><rect width="1200" height="380" fill="{t["card"]}"/><rect width="1200" height="380" fill="url(#dots)"/>'
        f'<g filter="url(#blur)"><circle cx="160" cy="60" r="130" fill="{t["cobalt"]}" opacity=".30" {anim("drift", 14)}/>'
        f'<circle cx="640" cy="360" r="120" fill="{t["orange"]}" opacity=".28" {anim("drift", 17, 2)}/>'
        f'<circle cx="1010" cy="40" r="120" fill="{t["mint"]}" opacity=".26" {anim("drift", 12, 4)}/>'
        f'<circle cx="1160" cy="330" r="110" fill="{t["lavender"]}" opacity=".30" {anim("drift", 15, 1)}/></g></g>'
        f'<rect x=".75" y=".75" width="1198.5" height="378.5" rx="29.5" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>'
        f'<g transform="translate(68 52)"><rect width="210" height="38" rx="19" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
        f'<circle cx="22" cy="19" r="10" fill="{t["mint"]}" opacity=".3" {anim("ring", 1.8)}/><circle cx="22" cy="19" r="5" fill="{t["mint"]}"/>'
        f'<text x="42" y="25" font-size="16" font-family="{MONO}" fill="{t["muted"]}">hello, world</text></g>'
        f'<text x="64" y="190" font-size="80" font-weight="800" fill="{t["ink"]}" letter-spacing="-2">{name}</text>'
        f'<rect x="68" y="204" width="{nw * .46:.0f}" height="9" rx="4.5" fill="{t["yellow"]}" opacity=".85" style="transform-box:fill-box;transform-origin:0 50%;animation:grow 1.2s ease-out both"/>'
        f"{role_svg}"
        f'<text x="68" y="326" font-size="19" fill="{t["muted"]}">Varanasi, India. I build things for the web and teach machines to learn.</text>'
        + place(sticker_target(0), 905, 118, 1.0, 6) + place(sticker_rocket(.4), 1075, 100, .95)
        + place(sticker_code(.8), 1000, 268, .92, -3) + place(sticker_ai(1.2), 1135, 258, .72)
        + place(sticker_pin(.6), 835, 285, .62) + place(sticker_tag("MERN", t["pink"], -8, .3, 17), 770, 78)
        + sparkle(960, 40, 15, P["yellow"], 0) + sparkle(1160, 175, 12, P["pink"], .8) + sparkle(820, 190, 10, P["cobalt"], 1.4)
        + sparkle(1070, 345, 12, P["yellow"], 2) + sparkle(750, 340, 10, P["orange"], .5)
    )
    return svg(1200, 380, body, defs)


# ---------------------------------------------------------------------------- headings
def heading(t, num, title, color):
    w_title = tw(title, 42, True)
    tag_w = 64
    total = tag_w + 22 + w_title
    x0 = (1200 - total) / 2
    body = (
        f'<g transform="translate({x0 + tag_w / 2} 44) rotate(-6)"><g {anim("wobble", 4)}><g filter="url(#sh)">'
        f'<rect x="-32" y="-24" width="64" height="48" rx="16" fill="#fff" stroke="#fff" stroke-width="8"/>'
        f'<rect x="-32" y="-24" width="64" height="48" rx="16" fill="{color}"/></g>'
        f'<text y="8" text-anchor="middle" font-size="22" font-weight="800" font-family="{MONO}" fill="#fff">{num}</text></g></g>'
        f'<text x="{x0 + tag_w + 22}" y="58" font-size="42" font-weight="800" fill="{t["ink"]}" letter-spacing="-1">{esc(title)}</text>'
        f'<path d="M{x0 + tag_w + 22} 76 q{w_title / 8} -10 {w_title / 4} 0 t{w_title / 4} 0 t{w_title / 4} 0 t{w_title / 4} 0" fill="none" '
        f'stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-dasharray="{w_title * 1.1:.0f}" '
        f'style="--len:{w_title * 1.1:.0f};animation:drawline 1.4s ease-out both"/>'
    )
    return svg(1200, 96, body)


# ---------------------------------------------------------------------------- now
def now(t):
    items = [("Tech head", "ShiftsDeal, a venue booking marketplace", t["mint"]),
             ("UG Data Science & AI", "Masters' Union, class of 2030", t["cobalt"]),
             ("Freelance web builds", "Client sites with their own CMS panels", t["orange"])]
    body = ""
    for i, (title, sub, col) in enumerate(items):
        x = i * 408
        body += (
            f'<g transform="translate({x} 0)" style="animation:rise .7s ease-out {i * .15}s both">'
            f'<rect x="1" y="1" width="382" height="138" rx="24" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
            f'<rect x="1" y="1" width="12" height="138" rx="6" fill="{col}" opacity=".9"/>'
            f'<g transform="translate(36 38)"><circle r="11" fill="{col}" opacity=".25" {anim("ring", 2, i * .3)}/><circle r="5.5" fill="{col}"/></g>'
            f'<text x="56" y="44" font-size="14" font-family="{MONO}" fill="{t["muted"]}" letter-spacing="2">NOW</text>'
            f'<text x="34" y="86" font-size="26" font-weight="800" fill="{t["ink"]}">{esc(title)}</text>'
            f'<text x="34" y="116" font-size="16" fill="{t["muted"]}">{esc(sub)}</text></g>'
        )
    return svg(1200, 140, f'<g transform="translate(20 0)">{body}</g>')


# ---------------------------------------------------------------------------- stack marquee
STACK = [
    ["HTML", "CSS", "JavaScript", "TypeScript", "React", "Next.js", "Vite", "Tailwind CSS", "Framer Motion", "Three.js", "GSAP"],
    ["Node.js", "Express", "Python", "Django", "PostgreSQL", "Prisma", "MySQL", "MongoDB", "Supabase", "Firebase", "Redis", "Razorpay"],
    ["Gemini API", "Groq", "NumPy", "Pandas", "Scikit-learn", "MediaPipe", "Claude Code", "Playwright", "Git", "Vercel", "Netlify", "Docker"],
]


def stack(t):
    cols = accents(t)
    rows = ""
    for r, names in enumerate(STACK):
        x, pills = 0, ""
        for i, n in enumerate(names):
            w = tw(n, 20, True) + 58
            c = cols[(i + r * 2) % len(cols)]
            pills += (
                f'<g transform="translate({x} 0)"><rect width="{w}" height="46" rx="23" fill="{tint_of(t, c)}" stroke="{c}" stroke-opacity=".45" stroke-width="1.5"/>'
                f'<circle cx="24" cy="23" r="6" fill="{c}"/><text x="40" y="30" font-size="20" font-weight="700" fill="{t["ink"]}">{esc(n)}</text></g>'
            )
            x += w + 14
        total = x
        reps = 1 if total >= 1300 else 2
        content = "".join(f'<g transform="translate({k * total} 0)">{pills}</g>' for k in range(reps + 1))
        d = [58, 74, 66][r]
        direction = "reverse" if r % 2 else "normal"
        rows += (
            f'<g transform="translate(0 {r * 66 + 8})"><g style="--w:{total}px;animation:marq {d}s linear infinite {direction}">{content}</g></g>'
        )
    defs = (
        '<linearGradient id="fadeg" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".07" stop-color="#fff"/>'
        '<stop offset=".93" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
        '<mask id="fade"><rect width="1200" height="214" fill="url(#fadeg)"/></mask>'
    )
    css = "@keyframes marq{to{transform:translateX(calc(var(--w) * -1))}}"
    return svg(1200, 214, f'<g mask="url(#fade)">{rows}</g>', defs, css)


# ---------------------------------------------------------------------------- project cards
CARDS = [
    ("profiley", "Profiley", "Resume builder", ["A reactive resume builder with real-time", "WYSIWYG editing and 10+ templates."], ["React 19", "Vite", "Tailwind"], "cobalt"),
    ("helios", "Helios", "Music player", ["Lightweight player with smooth audio controls,", "animated UI and a responsive layout."], ["HTML", "CSS", "JavaScript"], "pink"),
    ("portfolio", "Portfolio V2", "Developer site", ["Modular portfolio with reusable components,", "custom hooks, parallax and scroll animation."], ["React", "Vite", "Tailwind"], "mint"),
    ("mercatora", "Mercatora", "Management system", ["Mall management system with a secure admin", "dashboard for shops and listings."], ["Vanilla JS", "Vite", "Firebase"], "orange"),
    ("vaultara", "Vaultara", "Gov-tech", ["Privacy-first platform to securely store,", "manage and share citizen documents."], ["Firebase", "HTML", "Security"], "lavender"),
    ("aura", "Aura-PA", "AI assistant", ["Adaptive University and Routine Assistant that", "plans around a student's day."], ["TypeScript", "AI"], "cobalt"),
    ("stranger", "Stranger Things S5", "Fan experience", ["Cinematic fan site with GSAP parallax, a Hawkins", "Lab archive and a conspiracy board."], ["GSAP", "Tailwind", "HTML"], "pink"),
    ("infographic", "AI Era Infographic", "Interactive page", ["Explore how an AI thinks, with a live code editor", "to generate, edit and run code in the page."], ["JavaScript", "Ace editor"], "mint"),
]


def card(t, slug, title, kind, desc, tech, key):
    col = t[key]
    tint = tint_of(t, col)
    kw = tw(kind.upper(), 12, True) + 28
    chips, x = "", 28
    for c in tech:
        w = tw(c, 13, True) + 24
        chips += (f'<g transform="translate({x} 150)"><rect width="{w}" height="28" rx="14" fill="{tint}"/>'
                  f'<text x="{w / 2}" y="19" text-anchor="middle" font-size="13" font-weight="700" fill="{col}">{esc(c)}</text></g>')
        x += w + 8
    shine = "#FFFFFF" if t is THEMES["light"] else "#FFFFFF"
    shine_op = ".55" if t is THEMES["light"] else ".07"
    defs = '<clipPath id="cc"><rect x="1" y="1" width="578" height="194" rx="26"/></clipPath>'
    body = (
        f'<g clip-path="url(#cc)"><rect width="580" height="196" fill="{t["card"]}"/>'
        f'<circle cx="520" cy="30" r="86" fill="{col}" opacity=".16" {anim("drift", 9, sum(map(ord, slug)) % 5)}/>'
        f'<circle cx="560" cy="170" r="46" fill="{col}" opacity=".12" {anim("drift", 11, 1)}/>'
        f'<g style="animation:sweep 6s ease-in-out {sum(map(ord, slug)) % 4}s infinite"><rect x="-80" y="-20" width="60" height="240" fill="{shine}" opacity="{shine_op}" transform="skewX(-18)"/></g></g>'
        f'<rect x="1" y="1" width="578" height="194" rx="26" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>'
        f'<rect x="28" y="26" width="{kw}" height="26" rx="13" fill="{col}"/>'
        f'<text x="{28 + kw / 2}" y="44" text-anchor="middle" font-size="12" font-weight="800" fill="#fff" letter-spacing="1.2">{esc(kind.upper())}</text>'
        f'<text x="28" y="88" font-size="28" font-weight="800" fill="{t["ink"]}" letter-spacing="-.5">{esc(title)}</text>'
        f'<text x="28" y="112" font-size="15.5" fill="{t["muted"]}">{esc(desc[0])}</text>'
        f'<text x="28" y="133" font-size="15.5" fill="{t["muted"]}">{esc(desc[1])}</text>{chips}'
        f'<g transform="translate(530 34)"><circle r="20" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
        f'<path d="M-7 7 L7 -7 M-4 -7 H7 V4" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )
    return svg(580, 196, body, defs)


# ---------------------------------------------------------------------------- timeline
PATH = [
    ("JUN 2025", "Hotel Kavana", "IT infrastructure intern in Varanasi"),
    ("AUG 2025", "IIT Madras", "AI and algorithmic problem-solving"),
    ("AUG 2025", "MoreYeahs", "Web developer, built GigX"),
    ("OCT 2025", "Unified Mentor", "Full-stack developer, 4 apps shipped"),
    ("AUG 2026", "ShiftsDeal", "Tech head, payments to production"),
    ("AUG 2026", "Masters' Union", "UG Data Science & AI"),
]


def timeline(t):
    cols = accents(t)
    body = (
        f'<line x1="40" y1="170" x2="1160" y2="170" stroke="{t["line"]}" stroke-width="6" stroke-linecap="round"/>'
        f'<line x1="40" y1="170" x2="1160" y2="170" stroke="{t["cobalt"]}" stroke-width="6" stroke-linecap="round" stroke-dasharray="1120" '
        f'style="--len:1120;animation:drawline 2.4s ease-out both"/>'
    )
    for i, (when, who, what) in enumerate(PATH):
        x = 160 + i * 176
        c = cols[i % len(cols)]
        up = i % 2 == 0
        y_text = 52 if up else 232
        ly1, ly2 = (118, 160) if up else (180, 222)
        anchor = "middle"
        body += (
            f'<g style="animation:pop .5s ease-out {.5 + i * .25}s both;transform-box:fill-box;transform-origin:center">'
            f'<line x1="{x}" y1="{ly1}" x2="{x}" y2="{ly2}" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 7"/>'
            f'<circle cx="{x}" cy="170" r="17" fill="{t["bg"]}" stroke="{c}" stroke-width="5"/><circle cx="{x}" cy="170" r="6" fill="{c}"/>'
            f'<text x="{x}" y="{y_text}" text-anchor="{anchor}" font-size="13" font-family="{MONO}" fill="{c}" font-weight="700" letter-spacing="1.5">{when}</text>'
            f'<text x="{x}" y="{y_text + 28}" text-anchor="{anchor}" font-size="22" font-weight="800" fill="{t["ink"]}">{esc(who)}</text>'
            f'<text x="{x}" y="{y_text + 52}" text-anchor="{anchor}" font-size="14" fill="{t["muted"]}">{esc(what)}</text></g>'
        )
    body += (f'<g transform="translate(1160 170)"><circle r="14" fill="{t["orange"]}" opacity=".3" {anim("ring", 2)}/>'
             f'<path d="M-6 -9 L8 0 L-6 9Z" fill="{t["orange"]}"/></g>')
    return svg(1200, 300, body)


# ---------------------------------------------------------------------------- recognition
WINS = [
    ("target", "All-India Rank 54", "10 m air pistol, U-17 Nationals. State rank 34.", "cobalt"),
    ("trophy", "VVM Science Competition 2023", "Regional winner, advanced to the national level.", "yellow"),
    ("code", "Web Wizards, 2nd place", "AFS Tech Ramble, plus a special mention for deployment.", "mint"),
    ("rocket", "Top 100 nationally", "Quiz win that earned an invite to an ISRO satellite launch.", "orange"),
]
TAGS = [("Robowars '25, 2nd", "lavender"), ("G20 MUN press corps", "cobalt"), ("House Captain", "pink"),
        ("CHEMUN, IIMUN, TISB MUN", "orange"), ("Round Square committee", "mint")]


def wins(t):
    body = ""
    for i, (stk, title, sub, key) in enumerate(WINS):
        x, y = (i % 2) * 610, (i // 2) * 170
        col = t[key]
        body += (
            f'<g transform="translate({x} {y})" style="animation:rise .7s ease-out {i * .15}s both">'
            f'<rect x="1" y="1" width="578" height="148" rx="26" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
            f'<circle cx="86" cy="75" r="62" fill="{tint_of(t, col)}"/>'
            + place(STICKERS[stk](i * .3), 86, 75, .78) +
            f'<text x="178" y="66" font-size="24" font-weight="800" fill="{t["ink"]}">{esc(title)}</text>'
            f'<text x="178" y="96" font-size="15.5" fill="{t["muted"]}">{esc(sub)}</text>'
            f'<rect x="178" y="112" width="46" height="5" rx="2.5" fill="{col}"/></g>'
        )
    # tag row
    row1 = TAGS[:3]
    row2 = TAGS[3:]
    for r, row in enumerate([row1, row2]):
        ws = [tw(txt, 18, True) + 34 for txt, _ in row]
        total = sum(ws) + 22 * (len(row) - 1)
        x = (1190 - total) / 2
        for (txt, key), w in zip(row, ws):
            col = t[key]
            body += (
                f'<g transform="translate({x + w / 2} {386 + r * 56}) rotate({(-3, 2.5, -2)[(r * 3 + len(txt)) % 3]})"><g {anim("wobble", 3.4, r * .4 + len(txt) * .05)}>'
                f'<rect x="{-w / 2}" y="-22" width="{w}" height="44" rx="22" fill="{tint_of(t, col)}" stroke="{col}" stroke-width="2"/>'
                f'<text y="6" text-anchor="middle" font-size="18" font-weight="700" fill="{t["ink"]}">{esc(txt)}</text></g></g>'
            )
            x += w + 22
    return svg(1200, 470, f'<g transform="translate(5 5)">{body}</g>')


# ---------------------------------------------------------------------------- footer
def footer(t):
    def wave(y, amp, color, op, dur, delay):
        seg = f"q150 {-amp} 300 0 t300 0"
        d = f"M-600 {y} " + " ".join(["q150 %d 300 0 t300 0" % -amp] * 1) + " t300 0" * 7 + f" V260 H-600Z"
        return (f'<path d="{d}" fill="{color}" opacity="{op}" style="animation:wave {dur}s linear {delay}s infinite"/>')
    body = (
        wave(150, 34, t["cobalt"], .22, 14, 0) + wave(172, 28, t["lavender"], .25, 19, -4) + wave(196, 22, t["mint"], .28, 24, -9)
        + f'<text x="600" y="92" text-anchor="middle" font-size="46" font-weight="800" fill="{t["ink"]}" letter-spacing="-1">Let\'s build something good.</text>'
        f'<text x="600" y="128" text-anchor="middle" font-size="19" fill="{t["muted"]}">Collaborations, ideas and hello messages are all welcome.</text>'
        + place(sticker_rocket(.3), 160, 90, .7) + place(sticker_target(.7), 1040, 92, .62, 8)
        + sparkle(300, 60, 11, P["yellow"], 0) + sparkle(900, 50, 13, P["pink"], .6) + sparkle(250, 130, 9, P["cobalt"], 1.1) + sparkle(960, 138, 9, P["mint"], 1.6)
    )
    return svg(1200, 260, body)


# ---------------------------------------------------------------------------- shared (theme independent)
def board():
    items = (
        place(sticker_chat("hi, I'm Laksh", .2), 175, 72, 1.15, -4)
        + place(sticker_tag("full-stack", P["cobalt"], -6, .1, 22), 430, 52)
        + place(sticker_tag("ai / ml", P["orange"], 5, .5, 22), 585, 98)
        + place(sticker_pin(.3), 760, 80, .8)
        + place(sticker_tag("Varanasi", P["mint"], -4, .9, 20), 760, 178)
        + place(sticker_trophy(.5), 905, 82, .82, 6)
        + place(sticker_status("building at ShiftsDeal", .4), 330, 160, 1.0, -2)
        + place(sticker_tag("ships daily", P["pink"], 6, .2, 20), 585, 188)
        + place(sticker_tag("10 m air pistol", P["lavender"], -5, .6, 20), 1040, 90)
        + place(sticker_tag("Class of 2030", P["yellow"], 4, 1.0, 20, P["ink"]), 1040, 175)
        + sparkle(80, 160, 13, P["yellow"], 0) + sparkle(480, 120, 10, P["pink"], .7) + sparkle(1150, 40, 12, P["cobalt"], 1.2)
        + sparkle(660, 30, 12, P["yellow"], .3) + sparkle(900, 170, 9, P["orange"], 1.5)
    )
    return svg(1200, 240, items)


def pill(label, color, icon, w=196):
    icons = {
        "in": f'<rect x="22" y="14" width="28" height="28" rx="7" fill="#fff"/><text x="36" y="35" text-anchor="middle" font-size="18" font-weight="800" fill="{color}">in</text>',
        "mail": '<rect x="22" y="17" width="28" height="22" rx="5" fill="none" stroke="#fff" stroke-width="3"/><path d="M24 20 L36 30 L48 20" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
        "ig": '<rect x="22" y="14" width="28" height="28" rx="9" fill="none" stroke="#fff" stroke-width="3"/><circle cx="36" cy="28" r="6.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="43.5" cy="20.5" r="2" fill="#fff"/>',
    }
    fill = color if not color.startswith("url") else color
    defs = '<linearGradient id="ig" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FF9F43"/><stop offset=".5" stop-color="#FF4D8D"/><stop offset="1" stop-color="#8B5CF6"/></linearGradient>'
    body = (
        f'<g {anim("float", 4, sum(map(ord, label)) % 3)}><rect x="3" y="3" width="{w - 6}" height="50" rx="25" fill="{fill}" filter="url(#sh)"/>'
        f'{icons[icon]}<text x="68" y="35" font-size="20" font-weight="700" fill="#fff">{esc(label)}</text></g>'
    )
    return svg(w, 64, body, defs)


# ---------------------------------------------------------------------------- run
def main():
    for name, t in THEMES.items():
        write(name, "banner.svg", banner(t))
        write(name, "now.svg", now(t))
        write(name, "stack.svg", stack(t))
        write(name, "timeline.svg", timeline(t))
        write(name, "wins.svg", wins(t))
        write(name, "footer.svg", footer(t))
        for i, (num, title, key) in enumerate([("01", "About", "cobalt"), ("02", "Right now", "mint"), ("03", "Toolbox", "orange"),
                                               ("04", "Selected work", "lavender"), ("05", "The path so far", "pink"),
                                               ("06", "Wins", "yellow"), ("07", "By the numbers", "cobalt")]):
            write(name, f"h{num}.svg", heading(t, num, title, t[key]))
        for c in CARDS:
            write(name, f"card-{c[0]}.svg", card(t, *c))
    write("shared", "board.svg", board())
    write("shared", "pill-linkedin.svg", pill("LinkedIn", "#0A66C2", "in"))
    write("shared", "pill-email.svg", pill("Email me", "#FF7A3D", "mail"))
    write("shared", "pill-instagram.svg", pill("Instagram", "url(#ig)", "ig"))
    print("assets built")


if __name__ == "__main__":
    main()
