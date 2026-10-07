"""Text as SVG outlines (identical on every device) plus a typewriter helper. Fonts are SIL OFL, see scripts/fonts."""
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = os.path.join(os.path.dirname(__file__), "fonts")


class Face:
    def __init__(self, filename):
        self.font = TTFont(os.path.join(FONTS, filename))
        self.gs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upm = self.font["head"].unitsPerEm
        self.hmtx = self.font["hmtx"]

    def width(self, text, size, tracking=0):
        s = size / self.upm
        return sum(self.hmtx[self.cmap.get(ord(c), self.cmap[ord("?")])][0] * s + tracking for c in text)

    def glyphs(self, text, size, x, y, tracking=0):
        s = size / self.upm
        out = []
        for ch in text:
            gn = self.cmap.get(ord(ch), self.cmap[ord("?")])
            if ch != " ":
                pen = SVGPathPen(self.gs, ntos=lambda v: f"{v:.1f}")
                self.gs[gn].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
                out.append(pen.getCommands())
            x += self.hmtx[gn][0] * s + tracking
        return out, x


def txt(face, text, size, x, y, fill, tracking=0, anchor="l", extra="", style=""):
    """One <path> for a whole string. anchor: l, m, r. Returns (svg, width)."""
    w = face.width(text, size, tracking)
    if anchor == "m":
        x -= w / 2
    elif anchor == "r":
        x -= w
    paths, _ = face.glyphs(text, size, x, y, tracking)
    return f'<path d="{"".join(paths)}" fill="{fill}" {extra} style="{style}"/>', w


def reveal(face, text, size, x, y, fill, delay=0.0, step=.035, dur=.5, tracking=0, anim="rise"):
    """Per-letter staggered reveal (CSS animation, runs once)."""
    paths, end = face.glyphs(text, size, x, y, tracking)
    return "".join(f'<path d="{d}" fill="{fill}" style="animation:{anim} {dur}s ease-out {delay + i * step:.2f}s both"/>' for i, d in enumerate(paths)), end


def typed(uid, face, x, y, text, begin, per, size, fill, cursor, loop, keep_cursor=False, tracking=0):
    """Typewriter line driven by SMIL. Needs an <animate id="loop" .../> element in the document.
    Fixed advance per character, so the face should be monospaced. Returns (clipPath, text, cursor)."""
    n = len(text)
    cw = face.width("M", size, tracking)
    dur = n * per
    xs = ";".join(f"{x + i * cw:.1f}" for i in range(n + 1))
    ws = ";".join(f"{i * cw:.1f}" for i in range(n + 1))
    b = f"loop.begin+{begin}s"
    cur = (f'<rect y="{y - size * .82:.1f}" width="{cw * .9:.1f}" height="{size * .98:.1f}" fill="{cursor}" opacity="0">'
           f'<animate attributeName="x" values="{xs}" calcMode="discrete" dur="{dur:.2f}s" begin="{b}" fill="freeze"/>'
           f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;.999;1" calcMode="discrete" dur="{dur:.2f}s" begin="{b}"/>')
    if keep_cursor:
        end = begin + dur
        cur += (f'<animate attributeName="opacity" values="1;0" keyTimes="0;.5" calcMode="discrete" dur="1s" '
                f'begin="loop.begin+{end:.2f}s" repeatDur="{loop - end:.2f}s"/>')
    cur += "</rect>"
    clip = (f'<clipPath id="c{uid}"><rect x="{x}" y="{y - size}" height="{size * 1.4:.1f}" width="{n * cw:.1f}">'
            f'<set attributeName="width" to="0" begin="loop.begin"/>'
            f'<animate attributeName="width" values="{ws}" calcMode="discrete" dur="{dur:.2f}s" begin="{b}" fill="freeze"/></rect></clipPath>')
    paths, _ = face.glyphs(text, size, x, y, tracking)
    t = f'<path d="{"".join(paths)}" fill="{fill}" clip-path="url(#c{uid})"/>'
    return clip, t, cur
