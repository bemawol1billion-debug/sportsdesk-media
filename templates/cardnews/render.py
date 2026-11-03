"""스포츠데스크 카드뉴스 렌더러.

사용법: python3 render.py <content.json> <output_dir>
출력: 01.png(표지) ~ 05.png(마무리), 1080x1440 (3:4)
"""
import html
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

W, H = 1080, 1440

# ---- 디자인 시스템 ----
NAVY = "#0B1626"
PANEL = "#12233A"
LINE = "#22344C"
ORANGE = "#FF5A36"
WHITE = "#F5F2EB"
MUTED = "#8FA3B8"
BODY = "#C9D4E0"
FONT = "'Noto Sans CJK KR', 'Noto Sans KR', sans-serif"

BASE_CSS = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; background:{NAVY}; color:{WHITE};
  font-family:{FONT}; overflow:hidden; position:relative; word-break:keep-all; }}
.frame {{ position:absolute; inset:0; padding:72px 84px 64px; display:flex; flex-direction:column; }}
.top {{ display:flex; justify-content:space-between; align-items:center;
  padding-bottom:28px; border-bottom:2px solid {LINE}; }}
.logo {{ display:flex; align-items:center; gap:16px; font-weight:900; font-size:30px; letter-spacing:6px; }}
.logo i {{ display:block; width:22px; height:22px; background:{ORANGE}; }}
.date {{ font-size:26px; color:{MUTED}; font-weight:700; letter-spacing:3px; }}
.foot {{ margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end;
  font-size:24px; color:{MUTED}; padding-top:24px; border-top:2px solid {LINE}; }}
