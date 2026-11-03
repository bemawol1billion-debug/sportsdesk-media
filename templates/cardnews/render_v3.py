"""스포츠데스크 카드뉴스 렌더러 v3 (종목 배경 일러스트 + 키워드 표지) — 이슈 1개 = 게시물 1개(3~5장).

사용법: python3 render_v2.py <post.json> <output_dir>
슬라이드 타입: cover, text, stats, compare, why, closing
종목별 포인트 컬러: baseball / basketball / badminton / football / volleyball / golf / default
"""
import html
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
import backgrounds  # noqa: E402

W, H = 1080, 1440
NAVY, PANEL, LINE = "#0B1626", "#12233A", "#22344C"
WHITE, MUTED, BODY = "#F5F2EB", "#8FA3B8", "#C9D4E0"
FONT = "'Noto Sans CJK KR', 'Noto Sans KR', sans-serif"
ACCENTS = {
    "baseball": "#FF5A36", "basketball": "#FFB020", "badminton": "#2BD9A0",
    "football": "#4DA3FF", "volleyball": "#C77DFF", "golf": "#9BE15D", "default": "#FF5A36",
}


def esc(s):
    return html.escape(str(s)).replace("\n", "<br>")


def css(acc):
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; background:{NAVY}; color:{WHITE}; font-family:{FONT};
  overflow:hidden; position:relative; word-break:keep-all; }}
.frame {{ position:absolute; inset:0; padding:72px 84px 64px; display:flex; flex-direction:column; }}
.top {{ display:flex; justify-content:space-between; align-items:center; padding-bottom:28px; border-bottom:2px solid {LINE}; }}
.logo {{ display:flex; align-items:center; gap:16px; font-weight:900; font-size:30px; letter-spacing:6px; }}
.logo i {{ display:block; width:22px; height:22px; background:{acc}; }}
.date {{ font-size:26px; color:{MUTED}; font-weight:700; letter-spacing:3px; }}
.foot {{ margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end; gap:24px;
  font-size:24px; color:{MUTED}; padding-top:24px; border-top:2px solid {LINE}; }}
