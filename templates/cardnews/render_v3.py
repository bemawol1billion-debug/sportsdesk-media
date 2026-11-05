"""스포츠데스크 카드뉴스 렌더러 v3 (종목 배경 일러스트 + 키워드 표지 + 공식 배포 사진 레이어) — 이슈 1개 = 게시물 1개(3~5장).

사진: 원고 최상위 "photo": {"src", "mode": full|cutout, "credit", "focus", "height", "right", "inner"} (슬라이드별 "photo"로 덮어쓰기, false면 끔)

사용법: python3 render_v2.py <post.json> <output_dir>
슬라이드 타입: cover, text, stats, compare, why, vote, dday, closing
종목별 포인트 컬러: baseball / basketball / badminton / football / volleyball / golf / default
"""
import base64
import html
import json
import mimetypes
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
    "football": "#4DA3FF", "ski": "#7FD4FF", "volleyball": "#C77DFF", "golf": "#9BE15D", "shorttrack": "#FF6FA8", "default": "#FF5A36",
}


ROOT = Path(__file__).resolve().parents[2]


def photo_uri(src):
    p = Path(src)
    if not p.is_absolute():
        p = ROOT / p
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def photo_layers(ph, cover):
    """공식 배포 사진 레이어. mode=full: 전면 배경 / mode=cutout: 배경 제거 PNG를 오른쪽 아래에 세움."""
    uri = photo_uri(ph["src"])
    mode = ph.get("mode", "full")
    if mode == "cutout":
        h = ph.get("height", 1000)
        if cover:
            return (f"<img class='ph-cut' src='{uri}' style='height:{h}px;right:{ph.get('right', -30)}px'>"
                    "<div class='ph-cut-shade'></div>")
        return f"<img class='ph-cut ph-dim' src='{uri}' style='height:{h}px;right:{ph.get('right', -30)}px'>"
    pos = ph.get("focus", "center top")
    return f"<img class='ph-full' src='{uri}' style='object-position:{pos}'><div class='ph-tint'></div>"