.foot b {{ color:{WHITE}; font-weight:700; }}
.accent-bar {{ position:absolute; left:0; top:0; width:12px; height:100%; background:{ORANGE}; }}
"""


def esc(s):
    return html.escape(s).replace("\n", "<br>")


def page(body, extra_css=""):
    return f"<html><head><meta charset='utf-8'><style>{BASE_CSS}{extra_css}</style></head><body>{body}</body></html>"


def header(d):
    return (f"<div class='top'><div class='logo'><i></i>SPORTS DESK</div>"
            f"<div class='date'>{d['date']} {d['weekday']}</div></div>")


def cover(d):
    items = "".join(
        f"<div class='item'><div class='n'>{i+1:02d}</div><div><div class='sp'>{esc(it['sport'])}</div>"
        f"<div class='hl'>{esc(it['headline'])}</div></div></div>"
        for i, it in enumerate(d["cover"]["items"]))
    css = f"""
    .title {{ font-size:150px; font-weight:900; line-height:1.08; margin-top:90px; letter-spacing:-4px; }}
    .title span {{ color:{ORANGE}; }}
    .sub {{ font-size:32px; color:{MUTED}; margin-top:28px; font-weight:700; }}
    .list {{ margin-top:80px; display:flex; flex-direction:column; gap:40px; }}
    .item {{ display:flex; gap:36px; align-items:flex-start; }}
    .n {{ font-size:64px; font-weight:900; color:{ORANGE}; line-height:1; min-width:96px; }}
    .sp {{ font-size:26px; color:{MUTED}; font-weight:700; letter-spacing:2px; margin-bottom:8px; }}
    .hl {{ font-size:44px; font-weight:700; line-height:1.3; }}
    """
    title = esc(d["cover"]["title"]).replace("3", f"<span>3</span>")
    body = (f"<div class='accent-bar'></div><div class='frame'>{header(d)}"
            f"<div class='title'>{title}</div>"
            f"<div class='sub'>오늘 꼭 알아야 할 스포츠 이슈, 맥락까지</div>"
            f"<div class='list'>{items}</div>"
            f"<div class='foot'><span>옆으로 넘겨서 보기 →</span><span><b>1</b> / 5</span></div></div>")
    return page(body, css)


def issue(d, it, idx):
    facts = "".join(f"<p>{esc(f)}</p>" for f in it["facts"])
    css = f"""
    .chip {{ margin-top:52px; display:inline-flex; gap:18px; align-items:center; font-size:26px; font-weight:700;
      letter-spacing:3px; color:{ORANGE}; }}
    .chip .no {{ background:{ORANGE}; color:{NAVY}; padding:6px 14px; letter-spacing:1px; }}
    .chip .tag {{ color:{MUTED}; letter-spacing:1px; }}
    .stat {{ font-size:190px; font-weight:900; color:{ORANGE}; line-height:1; margin-top:30px; letter-spacing:-6px; }}
    .stat-label {{ font-size:28px; color:{MUTED}; font-weight:700; margin-top:16px; }}
    .hl {{ font-size:62px; font-weight:900; line-height:1.22; margin-top:48px; letter-spacing:-1px; }}
    .facts {{ margin-top:36px; display:flex; flex-direction:column; gap:18px; }}
    .facts p {{ font-size:33px; line-height:1.55; color:{BODY}; }}
    .why {{ margin-top:40px; background:{PANEL}; border-left:10px solid {ORANGE}; padding:30px 36px; }}
    .why .t {{ font-size:26px; font-weight:900; color:{ORANGE}; letter-spacing:2px; margin-bottom:12px; }}
    .why .b {{ font-size:32px; line-height:1.55; font-weight:700; }}
    """
    body = (f"<div class='frame'>{header(d)}"
            f"<div><div class='chip'><span class='no'>{it['no']}</span>{esc(it['sport'])}"
            f"<span class='tag'>· {esc(it['tag'])}</span></div></div>"
            f"<div class='stat'>{esc(it['stat'])}</div><div class='stat-label'>{esc(it['stat_label'])}</div>"
            f"<div class='hl'>{esc(it['headline'])}</div>"
            f"<div class='facts'>{facts}</div>"
            f"<div class='why'><div class='t'>왜 중요한가</div><div class='b'>{esc(it['why'])}</div></div>"
            f"<div class='foot'><span>출처 · {esc(it['source'])}</span><span><b>{idx}</b> / 5</span></div></div>")
    return page(body, css)


def closing(d):
    c = d["closing"]
    rows = "".join(
        f"<div class='row'><div class='tm'>{esc(g['time'])}</div><div class='sp'>{esc(g['sport'])}</div>"
        f"<div class='mt'>{esc(g['match'])}<span>{esc(g['place'])}</span></div></div>"
        for g in c["games"])
    css = f"""
    .title {{ font-size:96px; font-weight:900; line-height:1.1; margin-top:48px; letter-spacing:-3px; }}
    .rows {{ margin-top:40px; display:flex; flex-direction:column; }}
    .row {{ display:flex; align-items:center; gap:28px; padding:20px 0; border-bottom:2px solid {LINE}; }}
    .tm {{ font-size:40px; font-weight:900; color:{ORANGE}; min-width:130px; }}
    .sp {{ font-size:26px; font-weight:700; color:{NAVY}; background:{MUTED}; padding:6px 14px; min-width:110px; text-align:center; }}
    .mt {{ font-size:34px; font-weight:700; white-space:pre; }}
    .mt span {{ color:{MUTED}; font-size:26px; margin-left:16px; font-weight:400; }}
    .cta {{ margin-top:40px; background:{ORANGE}; color:{NAVY}; padding:36px 40px; font-size:40px; font-weight:900; line-height:1.35; }}
    .handle {{ margin-top:22px; font-size:30px; color:{WHITE}; font-weight:700; }}
    """
    body = (f"<div class='accent-bar'></div><div class='frame'>{header(d)}"
            f"<div class='title'>{esc(c['title'])}</div><div class='rows'>{rows}</div>"
            f"<div class='cta'>{esc(c['cta'])}</div>"
            f"<div class='handle'>@sport_news_desk 팔로우하고 내일 아침에 다시 만나요</div>"
            f"<div class='foot'><span>스포츠데스크 · 매일 오전 업데이트</span><span><b>5</b> / 5</span></div></div>")
    return page(body, css)


def main(content_path, out_dir):
    d = json.loads(Path(content_path).read_text(encoding="utf-8"))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pages = [cover(d)] + [issue(d, it, i + 2) for i, it in enumerate(d["issues"])] + [closing(d)]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, h in enumerate(pages, 1):
            pg.set_content(h)
            pg.wait_for_timeout(150)
            # 넘침 검사: 본문이 화면 밖으로 나가면 경고
            overflow = pg.evaluate("document.querySelector('.frame').scrollHeight > %d" % H)
            if overflow:
                print(f"WARNING: page {i:02d} overflows")
            pg.screenshot(path=str(out / f"{i:02d}.png"))
        b.close()
    print("rendered", len(pages), "pages to", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
