"""Generate the README artwork (black & white manga, night theme).

Run: python scripts/gen_assets.py  ->  writes assets/*.svg
Data: my GitHub contribution calendar (last 12 months, private repos counted anonymously).
Auth: GITHUB_TOKEN / GH_TOKEN, or `gh auth token` when run locally. Stdlib only.
"""
import collections
import datetime as dt
import html
import json
import os
import pathlib
import random
import subprocess
import urllib.request

LOGIN = os.environ.get("GH_LOGIN", "LorenzoMarty")
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

INK, PAPER, TONE, GREY = "#0d0d0d", "#fbfbf8", "#d6d6d1", "#8c8c88"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
HEAVY = "Impact,'Arial Black','Helvetica Neue',sans-serif"
MONO = "SFMono-Regular,Consolas,'Liberation Mono',monospace"
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

DEFS = f"""<defs>
<pattern id="tone" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="2.5" cy="2.5" r="1" fill="{INK}" fill-opacity=".22"/></pattern>
<pattern id="nightTone" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="2.5" cy="2.5" r="1" fill="#fff" fill-opacity=".13"/></pattern>
</defs>"""


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{DEFS}{body}</svg>')


def star4(x, y, r, fill):
    return f'<path transform="translate({x:.1f},{y:.1f})" d="M0,{-r}Q0,0 {r},0Q0,0 0,{r}Q0,0 {-r},0Q0,0 0,{-r}Z" fill="{fill}"/>'


# ---- data: GitHub contribution calendar ------------------------------------
QUERY = """query($login: String!) { user(login: $login) { contributionsCollection {
  contributionCalendar { weeks { contributionDays { date contributionCount } } } } } }"""


def fetch_calendar():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") \
        or subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "night-log"})
    res = json.load(urllib.request.urlopen(req))
    if "errors" in res:
        raise SystemExit(res["errors"])
    weeks = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return {dt.date.fromisoformat(d["date"]): d["contributionCount"] for w in weeks for d in w["contributionDays"]}


cal = fetch_calendar()
days = sorted(cal)
first, TODAY = days[0], days[-1]
active = [d for d in days if cal[d]]
active_set = set(active)
per_month = collections.Counter((d.year, d.month) for d in active)


def streaks():
    best = cur = 0
    best_end = days[0]
    for d in days:
        cur = cur + 1 if d in active_set else 0
        if cur > best:
            best, best_end = cur, d
    i = len(days) - 1
    if days[i] not in active_set:  # today may not have a contribution yet
        i -= 1
    now = 0
    while i >= 0 and days[i] in active_set:
        now, i = now + 1, i - 1
    return best, best_end, now


week = lambda d: d - dt.timedelta(days=d.weekday())
weeks_total = len({week(d) for d in days})
weeks_active = len({week(d) for d in active})
best_streak, best_end, now_streak = streaks()
months = []
y, m = TODAY.year, TODAY.month
for _ in range(12):
    months.append((y, m))
    y, m = (y, m - 1) if m > 1 else (y - 1, 12)
months.reverse()


# ---- banner: manga cover, night panel with one lit window -------------------
def banner():
    rng, W, H = random.Random(11), 900, 180
    panel = "612,3 897,3 897,177 572,177"
    b = f'<rect x="1.5" y="1.5" width="897" height="177" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
    b += f'<polygon points="330,3 590,3 550,177 300,177" fill="url(#tone)" opacity=".55"/>'
    b += "".join(f'<line x1="{20+i*34}" y1="176" x2="{60+i*34}" y2="150" stroke="{TONE}" stroke-width="1.2"/>' for i in range(8))
    # night panel
    b += f'<clipPath id="np"><polygon points="{panel}"/></clipPath><g clip-path="url(#np)"><rect x="560" width="340" height="{H}" fill="#242424"/><rect x="560" width="340" height="{H}" fill="url(#nightTone)"/>'
    for _ in range(45):
        b += f'<circle cx="{rng.uniform(600,895):.0f}" cy="{rng.uniform(6,110):.0f}" r="{rng.uniform(.6,1.5):.1f}" fill="#fff" opacity="{rng.uniform(.5,1):.2f}"/>'
    b += '<circle cx="820" cy="52" r="24" fill="#fff"/><circle cx="811" cy="45" r="5" fill="#d0d0cc"/><circle cx="828" cy="60" r="3.5" fill="#d0d0cc"/>'
    x = 560
    while x < 900:
        w, h = rng.randint(24, 52), rng.randint(36, 96)
        b += f'<rect x="{x}" y="{H-h}" width="{w}" height="{h}" fill="#000"/>'
        for wx in range(x + 5, x + w - 6, 9):
            for wy in range(H - h + 7, H - 6, 12):
                if rng.random() < .22:
                    b += f'<rect x="{wx}" y="{wy}" width="3.5" height="5" fill="#fff" opacity=".85"/>'
        x += w + rng.randint(0, 4)
    b += ('<rect x="694" y="132" width="10" height="13" fill="#fff"/>'
          + "".join(f'<line x1="{699+dx*9}" y1="{138.5+dy*9}" x2="{699+dx*15}" y2="{138.5+dy*15}" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>'
                    for dx, dy in [(-1, -1), (0, -1.2), (1, -1), (-1.2, 0), (1.2, 0)])
          + '</g>')
    b += f'<polygon points="{panel}" fill="none" stroke="{INK}" stroke-width="3"/>'
    # text + speech bubble
    tag = "tracing, evaluating and budgeting LLMs, mostly after dark."
    b += (f'<text x="40" y="36" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{GREY}">CHAPTER 00 · PROLOGUE</text>'
          f'<text x="43" y="87" font-family="{HEAVY}" font-size="52" font-style="italic" fill="{TONE}">LORENZO MARTY</text>'
          f'<text x="40" y="84" font-family="{HEAVY}" font-size="52" font-style="italic" fill="{INK}">LORENZO MARTY</text>'
          f'<text x="41" y="108" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="1.5" fill="{INK}">AI &amp; LLMOPS ENGINEER</text>'
          f'<polygon points="500,128 566,150 500,146" fill="{PAPER}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
          f'<rect x="38" y="120" width="464" height="38" rx="19" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
          f'<line x1="501.5" y1="129" x2="501.5" y2="145" stroke="{PAPER}" stroke-width="3"/>'
          f'<text x="270" y="144" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{INK}">{tag}</text>')
    return svg(W, H, b, "Lorenzo Marty, AI and LLMOps engineer — manga-style cover with a night skyline and one window still lit")