def credit(ph):
    return f"<div class='ph-credit'>{esc(ph['credit'])}</div>" if ph and ph.get("credit") else ""


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
.vq {{ margin-top:22px; font-size:78px; font-weight:900; line-height:1.2; letter-spacing:-2px; }}
.vopts {{ margin-top:56px; display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
.vopt {{ background:{PANEL}; border:4px solid {LINE}; padding:40px 30px 44px; text-align:center; }}
.vopt.a {{ border-color:{acc}; }}
.vopt.b {{ border-color:{WHITE}; }}
.vopt .k {{ display:inline-block; width:96px; height:96px; line-height:96px; font-size:58px; font-weight:900; background:{acc}; color:{NAVY}; border-radius:50%; }}
.vopt.b .k {{ background:{WHITE}; }}
.vopt .t {{ margin-top:28px; font-size:44px; font-weight:900; line-height:1.3; }}
.vopt .d {{ margin-top:14px; font-size:28px; color:{BODY}; line-height:1.45; }}
.vcta {{ margin-top:48px; font-size:38px; font-weight:900; text-align:center; }}
.vcta em {{ font-style:normal; color:{acc}; }}
.vchip {{ display:inline-block; margin-left:22px; background:{acc}; color:{NAVY}; padding:8px 18px; font-size:26px; font-weight:900; letter-spacing:2px; vertical-align:middle; }}

.dd {{ margin-top:36px; display:flex; flex-direction:column; gap:12px; }}
.ddr {{ display:flex; align-items:center; justify-content:space-between; background:{PANEL}; padding:18px 30px; border-left:8px solid {acc}; }}
.ddr.dim {{ border-left-color:{LINE}; }}
.ddr .n {{ font-size:38px; font-weight:900; }}
.ddr .n span {{ font-size:24px; color:{MUTED}; font-weight:700; margin-left:12px; }}
.ddr .s {{ font-size:26px; color:{BODY}; margin-top:6px; font-weight:700; }}
.ddr .v {{ font-size:64px; font-weight:900; color:{acc}; letter-spacing:-2px; white-space:nowrap; }}
.ddr.dim .v {{ font-size:30px; color:{MUTED}; letter-spacing:0; }}
.ddnote {{ margin-top:22px; font-size:24px; color:{MUTED}; line-height:1.5; }}
.ph-full {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.ph-tint {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(11,22,38,0.35) 0%, rgba(11,22,38,0.10) 40%, rgba(11,22,38,0.55) 100%); mix-blend-mode:multiply; }}
.ph-cut {{ position:absolute; bottom:0; width:auto; filter:drop-shadow(0 0 60px {acc}55) drop-shadow(0 20px 40px rgba(0,0,0,0.6)); }}
.ph-cut.ph-dim {{ opacity:0.16; filter:grayscale(0.4); }}
.ph-cut-shade {{ position:absolute; inset:0; background:linear-gradient(90deg, rgba(5,8,15,0.80) 0%, rgba(5,8,15,0.35) 45%, rgba(5,8,15,0) 70%); }}
.shade-photo {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(5,8,15,0.92) 0%, rgba(5,8,15,0.70) 28%, rgba(5,8,15,0.15) 52%, rgba(5,8,15,0.45) 80%, rgba(5,8,15,0.92) 100%); }}
.ph-credit {{ position:absolute; z-index:3; right:84px; bottom:142px; font-size:20px; color:rgba(245,242,235,0.75); font-weight:700; text-shadow:0 2px 8px rgba(0,0,0,0.8); }}
.b-top {{ display:flex; justify-content:space-between; align-items:flex-start; }}
.b-brand {{ font-weight:900; font-size:30px; letter-spacing:3px; display:flex; gap:14px; align-items:center; }}
.b-brand i {{ width:10px; height:44px; background:{acc}; display:block; }}
.b-brand small {{ display:block; font-size:18px; letter-spacing:2px; color:{MUTED}; font-weight:700; margin-top:4px; }}
.b-tag {{ font-size:24px; font-weight:900; color:{acc}; letter-spacing:2px; border:2px solid {acc}; padding:8px 16px; }}
.b-mid {{ flex:1; display:flex; flex-direction:column; justify-content:flex-end; padding-bottom:30px; position:relative; }}
.b-chip {{ align-self:flex-start; background:{acc}; color:#0A0C10; font-size:28px; font-weight:900; padding:8px 20px; border-radius:30px; margin-bottom:22px; }}
.b-kw {{ font-family:'Noto Sans CJK KR Black','Noto Sans CJK KR',sans-serif; font-weight:900; color:{acc}; line-height:1.0; letter-spacing:-5px; transform:scaleX(0.94); transform-origin:left; text-shadow:0 6px 0 rgba(0,0,0,0.35), 0 10px 40px rgba(0,0,0,0.8); }}
.b-hook {{ font-family:'Noto Sans CJK KR Black','Noto Sans CJK KR',sans-serif; font-weight:900; color:#FFFFFF; font-size:104px; line-height:1.08; letter-spacing:-4px; margin-top:10px; transform:scaleX(0.94); transform-origin:left; text-shadow:0 6px 0 rgba(0,0,0,0.35), 0 10px 40px rgba(0,0,0,0.85); }}
.b-brush {{ margin-top:-14px; margin-left:-6px; opacity:0.95; }}
.b-sub {{ margin-top:30px; font-size:34px; font-weight:700; line-height:1.5; color:#E9EDF2; text-shadow:0 3px 14px rgba(0,0,0,0.9); }}
.b-sub em {{ font-style:normal; color:{acc}; }}
.b-arrow {{ position:absolute; right:40px; top:40px; }}
.b-sparks {{ position:absolute; }}
.b-bottom {{ display:flex; justify-content:space-between; align-items:flex-end; }}
.hero {{ position:absolute; inset:0; }}
.hero img.cut {{ position:absolute; bottom:0; right:-40px; height:1080px; filter:drop-shadow(0 30px 50px rgba(0,0,0,0.7)); }}
.hero .obj {{ position:absolute; right:-120px; top:300px; filter:drop-shadow(0 0 80px rgba(255,214,10,0.25)); }}
.bshade {{ position:absolute; inset:0; background:linear-gradient(90deg, rgba(7,9,13,0.85) 0%, rgba(7,9,13,0.45) 50%, rgba(7,9,13,0) 75%), linear-gradient(180deg, rgba(7,9,13,0.6) 0%, rgba(7,9,13,0) 25%, rgba(7,9,13,0) 70%, rgba(7,9,13,0.85) 100%); }}
.vsub {{ margin-top:14px; font-size:28px; color:{MUTED}; text-align:center; font-weight:700; }}
"""


def top(d):
    return (f"<div class='top'><div class='logo'><i></i>SPORTS DESK</div>"
            f"<div class='date'>{esc(d['date'])} {esc(d['weekday'])}</div></div>")


def foot(left, i, n):
    return f"<div class='foot'><span>{esc(left)}</span><span><b>{i}</b>&nbsp;/&nbsp;{n}</span></div>"


def kicker(d):
    return f"<div><div class='kicker'>{esc(d['sport_en'])}<span class='tag'>· {esc(d['tag'])}</span></div></div>"


def cover_bold(d, s, i, n, ph):
    sport_acc = ACCENTS.get(d.get("sport_key", "default"), ACCENTS["default"])
    bk = backgrounds.bokeh(sport_acc)
    if ph and ph.get("mode") == "cutout":
        hero = f"<img class='cut' src='{photo_uri(ph['src'])}' style='height:{ph.get('height', 1080)}px;right:{ph.get('right', -40)}px'>"
        back = f"<div class='bgimg'>{bk}</div><div class='hero'>{hero}</div><div class='bshade'></div>"
    elif ph:
        back = (f"<div class='bgimg'>{photo_layers(ph, True)}</div><div class='bshade'></div>")
    elif s.get("jerseys"):
        back = (f"<div class='bgimg'>{bk}</div><div class='hero'>{backgrounds.jerseys(s['jerseys'], d.get('sport_key', 'baseball'), 'bold')}</div>"
                "<div class='bshade' style='opacity:0.6'></div>")
    else:
        # 실사 이미지가 없으면 일러스트 없이 조명 배경 + 큰 글씨만 (2026-11-05: 애니메이션 느낌 금지)
        back = f"<div class='bgimg'>{bk}</div><div class='bshade'></div>"
    kw = s["keyword"]
    size = s.get("kw_size") or (230 if len(kw) <= 3 else 170 if len(kw) <= 6 else 130)
    chip = f"<div class='b-chip'>🗳 {esc(s['vote_chip'])}</div>" if s.get("vote_chip") else ""
    sub = esc(s["sub"]).replace("[", "<em>").replace("]", "</em>")
    tag = f"#{esc(d['tag'])}"
    inner = (f"<div class='b-top'><div class='b-brand'><i></i><div>SPORTS DESK<small>{esc(d['sport_en'])} · {esc(d['date'])}</small></div></div>"
             f"<div class='b-tag'>{tag}</div></div>"
             f"<div class='b-mid'><div class='b-arrow'>{backgrounds.doodle_arrow()}</div>{chip}"
             f"<div class='b-kw' style='font-size:{size}px'>{esc(kw)}</div>"
             f"<div class='b-hook'>{esc(s['hook'])}</div>"
             f"<div class='b-brush'>{backgrounds.brush(w=s.get('brush_w', 460))}</div>"
             f"<div class='b-sub'>{sub}</div></div>"
             f"<div class='b-bottom'><div class='badge'><div class='v'>{esc(s['badge_v'])}</div><div class='l'>{esc(s['badge_l'])}</div></div></div>")
    return (f"{back}{credit(ph)}<div class='frame'>{inner}{foot('옆으로 넘겨서 보기 →', i, n)}</div>")


def slide(d, s, i, n):
    t = s["type"]
    src = "출처 · " + s["source"] if s.get("source") else ""
    bg = backgrounds.get(d.get("sport_key", ""))
    ph = s.get("photo", d.get("photo") if (t == "cover" or d.get("photo", {}).get("inner", False)) else None)
    if s.get("photo") is False:
        ph = None
    bold = d.get("style") == "bold"
    if bold:
        bg = backgrounds.bokeh(ACCENTS.get(d.get("sport_key", "default"), ACCENTS["default"]), seed=i)
    if t == "cover" and bold:
        return cover_bold(d, s, i, n, ph)
    if t == "cover":
        kw = s["keyword"]
        size = s.get("kw_size") or (250 if len(kw) <= 3 else 190 if len(kw) <= 5 else 150)
        chip = f"<div style='margin-top:18px'><span class='vchip' style='margin-left:0'>{esc(s['vote_chip'])}</span></div>" if s.get("vote_chip") else ""
        inner = (f"<div><div>{kicker(d)}{chip}</div>"
                 f"<div class='kw' style='font-size:{size}px'>{esc(kw)}</div>"
                 f"<div class='hook'>{esc(s['hook'])}</div>"
                 f"<div class='csub'>{esc(s['sub'])}</div></div>"
                 f"<div class='badge'><div class='v'>{esc(s['badge_v'])}</div><div class='l'>{esc(s['badge_l'])}</div></div>")
        if s.get("jerseys"):
            jz = backgrounds.jerseys(s["jerseys"], d.get("sport_key", "baseball"))
            back = (f"<div class='bgimg'>{bg}</div><div class='shade-cover'></div>"
                    f"<div class='bgimg' style='background:rgba(5,8,15,0.45)'></div><div class='bgimg'>{jz}</div>")
        elif ph and ph.get("mode", "full") == "full":
            back = f"<div class='bgimg'>{photo_layers(ph, True)}</div><div class='shade-photo'></div>"
        elif ph:
            back = f"<div class='bgimg'>{bg}</div><div class='shade-cover'></div>{photo_layers(ph, True)}"
        else:
            back = f"<div class='bgimg'>{bg}</div><div class='shade-cover'></div>"
        return (f"{back}<div class='bar'></div>{credit(ph)}"
                f"<div class='frame'>{top(d)}<div class='cover-mid'>{inner}</div>{foot('옆으로 넘겨서 보기 →', i, n)}</div>")
    if ph and ph.get("mode", "full") == "full":
        under = f"<div class='bgimg'>{photo_layers(ph, False)}</div><div class='shade-inner'></div>"
    elif ph:
        under = f"<div class='bgimg'>{bg}</div><div class='shade-inner'></div>{photo_layers(ph, False)}"
    else:
        under = f"<div class='bgimg'>{bg}</div><div class='shade-inner'></div>"
    if t == "text":
        bul = "".join(f"<div>{esc(b)}</div>" for b in s["bullets"])
        inner = (f"<div class='label'>{esc(s['label'])}</div><div class='heading'>{esc(s['heading'])}</div>"
                 f"<div class='bul'>{bul}</div>")
    elif t == "stats":
        cells = "".join(f"<div class='cell'><div class='v'"
                        + (f" style='font-size:{c['size']}px'" if c.get('size') else "")
                        + f">{esc(c['v'])}</div><div class='l'>{esc(c['l'])}</div></div>"
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
    elif t == "vote":
        a, b = s["options"]
        def opt(o, cls):
            d = f"<div class='d'>{esc(o['desc'])}</div>" if o.get("desc") else ""
            return f"<div class='vopt {cls}'><div class='k'>{esc(o['key'])}</div><div class='t'>{esc(o['text'])}</div>{d}</div>"
        cta = esc(s.get("cta", "캡션 아래 [설문]에서 투표해주세요")).replace("[", "<em>").replace("]", "</em>")
        inner = (f"<div class='label'>{esc(s.get('label', '당신의 선택은?'))}</div><div class='vq'>{esc(s['question'])}</div>"
                 f"<div class='vopts'>{opt(a, 'a')}{opt(b, 'b')}</div>"
                 f"<div class='vcta'>{cta}</div>"
                 f"<div class='vsub'>{esc(s.get('sub', '그렇게 생각한 이유는 댓글로 남겨주세요'))}</div>")
        return f"{under}<div class='bar'></div><div class='frame'>{top(d)}<div class='mid'>{inner}</div>{foot(src or '스포츠데스크 · 매일 스포츠를 맥락까지', i, n)}</div>"
    elif t == "dday":
        rows = ""
        for r in s["rows"]:
            dim = " dim" if r.get("dim") else ""
            rows += (f"<div class='ddr{dim}'><div><div class='n'>{esc(r['name'])}<span>{esc(r.get('region', ''))}</span></div>"
                     f"<div class='s'>{esc(r['status'])}</div></div><div class='v'>{esc(r['d'])}</div></div>")
        note = f"<div class='ddnote'>{esc(s['note'])}</div>" if s.get("note") else ""
        inner = (f"<div class='label'>{esc(s['label'])}</div><div class='heading'>{esc(s['heading'])}</div>"
                 f"<div class='dd'>{rows}</div>{note}")
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
    if d.get("style") == "bold":
        acc = "#FFD60A"
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    n = len(d["slides"])
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(d["slides"], 1):
            extra = (".shade-inner { background:rgba(7,9,13,0.80) !important; } body { background:#07090D !important; }"
                     ".heading, .big, .sum, .vq { font-family:'Noto Sans CJK KR Black','Noto Sans CJK KR',sans-serif; letter-spacing:-2px; }"
                     if d.get("style") == "bold" else "")
            pg.set_content(f"<html><head><meta charset='utf-8'><style>{css(acc)}{extra}</style></head>"
                           f"<body>{slide(d, s, i, n)}</body></html>")
            pg.wait_for_timeout(120)
            if pg.evaluate(f"document.querySelector('.frame').scrollHeight > {H}"):
                print(f"WARNING: {Path(path).stem} slide {i:02d} overflows")
            pg.screenshot(path=str(out / f"{i:02d}.png"))
        b.close()
    print("rendered", n, "slides ->", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
