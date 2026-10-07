"""Shared helpers for the profile README graphics: themes, text sizing, animated stickers."""
from xml.sax.saxutils import escape

FONT = "'Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,Menlo,monospace"

THEMES = {
    "light": dict(
        ink="#0B1B3A", muted="#5B6B8C", card="#F6F8FF", card2="#EDF1FF", line="#DCE3F5", bg="#FFFFFF",
        cobalt="#2F5BFF", orange="#FF7A3D", mint="#14B38A", lavender="#8B7CFF", pink="#FF6FA8", yellow="#FFC93C",
        tint_cobalt="#E3EAFF", tint_orange="#FFE9DD", tint_mint="#D8F5EC", tint_lav="#ECE9FF", tint_pink="#FFE3EE", tint_yellow="#FFF2CC",
    ),
    "dark": dict(
        ink="#E8EEFF", muted="#8FA0C4", card="#121A2E", card2="#17213A", line="#25304D", bg="#0D1117",
        cobalt="#6C8CFF", orange="#FF8F5C", mint="#3DD6AE", lavender="#A99BFF", pink="#FF8DBB", yellow="#FFD25E",
        tint_cobalt="#1B2850", tint_orange="#3A2418", tint_mint="#14352E", tint_lav="#272150", tint_pink="#3B1B2B", tint_yellow="#3A3015",
    ),
}

try:
    from PIL import ImageFont

    _fonts = {}

    def tw(text, size, bold=False):
        key = (size, bold)
        if key not in _fonts:
            _fonts[key] = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", size)
        return _fonts[key].getlength(text) * 1.04
except Exception:  # pragma: no cover
    def tw(text, size, bold=False):
        return len(text) * size * (0.6 if bold else 0.56)


def esc(s):
    return escape(s, {'"': "&quot;"})