# ---- chapter strip -----------------------------------------------------------
def chapter(n, title):
    b = (f'<rect x="1.5" y="1.5" width="897" height="27" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
         f'<polygon points="1.5,1.5 96,1.5 84,28.5 1.5,28.5" fill="{INK}"/>'
         f'<text x="14" y="20" font-family="{MONO}" font-size="13" font-weight="700" fill="{PAPER}">CH.{n:02d}</text>'
         f'<text x="110" y="22" font-family="{HEAVY}" font-size="17" font-style="italic" letter-spacing=".5" fill="{INK}">{html.escape(title.upper())}</text>'
         + "".join(f'<line x1="{790+i*11}" y1="28" x2="{804+i*11}" y2="3" stroke="{GREY}" stroke-width="1.2"/>' for i in range(9)))
    return svg(900, 30, b, f"Chapter {n}: {html.escape(title)}")


# ---- night log: stats | monthly skyline | star map ---------------------------
def nightlog():
    rng, W, H = random.Random(5), 900, 250
    b = ""
    # A: stats (paper)
    b += f'<rect x="1.5" y="1.5" width="262" height="{H-3}" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
    b += f'<polygon points="263,{H-2} 120,{H-2} 263,{H-90}" fill="url(#tone)" opacity=".5"/>'
    b += f'<line x1="132" y1="10" x2="132" y2="{H-10}" stroke="{INK}" stroke-width="1.5"/><line x1="10" y1="{H/2}" x2="255" y2="{H/2}" stroke="{INK}" stroke-width="1.5"/>'
    for i, (n, label, sub) in enumerate([(len(active), "ACTIVE DAYS", "last 12 months"),
                                          (best_streak, "LONGEST STREAK", f"days, ended {best_end.day} {MON[best_end.month-1]}"),
                                          (now_streak, "CURRENT STREAK", "days in a row"),
                                          (weeks_active, "ACTIVE WEEKS", f"of {weeks_total}")]):
        x, y = 16 + (i % 2) * 122, 16 + (i // 2) * (H / 2 - 2)
        b += (f'<text x="{x+2}" y="{y+56}" font-family="{HEAVY}" font-size="50" font-style="italic" fill="{TONE}">{n}</text>'
              f'<text x="{x}" y="{y+53}" font-family="{HEAVY}" font-size="50" font-style="italic" fill="{INK}">{n}</text>'
              f'<text x="{x}" y="{y+76}" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="1.5" fill="{INK}">{label}</text>'
              f'<text x="{x}" y="{y+92}" font-family="{SANS}" font-size="10.5" fill="{GREY}">{sub}</text>')
    # B: skyline, active days per month (night)
    bx = 271
    b += f'<rect x="{bx}" y="1.5" width="318" height="{H-3}" fill="#242424" stroke="{INK}" stroke-width="3"/><rect x="{bx}" y="1.5" width="318" height="{H-3}" fill="url(#nightTone)"/>'
    b += f'<text x="{bx+14}" y="24" font-family="{MONO}" font-size="10.5" letter-spacing="1.5" fill="#fff">ACTIVE DAYS / MONTH</text>'
    base, bw, step = 222, 20, 25
    for i, ym in enumerate(months):
        n, partial = per_month[ym], ym == months[-1]
        h, x = max(round(n / 31 * 150), 10), bx + 12 + i * step
        dash = ' stroke-dasharray="3 2"' if partial else ""
        b += f'<rect x="{x}" y="{base-h}" width="{bw}" height="{h}" fill="#000" stroke="#fff" stroke-width="1.5"{dash}/>'
        for wx in range(x + 4, x + bw - 5, 8):
            for wy in range(base - h + 6, base - 5, 11):
                if rng.random() < .72:
                    b += f'<rect x="{wx}" y="{wy}" width="4" height="5.5" fill="#fff" opacity=".9"/>'
        b += (f'<text x="{x+bw/2}" y="{base-h-6}" text-anchor="middle" font-family="{HEAVY}" font-size="12" font-style="italic" fill="#fff">{n}</text>'
              f'<text x="{x+bw/2}" y="{base+15}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="#bbb">{MON[ym[1]-1]}</text>')
    b += f'<line x1="{bx+8}" y1="{base}" x2="{bx+310}" y2="{base}" stroke="#fff" stroke-opacity=".5"/>'
    # C: pulse of the year, rolling 30-day active-day rate (night)
    cx = 597
    b += f'<rect x="{cx}" y="1.5" width="301.5" height="{H-3}" fill="#242424" stroke="{INK}" stroke-width="3"/><rect x="{cx}" y="1.5" width="301.5" height="{H-3}" fill="url(#nightTone)"/>'
    b += f'<text x="{cx+14}" y="24" font-family="{MONO}" font-size="10.5" letter-spacing="1.5" fill="#fff">PULSE OF THE YEAR</text>'
    x0, x1, top, base = cx + 16, cx + 289, 44, 205
    n = len(days)
    win, s, roll = collections.deque(), 0, []
    for d in days:
        win.append(1 if d in active_set else 0)
        s += win[-1]
        if len(win) > 30:
            s -= win.popleft()
        roll.append(s)
    vmax = max(max(roll) * 1.15, 1)
    xf = lambda i: x0 + (i / (n - 1) * (x1 - x0) if n > 1 else 0)
    yf = lambda v: base - v / vmax * (base - top)
    b += f'<line x1="{x0-6}" y1="{base}" x2="{x1+6}" y2="{base}" stroke="#fff" stroke-opacity=".5"/>'
    b += f'<line x1="{x0-6}" y1="{(top+base)/2:.1f}" x2="{x1+6}" y2="{(top+base)/2:.1f}" stroke="#fff" stroke-opacity=".12"/>'
    pts = " ".join(f"{xf(i):.1f},{yf(roll[i]):.1f}" for i in range(n))
    b += f'<polygon points="{x0},{base} {pts} {x1},{base}" fill="#fff" fill-opacity=".08"/>'
    b += f'<polyline points="{pts}" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>'
    for i, d in enumerate(days):
        if d.day == 1:
            b += (f'<line x1="{xf(i):.1f}" y1="{base}" x2="{xf(i):.1f}" y2="{base+4}" stroke="#fff" stroke-opacity=".5"/>'
                  f'<text x="{xf(i):.1f}" y="{base+15}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="#bbb">{MON[d.month-1]}</text>')
    peak_i = max(range(n), key=lambda i: (roll[i], i))
    peak_val, peak_date = roll[peak_i], days[peak_i]
    px_, py_ = xf(peak_i), yf(peak_val)
    lx = min(max(px_, x0 + 16), x1 - 16)
    b += star4(px_, py_, 3.4, "#fff")
    b += f'<text x="{lx:.1f}" y="{py_-9:.1f}" text-anchor="middle" font-family="{HEAVY}" font-style="italic" font-size="13" fill="#fff">{peak_val}</text>'
    now_val = roll[-1]
    nx, ny = xf(n - 1), yf(now_val)
    b += f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="4.5" fill="none" stroke="#fff" stroke-width="1.1"/>'
    b += f'<text x="{cx+14}" y="{H-10}" font-family="{SANS}" font-size="8.5" fill="#bbb">{now_val}/30 active days now · peaked {peak_val}/30 in {MON[peak_date.month-1]}</text>'
    b += f'<text x="255" y="{H-8}" text-anchor="end" font-family="{MONO}" font-size="8.5" fill="{GREY}">UPDATED {TODAY.isoformat()}</text>'
    return svg(W, H, b, f"Active days, a monthly skyline of active days, and a rolling 30-day pulse of active-day rate through the year — now {now_val} of 30, peaked at {peak_val} of 30 in {MON[peak_date.month-1]}")


OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.svg"):
    old.unlink()
files = {"banner": banner(), "nightlog": nightlog()}
for n, t in enumerate(["Origin", "Night Log", "Story Arcs", "Loadout"], 1):
    files[f"ch{n}"] = chapter(n, t)
for name, content in files.items():
    (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
print(f"active={len(active)} best_streak={best_streak} now={now_streak} weeks={weeks_active}/{weeks_total} window={first}..{TODAY} files={len(files)}")
