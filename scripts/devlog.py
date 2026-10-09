"""Daily dev log: one Markdown file per day, plus a weekly roll-up.

Run:
  python scripts/devlog.py new            ->  devlog/YYYY/YYYY-MM-DD.md (carries over open tasks)
  python scripts/devlog.py week           ->  devlog/weekly/YYYY-Www.md for the current week
  python scripts/devlog.py week --last    ->  same, for last week
  python scripts/devlog.py new --date 2026-10-09

The day starts at DEVLOG_DAY_START (default 5h, America/Sao_Paulo): a commit at 2am still
belongs to the night before. Stdlib only.
"""
import argparse
import datetime as dt
import os
import pathlib
import re
import zoneinfo

ROOT = pathlib.Path(__file__).resolve().parent.parent / "devlog"
TZ = zoneinfo.ZoneInfo(os.environ.get("DEVLOG_TZ", "America/Sao_Paulo"))
DAY_START = int(os.environ.get("DEVLOG_DAY_START", "5"))
WEEKDAYS = "segunda terça quarta quinta sexta sábado domingo".split()

FOCUS, DONE, LEARNED, BLOCKERS, TOMORROW = "Foco de hoje", "Feito", "Aprendi", "Bloqueios", "Amanhã"
SECTIONS = [FOCUS, DONE, LEARNED, BLOCKERS, TOMORROW]
HINTS = {
    FOCUS: "1 a 3 coisas que fariam o dia valer a pena",
    DONE: "o que saiu de fato (commits, PRs, deploys, decisões)",
    LEARNED: "uma coisa nova, com link se tiver",
    BLOCKERS: "o que travou e quanto tempo custou",
    TOMORROW: "por onde começar amanhã; o que ficar aberto aqui vira foco amanhã",
}
TASK = re.compile(r"^\s*-\s*\[( |x|X)\]\s*(.*\S)\s*$")
BULLET = re.compile(r"^\s*-\s+(?!\[[ xX]\])(.*\S)\s*$")


def today():
    return (dt.datetime.now(TZ) - dt.timedelta(hours=DAY_START)).date()


def path_for(day):
    return ROOT / f"{day.year}" / f"{day.isoformat()}.md"


def entries():
    days = []
    for p in ROOT.glob("[0-9][0-9][0-9][0-9]/*.md"):
        try:
            days.append(dt.date.fromisoformat(p.stem))
        except ValueError:
            pass
    return sorted(days)


def parse(text):
    """Map section title -> list of lines under it."""
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur and not line.lstrip().startswith("<!--"):
            out[cur].append(line)
    return out


def tasks(lines, done):
    return [m[2] for m in map(TASK.match, lines) if m and (m[1] != " ") == done]


def bullets(lines):
    return [m[1] for m in map(BULLET.match, lines) if m]


def render(day, carried):
    focus = "\n".join(f"- [ ] {t}" for t in carried) or "- [ ] "
    body = {FOCUS: focus, DONE: "- ", LEARNED: "- ", BLOCKERS: "- ", TOMORROW: "- [ ] "}
    parts = [f"# {day.isoformat()} · {WEEKDAYS[day.weekday()]}\n"]
    for s in SECTIONS:
        parts.append(f"## {s}\n<!-- {HINTS[s]} -->\n{body[s]}\n")
    return "\n".join(parts)


def cmd_new(day):
    target = path_for(day)
    if target.exists():
        print(f"{target.relative_to(ROOT.parent)} already exists")
        return
    previous = [d for d in entries() if d < day]
    carried = []
    if previous:
        sec = parse(path_for(previous[-1]).read_text(encoding="utf-8"))
        for t in tasks(sec.get(TOMORROW, []), False) + tasks(sec.get(FOCUS, []), False):
            if t not in carried:
                carried.append(t)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(day, carried), encoding="utf-8")
    print(f"created {target.relative_to(ROOT.parent)} ({len(carried)} carried over)")


def cmd_week(day):
    monday = day - dt.timedelta(days=day.weekday())
    week = [monday + dt.timedelta(days=i) for i in range(7)]
    logged = [d for d in week if path_for(d).exists()]
    year, num, _ = monday.isocalendar()
    done, learned, blockers, last_open = [], [], [], []
    for d in logged:
        sec = parse(path_for(d).read_text(encoding="utf-8"))
        tag = f"*{WEEKDAYS[d.weekday()][:3]}*"
        done += [f"{tag} {t}" for t in tasks(sec.get(FOCUS, []), True) + bullets(sec.get(DONE, []))]
        learned += [f"{tag} {t}" for t in bullets(sec.get(LEARNED, []))]
        blockers += [f"{tag} {t}" for t in bullets(sec.get(BLOCKERS, []))]
        last_open = tasks(sec.get(FOCUS, []), False) + tasks(sec.get(TOMORROW, []), False)

    def block(items, empty="—"):
        return "\n".join(f"- {i}" for i in items) or empty

    streak = "".join("■" if d in logged else "□" for d in week)
    links = " · ".join(f"[{WEEKDAYS[d.weekday()][:3]}](../{d.year}/{d.isoformat()}.md)" for d in logged)
    text = (
        f"# Semana {year}-W{num:02d} · {monday:%d/%m} a {week[-1]:%d/%m}\n\n"
        f"`{streak}` {len(logged)}/7 dias registrados · {len(done)} entregas · "
        f"{len(learned)} aprendizados · {len(blockers)} bloqueios\n\n"
        f"{links or 'Nenhum dia registrado.'}\n\n"
        f"## Entregas\n{block(done)}\n\n"
        f"## Aprendizados\n{block(learned)}\n\n"
        f"## Bloqueios\n{block(blockers, 'Nenhum. 🎉')}\n\n"
        f"## Em aberto\n{block(dict.fromkeys(last_open))}\n"
    )
    target = ROOT / "weekly" / f"{year}-W{num:02d}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT.parent)} ({len(logged)} days)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["new", "week"])
    ap.add_argument("--date", type=dt.date.fromisoformat, help="YYYY-MM-DD (default: today)")
    ap.add_argument("--last", action="store_true", help="week: summarize the previous week")
    a = ap.parse_args()
    day = a.date or today()
    if a.command == "new":
        cmd_new(day)
    else:
        cmd_week(day - dt.timedelta(days=7) if a.last else day)


if __name__ == "__main__":
    main()
