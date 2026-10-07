"""Draws the live GitHub numbers (stats tiles, contribution heatmap, language bar) as themed SVGs.

Runs in the 'Refresh stats' GitHub Action with the built-in GITHUB_TOKEN, no third-party services.
Locally:  GITHUB_TOKEN=$(gh auth token) python scripts/build_stats.py
"""
import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import THEMES, anim, esc, svg, tw  # noqa: E402

LOGIN = os.environ.get("PROFILE_LOGIN", "TheRealLaksh")
ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")

QUERY = """
query($login:String!){user(login:$login){
  repositories(ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false,first:100){
    totalCount nodes{languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}
  contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}
}}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]


def tiles(t, nums):
    items = [("Contributions in the last year", nums["total"], t["cobalt"]), ("Days with activity", nums["active"], t["orange"]),
             ("Busiest day, contributions", nums["best"], t["mint"]), ("Public repositories", nums["repos"], t["lavender"])]
    body = ""
    for i, (label, val, col) in enumerate(items):
        x = i * 296
        body += (
            f'<g transform="translate({x} 0)" style="animation:rise .7s ease-out {i * .12}s both">'
            f'<rect x="1" y="1" width="272" height="128" rx="24" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
            f'<rect x="24" y="26" width="36" height="6" rx="3" fill="{col}"/>'
            f'<text x="24" y="86" font-size="54" font-weight="800" fill="{t["ink"]}" letter-spacing="-2">{val:,}</text>'
            f'<text x="24" y="112" font-size="14.5" fill="{t["muted"]}">{esc(label)}</text></g>'
        )
    return svg(1200, 132, f'<g transform="translate(8 0)">{body}</g>')


def heatmap(t, weeks, total):
    cell, gap = 15, 4
    step = cell + gap
    nz = sorted(d["contributionCount"] for w in weeks for d in w["contributionDays"] if d["contributionCount"])
    q = [nz[int(len(nz) * f)] for f in (.25, .5, .75)] if nz else [1, 2, 3]
    x0, y0 = (1200 - len(weeks) * step + gap) / 2, 74
    cells = ""
    months = ""
    last_month = None
    for wi, w in enumerate(weeks):
        first = w["contributionDays"][0]["date"]
        m = dt.date.fromisoformat(first).strftime("%b")
        if m != last_month and wi < len(weeks) - 2:
            months += f'<text x="{x0 + wi * step}" y="{y0 - 12}" font-size="13" fill="{t["muted"]}">{m}</text>'
            last_month = m
        for d in w["contributionDays"]:
            wd = dt.date.fromisoformat(d["date"]).weekday()
            row = (wd + 1) % 7  # Sunday first, like GitHub
            c = d["contributionCount"]
            lvl = 0 if c == 0 else 1 + sum(c > x for x in q)
            fill = t["card2"] if lvl == 0 else t["cobalt"]
            op = [1, .3, .55, .8, 1][lvl]
            cells += (
                f'<rect x="{x0 + wi * step:.0f}" y="{y0 + row * step}" width="{cell}" height="{cell}" rx="4" fill="{fill}" fill-opacity="{op}" '
                f'style="transform-box:fill-box;transform-origin:center;animation:pop .45s ease-out {wi * .018:.2f}s both"><title>{d["date"]}: {c}</title></rect>'
            )
    legend = ""
    lx = 1200 - x0 - 5 * step - 60
    legend += f'<text x="{lx - 40}" y="{y0 + 7 * step + 22}" font-size="13" fill="{t["muted"]}">Less</text>'
    for i in range(5):
        fill = t["card2"] if i == 0 else t["cobalt"]
        legend += f'<rect x="{lx + i * step}" y="{y0 + 7 * step + 10}" width="{cell}" height="{cell}" rx="4" fill="{fill}" fill-opacity="{[1, .3, .55, .8, 1][i]}"/>'
    legend += f'<text x="{lx + 5 * step + 6}" y="{y0 + 7 * step + 22}" font-size="13" fill="{t["muted"]}">More</text>'
    body = (
        f'<rect x="1" y="1" width="1198" height="{y0 + 7 * step + 46}" rx="26" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
        f'<text x="{x0}" y="36" font-size="22" font-weight="800" fill="{t["ink"]}">{total:,} contributions in the last year</text>{months}{cells}{legend}'
    )
    return svg(1200, y0 + 7 * step + 48, body)


def languages(t, repos):
    sizes = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:6]
    tot = sum(v for _, v in sizes.items()) or 1
    cols = [t["cobalt"], t["orange"], t["mint"], t["lavender"], t["pink"], t["yellow"]]
    x, bar, leg = 40, "", ""
    width = 1120
    shown = sum(v for _, v in top)
    for i, (name, v) in enumerate(top):
        w = width * v / shown
        bar += (f'<rect x="{x:.1f}" y="70" width="{max(w - 4, 2):.1f}" height="26" rx="13" fill="{cols[i]}" '
                f'style="transform-box:fill-box;transform-origin:0 50%;animation:grow 1.1s ease-out {i * .12}s both"/>')
        x += w
        lx, ly = 40 + (i % 3) * 380, 140 + (i // 3) * 34
        leg += (f'<circle cx="{lx + 8}" cy="{ly - 5}" r="8" fill="{cols[i]}"/><text x="{lx + 28}" y="{ly}" font-size="18" font-weight="700" fill="{t["ink"]}">{esc(name)}</text>'
                f'<text x="{lx + 28 + tw(name, 18, True) + 10}" y="{ly}" font-size="16" fill="{t["muted"]}">{100 * v / tot:.1f}%</text>')
    body = (f'<rect x="1" y="1" width="1198" height="226" rx="26" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
            f'<text x="40" y="44" font-size="22" font-weight="800" fill="{t["ink"]}">Languages across my public repos</text>{bar}{leg}')
    return svg(1200, 230, body)


def main():
    u = fetch()
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    nums = dict(total=cal["totalContributions"], active=sum(1 for d in days if d["contributionCount"]),
                best=max(d["contributionCount"] for d in days), repos=u["repositories"]["totalCount"])
    for name, t in THEMES.items():
        d = os.path.join(ROOT, name)
        os.makedirs(d, exist_ok=True)
        for fn, content in (("stats.svg", tiles(t, nums)), ("heatmap.svg", heatmap(t, weeks, nums["total"])),
                            ("langs.svg", languages(t, u["repositories"]["nodes"]))):
            with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                f.write(content)
    print("stats built", nums)


if __name__ == "__main__":
    main()