CSS = """
.fb{transform-box:fill-box;transform-origin:center}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
@keyframes wobble{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.14)}}
@keyframes twinkle{0%,100%{transform:scale(.3);opacity:.25}50%{transform:scale(1);opacity:1}}
@keyframes flame{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.6)}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes ring{0%{transform:scale(.7);opacity:.7}100%{transform:scale(1.45);opacity:0}}
@keyframes dart{0%{transform:translate(34px,-34px);opacity:0}14%{transform:translate(0,0);opacity:1}86%{transform:translate(0,0);opacity:1}100%{transform:translate(0,0);opacity:0}}
@keyframes typeline{0%{transform:scaleX(0)}30%,88%{transform:scaleX(1)}100%{transform:scaleX(0)}}
@keyframes bounce{0%,100%{transform:translateY(0)}45%{transform:translateY(-16px)}}
@keyframes shadow{0%,100%{transform:scale(1);opacity:.28}45%{transform:scale(.6);opacity:.12}}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(26px,-18px)}}
@keyframes drawline{from{stroke-dashoffset:var(--len)}to{stroke-dashoffset:0}}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}
@keyframes sweep{0%{transform:translateX(-140%)}60%,100%{transform:translateX(260%)}}
@keyframes spinslow{to{transform:rotate(360deg)}}
@keyframes wave{to{transform:translateX(-600px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def svg(width, height, body, defs="", extra_css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'font-family="{FONT}" role="img">'
        f"<style>{CSS}{extra_css}</style><defs>"
        '<filter id="sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#0B1B3A" flood-opacity=".22"/></filter>'
        f"{defs}</defs>{body}</svg>"
    )


def anim(cls, dur, delay=0, extra=""):
    return f'class="fb {cls}" style="animation:{cls} {dur}s ease-in-out {delay}s infinite;{extra}"'


# --------------------------------------------------------------------------------------
# Stickers: die-cut look (white outline + soft shadow). Colours are fixed so they read on
# both the light and the dark page.  Each returns a <g> centred on 0,0, roughly 120 px wide.
# --------------------------------------------------------------------------------------
P = dict(ink="#0B1B3A", cobalt="#2F5BFF", orange="#FF7A3D", mint="#14B38A", lavender="#8B7CFF",
         pink="#FF6FA8", yellow="#FFC93C", white="#FFFFFF", paper="#F1F4FF")


def place(inner, x, y, s=1.0, rot=0):
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">{inner}</g>'


def sparkle(x, y, size=14, color=P["yellow"], delay=0, dur=2.6):
    s = size
    path = f"M0 {-s} Q0 0 {s} 0 Q0 0 0 {s} Q0 0 {-s} 0 Q0 0 0 {-s}Z"
    return (f'<g transform="translate({x} {y})"><path d="{path}" fill="{color}" stroke="#fff" stroke-width="2.5" stroke-linejoin="round" '
            f'{anim("twinkle", dur, delay)}/></g>')


def sticker_target(delay=0):
    return (
        f'<g {anim("float", 5, delay)}><g filter="url(#sh)">'
        f'<circle r="56" fill="#fff"/><circle r="47" fill="{P["cobalt"]}"/><circle r="35" fill="#fff"/>'
        f'<circle r="24" fill="{P["orange"]}"/><circle r="12" fill="#fff"/><circle r="5" fill="{P["ink"]}"/></g>'
        f'<circle r="47" fill="none" stroke="{P["cobalt"]}" stroke-width="3" {anim("ring", 2.4, delay)}/>'
        f'<g class="fb" style="animation:dart 4.4s ease-out {delay}s infinite">'
        f'<line x1="62" y1="-62" x2="6" y2="-6" stroke="{P["ink"]}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M62 -62 L46 -64 L50 -50Z M54 -54 L38 -56 L42 -42Z" fill="{P["pink"]}" stroke="#fff" stroke-width="2"/></g></g>'
    )


def sticker_rocket(delay=0):
    body = "M0 -54 C24 -32 24 6 15 32 L-15 32 C-24 6 -24 -32 0 -54Z"
    return (
        f'<g {anim("float", 4.2, delay)}><g transform="rotate(40)" filter="url(#sh)">'
        f'<path d="M-7 32 Q0 70 7 32Z" fill="{P["orange"]}" stroke="#fff" stroke-width="6" stroke-linejoin="round" '
        f'style="transform-box:fill-box;transform-origin:50% 0;animation:flame .45s ease-in-out infinite"/>'
        f'<path d="M-15 12 L-34 40 L-15 32Z M15 12 L34 40 L15 32Z" fill="{P["pink"]}" stroke="#fff" stroke-width="8" stroke-linejoin="round"/>'
        f'<path d="{body}" fill="#fff" stroke="#fff" stroke-width="12" stroke-linejoin="round"/>'
        f'<path d="{body}" fill="{P["paper"]}"/>'
        f'<path d="M0 -54 C13 -43 18 -33 20 -24 L-20 -24 C-18 -33 -13 -43 0 -54Z" fill="{P["orange"]}"/>'
        f'<circle cy="-8" r="10" fill="{P["cobalt"]}" stroke="#fff" stroke-width="4"/>'
        f'<rect x="-15" y="24" width="30" height="8" fill="{P["ink"]}" opacity=".12"/></g></g>'
    )


def sticker_code(delay=0):
    lines = [(-30, 52, P["mint"], 0), (-14, 74, P["lavender"], .35), (2, 40, P["orange"], .7), (18, 62, P["yellow"], 1.05)]
    ls = "".join(
        f'<rect x="-44" y="{y}" width="{w}" height="7" rx="3.5" fill="{c}" style="transform-box:fill-box;transform-origin:0 50%;'
        f'animation:typeline 4.2s ease-in-out {delay + d}s infinite"/>' for y, w, c, d in lines
    )
    return (
        f'<g {anim("float", 4.8, delay)}><g filter="url(#sh)">'
        f'<rect x="-62" y="-48" width="124" height="96" rx="18" fill="#fff"/>'
        f'<rect x="-54" y="-40" width="108" height="80" rx="12" fill="{P["ink"]}"/>'
        f'<path d="M-54 -28 a12 12 0 0 1 12 -12 h84 a12 12 0 0 1 12 12 v4 h-108z" fill="#1C2F5C"/>'
        f'<circle cx="-42" cy="-32" r="3.6" fill="{P["orange"]}"/><circle cx="-31" cy="-32" r="3.6" fill="{P["yellow"]}"/>'
        f'<circle cx="-20" cy="-32" r="3.6" fill="{P["mint"]}"/></g>{ls}'
        f'<rect x="-44" y="32" width="9" height="3.5" fill="#fff" style="animation:blink 1s steps(1) infinite"/></g>'
    )


def sticker_ai(delay=0):
    layers = [(-30, [-22, 22]), (0, [-34, 0, 34]), (30, [-22, 22])]
    lines = ""
    for i in range(len(layers) - 1):
        for y1 in layers[i][1]:
            for y2 in layers[i + 1][1]:
                lines += f'<line x1="{layers[i][0]}" y1="{y1}" x2="{layers[i + 1][0]}" y2="{y2}" stroke="#fff" stroke-width="2" opacity=".55"/>'
    nodes = ""
    k = 0
    for x, ys in layers:
        for y in ys:
            nodes += (f'<circle cx="{x}" cy="{y}" r="7" fill="#fff" '
                      f'style="transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-in-out {delay + k * .22}s infinite"/>')
            k += 1
    return (
        f'<g {anim("float", 5.4, delay)}><g filter="url(#sh)"><circle r="56" fill="#fff"/><circle r="48" fill="{P["lavender"]}"/></g>'
        f"{lines}{nodes}</g>"
    )


def sticker_pin(delay=0):
    path = "M0 -50 C-27 -50 -36 -23 -36 -12 C-36 12 0 46 0 46 C0 46 36 12 36 -12 C36 -23 27 -50 0 -50Z"
    return (
        f'<g><ellipse cy="58" rx="26" ry="6" fill="{P["ink"]}" {anim("shadow", 1.8, delay)}/>'
        f'<g {anim("bounce", 1.8, delay)}><g filter="url(#sh)"><path d="{path}" fill="#fff" stroke="#fff" stroke-width="12" stroke-linejoin="round"/>'
        f'<path d="{path}" fill="{P["orange"]}"/><circle cy="-12" r="14" fill="#fff"/><circle cy="-12" r="6" fill="{P["orange"]}"/></g></g></g>'
    )


def sticker_trophy(delay=0):
    cup = "M-28 -40 H28 V-10 C28 14 14 26 0 26 C-14 26 -28 14 -28 -10Z"
    return (
        f'<g {anim("float", 4.6, delay)}><g filter="url(#sh)">'
        f'<path d="M-28 -32 C-52 -32 -50 -2 -26 4 M28 -32 C52 -32 50 -2 26 4" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round"/>'
        f'<path d="M-28 -32 C-52 -32 -50 -2 -26 4 M28 -32 C52 -32 50 -2 26 4" fill="none" stroke="{P["yellow"]}" stroke-width="7" stroke-linecap="round"/>'
        f'<rect x="-9" y="22" width="18" height="22" fill="#fff" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>'
        f'<rect x="-30" y="42" width="60" height="14" rx="5" fill="#fff" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>'
        f'<path d="{cup}" fill="#fff" stroke="#fff" stroke-width="12" stroke-linejoin="round"/>'
        f'<path d="{cup}" fill="{P["yellow"]}"/><rect x="-9" y="22" width="18" height="22" fill="{P["orange"]}"/>'
        f'<rect x="-30" y="42" width="60" height="14" rx="5" fill="{P["cobalt"]}"/></g>'
        f'<path d="M-17 -30 V-8 C-17 2 -12 9 -6 12" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
        f'{sparkle(30, -42, 11, "#fff", delay)}</g>'
    )


def sticker_chat(text="hi, I'm Laksh", delay=0, color=P["cobalt"]):
    w = tw(text, 24, True) + 40
    return (
        f'<g {anim("wobble", 3.2, delay)}><g filter="url(#sh)">'
        f'<path d="M{-w / 2} -26 h{w} a14 14 0 0 1 14 14 v20 a14 14 0 0 1 -14 14 h{-(w / 2 - 12)} l-14 16 l2 -16 h{-(w / 2 - 2)} a14 14 0 0 1 -14 -14 v-20 a14 14 0 0 1 14 -14z" '
        f'transform="translate(0 -4)" fill="#fff" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>'
        f'<path d="M{-w / 2} -26 h{w} a14 14 0 0 1 14 14 v20 a14 14 0 0 1 -14 14 h{-(w / 2 - 12)} l-14 16 l2 -16 h{-(w / 2 - 2)} a14 14 0 0 1 -14 -14 v-20 a14 14 0 0 1 14 -14z" '
        f'transform="translate(0 -4)" fill="{color}"/></g>'
        f'<text y="1" text-anchor="middle" font-size="24" font-weight="700" fill="#fff">{esc(text)}</text></g>'
    )


def sticker_tag(text, color, rot=-4, delay=0, size=20, txt="#fff"):
    w = tw(text, size, True) + 30
    h = size + 22
    return (
        f'<g transform="rotate({rot})"><g {anim("wobble", 3.6, delay)}><g filter="url(#sh)">'
        f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="#fff" stroke="#fff" stroke-width="8"/>'
        f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{color}"/></g>'
        f'<text y="{size * .35}" text-anchor="middle" font-size="{size}" font-weight="700" fill="{txt}">{esc(text)}</text></g></g>'
    )


def sticker_status(text, delay=0):
    w = tw(text, 20, True) + 66
    return (
        f'<g {anim("float", 5, delay)}><g filter="url(#sh)">'
        f'<rect x="{-w / 2}" y="-24" width="{w}" height="48" rx="24" fill="#fff" stroke="#fff" stroke-width="8"/></g>'
        f'<circle cx="{-w / 2 + 24}" cy="0" r="14" fill="{P["mint"]}" opacity=".25" {anim("ring", 1.8, delay)}/>'
        f'<circle cx="{-w / 2 + 24}" cy="0" r="7" fill="{P["mint"]}"/>'
        f'<text x="{-w / 2 + 42}" y="7" font-size="20" font-weight="700" fill="{P["ink"]}">{esc(text)}</text></g>'
    )


STICKERS = dict(target=sticker_target, rocket=sticker_rocket, code=sticker_code, ai=sticker_ai,
                pin=sticker_pin, trophy=sticker_trophy)


def theme_css(t):
    return ""