.foot b {{ color:{WHITE}; }}
.bar {{ position:absolute; left:0; top:0; width:12px; height:100%; background:{acc}; }}
.kicker {{ display:inline-flex; gap:16px; align-items:center; font-size:26px; font-weight:700; letter-spacing:3px; color:{acc}; }}
.kicker .tag {{ color:{MUTED}; letter-spacing:1px; }}
.mid {{ flex:1; display:flex; flex-direction:column; justify-content:center; padding:40px 0; }}
.label {{ margin-top:0; font-size:28px; font-weight:900; color:{acc}; letter-spacing:2px; }}
.heading {{ margin-top:18px; font-size:64px; font-weight:900; line-height:1.22; letter-spacing:-1px; }}
/* cover */
.c-stat {{ font-size:280px; font-weight:900; color:{acc}; line-height:1; margin-top:40px; letter-spacing:-8px; }}
.c-head {{ font-size:90px; font-weight:900; line-height:1.18; margin-top:40px; letter-spacing:-2px; }}
.c-sub {{ font-size:36px; color:{MUTED}; font-weight:700; margin-top:32px; }}
/* text */
.bul {{ margin-top:56px; display:flex; flex-direction:column; gap:34px; }}
.bul div {{ display:flex; gap:24px; font-size:41px; line-height:1.5; color:{BODY}; }}
.bul div:before {{ content:''; flex:none; width:14px; height:14px; margin-top:22px; background:{acc}; }}
/* stats */
.grid {{ margin-top:56px; display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
.cell {{ background:{PANEL}; padding:44px 38px; min-height:290px; }}
.cell .v {{ font-size:108px; font-weight:900; color:{acc}; line-height:1; letter-spacing:-2px; }}
.cell .l {{ font-size:31px; color:{BODY}; margin-top:22px; line-height:1.45; font-weight:700; }}
/* compare */
.cmp {{ margin-top:48px; }}
.cmp .hd, .cmp .r {{ display:grid; grid-template-columns:1fr 200px 1fr; align-items:center; }}
.cmp .hd div {{ font-size:46px; font-weight:900; padding-bottom:20px; }}
.cmp .hd div:last-child, .cmp .r div:last-child {{ text-align:right; }}
.cmp .r {{ border-top:2px solid {LINE}; padding:32px 0; }}
.cmp .r div {{ font-size:38px; font-weight:700; line-height:1.35; }}
.cmp .m {{ text-align:center; font-size:24px !important; color:{MUTED}; }}
.cmp .win {{ color:{acc}; }}
/* why */
.big {{ margin-top:40px; font-size:86px; font-weight:900; line-height:1.22; letter-spacing:-2px; }}
.big em {{ font-style:normal; color:{acc}; }}
.box {{ margin-top:52px; background:{PANEL}; border-left:10px solid {acc}; padding:44px 44px; font-size:39px; line-height:1.6; color:{BODY}; }}
/* closing */
.sum {{ margin-top:0; font-size:80px; font-weight:900; line-height:1.25; letter-spacing:-2px; }}
.pts {{ margin-top:48px; display:flex; flex-direction:column; gap:22px; }}
.pts div {{ font-size:37px; line-height:1.5; color:{BODY}; padding-left:28px; border-left:6px solid {acc}; }}
.cta {{ margin-top:52px; background:{acc}; color:{NAVY}; padding:36px 40px; font-size:40px; font-weight:900; line-height:1.35; }}
.handle {{ margin-top:22px; font-size:30px; font-weight:700; }}
.bgimg {{ position:absolute; inset:0; }}
.bgimg svg {{ display:block; width:100%; height:100%; }}
.shade-cover {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(5,8,15,0.90) 0%, rgba(5,8,15,0.55) 26%, rgba(5,8,15,0.05) 52%, rgba(5,8,15,0.30) 88%, rgba(5,8,15,0.75) 100%); }}
.shade-inner {{ position:absolute; inset:0; background:rgba(11,22,38,0.87); }}
.frame {{ z-index:2; }}
.cover-mid {{ flex:1; display:flex; flex-direction:column; justify-content:space-between; padding:56px 0 40px; }}
.kw {{ font-weight:900; line-height:1.02; letter-spacing:-6px; margin-top:34px; text-shadow:0 8px 40px rgba(0,0,0,0.7); }}
.hook {{ font-size:70px; font-weight:900; color:{acc}; margin-top:26px; line-height:1.16; letter-spacing:-2px; text-shadow:0 6px 30px rgba(0,0,0,0.7); }}
.csub {{ font-size:36px; font-weight:700; color:#E3EAF2; margin-top:28px; line-height:1.45; text-shadow:0 4px 20px rgba(0,0,0,0.8); }}
.badge {{ display:inline-flex; align-items:center; gap:26px; background:{acc}; color:{NAVY}; padding:22px 34px 22px 30px; align-self:flex-start; }}
.badge .v {{ font-size:86px; font-weight:900; line-height:1; letter-spacing:-3px; }}
.badge .l {{ font-size:28px; font-weight:900; line-height:1.3; }}
"""


def top(d):
    return (f"<div class='top'><div class='logo'><i></i>SPORTS DESK</div>"
            f"<div class='date'>{esc(d['date'])} {esc(d['weekday'])}</div></div>")


def foot(left, i, n):
    return f"<div class='foot'><span>{esc(left)}</span><span><b>{i}</b>&nbsp;/&nbsp;{n}</span></div>"


def kicker(d):
    return f"<div><div class='kicker'>{esc(d['sport_en'])}<span class='tag'>· {esc(d['tag'])}</span></div></div>"


def slide(d, s, i, n):
    t = s["type"]
    src = "출처 · " + s["source"] if s.get("source") else ""
    bg = backgrounds.get(d.get("sport_key", ""))
    if t == "cover":
        kw = s["keyword"]
        size = s.get("kw_size") or (250 if len(kw) <= 3 else 190 if len(kw) <= 5 else 150)
        inner = (f"<div><div>{kicker(d)}</div>"
                 f"<div class='kw' style='font-size:{size}px'>{esc(kw)}</div>"
                 f"<div class='hook'>{esc(s['hook'])}</div>"
                 f"<div class='csub'>{esc(s['sub'])}</div></div>"
                 f"<div class='badge'><div class='v'>{esc(s['badge_v'])}</div><div class='l'>{esc(s['badge_l'])}</div></div>")
        return (f"<div class='bgimg'>{bg}</div><div class='shade-cover'></div><div class='bar'></div>"
                f"<div class='frame'>{top(d)}<div class='cover-mid'>{inner}</div>{foot('옆으로 넘겨서 보기 →', i, n)}</div>")
    under = f"<div class='bgimg'>{bg}</div><div class='shade-inner'></div>"
    if t == "text":
        bul = "".join(f"<div>{esc(b)}</div>" for b in s["bullets"])
        inner = (f"<div class='label'>{esc(s['label'])}</div><div class='heading'>{esc(s['heading'])}</div>"
                 f"<div class='bul'>{bul}</div>")
    elif t == "stats":
        cells = "".join(f"<div class='cell'><div class='v'>{esc(c['v'])}</div><div class='l'>{esc(c['l'])}</div></div>"
                        for c in s["stats"])
        inner = (f"<div class='label'>{esc(s['label'])}</div><div class='heading'>{esc(s['heading'])}</div>"
                 f"<div class='grid'>{cells}</div>")
    elif t == "compare":
        a, b = s["teams"]
        rows = ""
        for r in s["rows"]:
            wl = " win" if r.get("win") == "left" else ""
            wr = " win" if r.get("win") == "right" else ""
            rows += (f"<div class='r'><div class='{wl}'>{esc(r['l'])}</div><div class='m'>{esc(r['m'])}</div>"
                     f"<div class='{wr}'>{esc(r['r'])}</div></div>")
        inner = (f"<div class='label'>{esc(s['label'])}</div><div class='heading'>{esc(s['heading'])}</div>"
                 f"<div class='cmp'><div class='hd'><div>{esc(a)}</div><div></div><div>{esc(b)}</div></div>{rows}</div>")
    elif t == "why":
        big = esc(s["statement"]).replace("[", "<em>").replace("]", "</em>")
        inner = (f"<div class='label'>{esc(s['label'])}</div><div class='big'>{big}</div>"
                 f"<div class='box'>{esc(s['body'])}</div>")
    elif t == "closing":
        pts = "".join(f"<div>{esc(p)}</div>" for p in s.get("points", []))
        inner = (f"<div class='sum'>{esc(s['summary'])}</div><div class='pts'>{pts}</div>"
                 f"<div class='cta'>{esc(s['cta'])}</div><div class='handle'>@sport_news_desk</div>")
        return f"{under}<div class='bar'></div><div class='frame'>{top(d)}<div class='mid'>{inner}</div>{foot(src or '스포츠데스크 · 매일 스포츠를 맥락까지', i, n)}</div>"
    else:
        raise ValueError(t)
    return f"{under}<div class='frame'>{top(d)}<div class='mid'>{inner}</div>{foot(src, i, n)}</div>"


def main(path, out_dir):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    acc = ACCENTS.get(d.get("sport_key", "default"), ACCENTS["default"])
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    n = len(d["slides"])
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(d["slides"], 1):
            pg.set_content(f"<html><head><meta charset='utf-8'><style>{css(acc)}</style></head>"
                           f"<body>{slide(d, s, i, n)}</body></html>")
            pg.wait_for_timeout(120)
            if pg.evaluate(f"document.querySelector('.frame').scrollHeight > {H}"):
                print(f"WARNING: {Path(path).stem} slide {i:02d} overflows")
            pg.screenshot(path=str(out / f"{i:02d}.png"))
        b.close()
    print("rendered", n, "slides ->", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
