"""종목별 배경 일러스트 (SVG, 1080x1440). 실제 로고·인물·사진 없이 직접 그린 그래픽."""

W, H = 1080, 1440


def _wrap(defs, body):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}' "
            f"preserveAspectRatio='xMidYMid slice'><defs>{defs}"
            "<filter id='glow' x='-50%' y='-50%' width='200%' height='200%'><feGaussianBlur stdDeviation='18'/></filter>"
            "<filter id='soft' x='-20%' y='-20%' width='140%' height='140%'><feGaussianBlur stdDeviation='4'/></filter>"
            f"</defs>{body}</svg>")


def basketball():
    defs = """
    <linearGradient id='bg' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#0B1626'/><stop offset='1' stop-color='#04070D'/></linearGradient>
    <radialGradient id='ball' cx='0.36' cy='0.32' r='0.75'><stop offset='0' stop-color='#FFB062'/><stop offset='0.45' stop-color='#E8611C'/><stop offset='1' stop-color='#6E2104'/></radialGradient>
    <radialGradient id='spot' cx='0.75' cy='0.35' r='0.6'><stop offset='0' stop-color='#FFB020' stop-opacity='0.30'/><stop offset='1' stop-color='#FFB020' stop-opacity='0'/></radialGradient>
    <linearGradient id='floor' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3A2410' stop-opacity='0'/><stop offset='1' stop-color='#5A3818' stop-opacity='0.55'/></linearGradient>
    <clipPath id='bc'><circle cx='830' cy='1180' r='340'/></clipPath>
    """
    net = "".join(
        f"<line x1='{705 + i * 25}' y1='742' x2='{760 + i * 15}' y2='900' stroke='#E8EEF5' stroke-opacity='0.55' stroke-width='4'/>"
        f"<line x1='{960 - i * 25}' y1='742' x2='{905 - i * 15}' y2='900' stroke='#E8EEF5' stroke-opacity='0.55' stroke-width='4'/>"
        for i in range(11))
    planks = "".join(f"<line x1='0' y1='{y}' x2='1080' y2='{y}' stroke='#C08040' stroke-opacity='0.10' stroke-width='3'/>"
                     for y in range(1120, 1440, 46))
    body = f"""
    <rect width='1080' height='1440' fill='url(#bg)'/>
    <rect width='1080' height='1440' fill='url(#spot)'/>
    <polygon points='760,0 900,0 1080,1440 420,1440' fill='#FFFFFF' opacity='0.035'/>
    <rect x='0' y='1060' width='1080' height='380' fill='url(#floor)'/>{planks}
    <rect x='628' y='430' width='420' height='280' rx='10' fill='#FFFFFF' fill-opacity='0.06' stroke='#E8EEF5' stroke-opacity='0.75' stroke-width='7'/>
    <rect x='768' y='560' width='140' height='110' fill='none' stroke='#E8EEF5' stroke-opacity='0.75' stroke-width='6'/>
    <rect x='820' y='710' width='26' height='34' fill='#9AA7B5'/>
    {net}
    <ellipse cx='832' cy='742' rx='132' ry='24' fill='none' stroke='#FF6A1A' stroke-width='14'/>
    <circle cx='830' cy='1180' r='360' fill='#FFB020' opacity='0.18' filter='url(#glow)'/>
    <circle cx='830' cy='1180' r='340' fill='url(#ball)'/>
    <g clip-path='url(#bc)' fill='none' stroke='#2A0E02' stroke-width='11' stroke-linecap='round'>
      <path d='M470,1150 Q830,1080 1190,1150'/>
      <path d='M830,830 Q770,1180 830,1530'/>
      <path d='M560,920 Q760,1180 560,1440'/>
      <path d='M1100,920 Q900,1180 1100,1440'/>
    </g>
    """
    return _wrap(defs, body)


def baseball():
    defs = """
    <linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#050A14'/><stop offset='0.6' stop-color='#0B1A2E'/><stop offset='1' stop-color='#0A1F18'/></linearGradient>
    <radialGradient id='lightglow' cx='0.5' cy='0.5' r='0.5'><stop offset='0' stop-color='#FFFFFF' stop-opacity='0.9'/><stop offset='1' stop-color='#FFFFFF' stop-opacity='0'/></radialGradient>
    <linearGradient id='grass' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#145A36'/><stop offset='1' stop-color='#0A2E1C'/></linearGradient>
    <radialGradient id='ball' cx='0.38' cy='0.34' r='0.75'><stop offset='0' stop-color='#FFFFFF'/><stop offset='0.6' stop-color='#E3E1DA'/><stop offset='1' stop-color='#8F8C84'/></radialGradient>
    <clipPath id='bc'><circle cx='840' cy='860' r='250'/></clipPath>
    """
    lamps = ""
    for cx0, cy0 in ((150, 120), (930, 90)):
        lamps += f"<circle cx='{cx0 + 40}' cy='{cy0 + 30}' r='170' fill='url(#lightglow)' opacity='0.35'/>"
        for r in range(3):
            for c in range(5):
                lamps += f"<circle cx='{cx0 + c * 22}' cy='{cy0 + r * 22}' r='8' fill='#FFFFFF' opacity='0.95'/>"
        lamps += f"<rect x='{cx0 + 38}' y='{cy0 + 60}' width='10' height='420' fill='#1C2A3C'/>"
    body = f"""
    <rect width='1080' height='1440' fill='url(#sky)'/>
    {lamps}
    <polygon points='150,150 260,150 760,1100 -200,1100' fill='#FFFFFF' opacity='0.035'/>
    <polygon points='900,120 1010,120 1280,1100 400,1100' fill='#FFFFFF' opacity='0.035'/>
    <path d='M-100,1120 Q540,960 1180,1120 L1180,1440 L-100,1440 Z' fill='url(#grass)'/>
    <path d='M-100,1120 Q540,960 1180,1120' fill='none' stroke='#0E3D26' stroke-width='22'/>
    <polygon points='540,1100 860,1270 540,1440 220,1270' fill='#8A5530' opacity='0.85'/>
    <polygon points='540,1150 770,1270 540,1390 310,1270' fill='#15603A'/>
    <circle cx='540' cy='1270' r='34' fill='#8A5530'/>
    <g fill='#FFFFFF'><rect x='528' y='1088' width='24' height='24' transform='rotate(45 540 1100)'/>
      <rect x='848' y='1258' width='24' height='24' transform='rotate(45 860 1270)'/>
      <rect x='208' y='1258' width='24' height='24' transform='rotate(45 220 1270)'/></g>
    <line x1='540' y1='1440' x2='-100' y2='1100' stroke='#FFFFFF' stroke-opacity='0.7' stroke-width='5'/>
    <line x1='540' y1='1440' x2='1180' y2='1100' stroke='#FFFFFF' stroke-opacity='0.7' stroke-width='5'/>
    <circle cx='840' cy='860' r='270' fill='#FFFFFF' opacity='0.12' filter='url(#glow)'/>
    <circle cx='840' cy='860' r='250' fill='url(#ball)'/>
    <g clip-path='url(#bc)' fill='none'>
      <path d='M650,650 Q780,860 650,1070' stroke='#B8B4AA' stroke-width='5'/>
      <path d='M1030,650 Q900,860 1030,1070' stroke='#B8B4AA' stroke-width='5'/>
      <path d='M666,650 Q796,860 666,1070' stroke='#D2262F' stroke-width='12' stroke-dasharray='6 16' stroke-linecap='round'/>
      <path d='M1014,650 Q884,860 1014,1070' stroke='#D2262F' stroke-width='12' stroke-dasharray='6 16' stroke-linecap='round'/>
    </g>
    """
    return _wrap(defs, body)


def badminton():
    defs = """
    <linearGradient id='bg' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#06121A'/><stop offset='1' stop-color='#0A2230'/></linearGradient>
    <linearGradient id='court' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#0F5C46'/><stop offset='1' stop-color='#083828'/></linearGradient>
    <radialGradient id='spot' cx='0.72' cy='0.4' r='0.55'><stop offset='0' stop-color='#2BD9A0' stop-opacity='0.28'/><stop offset='1' stop-color='#2BD9A0' stop-opacity='0'/></radialGradient>
    <linearGradient id='feather' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#FFFFFF' stop-opacity='0.95'/><stop offset='1' stop-color='#DDE6EA' stop-opacity='0.95'/></linearGradient>
    <radialGradient id='cork' cx='0.4' cy='0.35' r='0.7'><stop offset='0' stop-color='#FFFFFF'/><stop offset='1' stop-color='#BFC6CC'/></radialGradient>
    """
    mesh = "".join(f"<line x1='{x}' y1='1000' x2='{x}' y2='1120' stroke='#FFFFFF' stroke-opacity='0.22' stroke-width='2'/>"
                   for x in range(0, 1080, 18))
    mesh += "".join(f"<line x1='0' y1='{y}' x2='1080' y2='{y}' stroke='#FFFFFF' stroke-opacity='0.22' stroke-width='2'/>"
                    for y in range(1006, 1120, 18))
    ribs = "".join(f"<line x1='{745 + i * 18}' y1='600' x2='{630 + i * 47}' y2='230' stroke='#A9B7BF' stroke-width='3'/>"
                   for i in range(9))
    scallop = "".join(f"<circle cx='{640 + i * 47}' cy='228' r='26' fill='#FFFFFF' fill-opacity='0.95'/>" for i in range(9))
    streaks = "".join(f"<line x1='{300 + i * 40}' y1='{860 + i * 30}' x2='{600 + i * 40}' y2='{700 + i * 30}' stroke='#2BD9A0' stroke-opacity='{0.35 - i * 0.05:.2f}' stroke-width='6' stroke-linecap='round'/>"
                      for i in range(5))
    body = f"""
    <rect width='1080' height='1440' fill='url(#bg)'/>
    <rect width='1080' height='1440' fill='url(#spot)'/>
    <polygon points='160,1060 920,1060 1180,1440 -100,1440' fill='url(#court)'/>
    <g stroke='#FFFFFF' stroke-opacity='0.8' stroke-width='6' fill='none'>
      <polygon points='160,1060 920,1060 1180,1440 -100,1440'/>
      <line x1='540' y1='1180' x2='540' y2='1440'/>
      <line x1='80' y1='1180' x2='1000' y2='1180'/>
      <line x1='210' y1='1060' x2='-30' y2='1440'/><line x1='870' y1='1060' x2='1110' y2='1440'/>
    </g>
    <rect x='0' y='994' width='1080' height='12' fill='#F5F5F5'/>
    {mesh}
    <rect x='0' y='1118' width='1080' height='4' fill='#F5F5F5' opacity='0.6'/>
    {streaks}
    <g transform='translate(130 200) rotate(-32 820 520)'>
      <circle cx='820' cy='420' r='300' fill='#2BD9A0' opacity='0.16' filter='url(#glow)'/>
      <polygon points='740,600 900,600 1050,230 590,230' fill='url(#feather)'/>
      {ribs}{scallop}
      <rect x='738' y='585' width='164' height='34' fill='#2BD9A0'/>
      <path d='M738,618 L902,618 Q902,740 820,740 Q738,740 738,618 Z' fill='url(#cork)'/>
    </g>
    """
    return _wrap(defs, body)


def ski():
    defs = """
    <linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#050B18'/><stop offset='0.55' stop-color='#0C1E36'/><stop offset='1' stop-color='#1B3554'/></linearGradient>
    <linearGradient id='snowA' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#E9F4FF'/><stop offset='1' stop-color='#9DB9D6'/></linearGradient>
    <linearGradient id='snowB' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#C9DDF0'/><stop offset='1' stop-color='#6F8FB0'/></linearGradient>
    <radialGradient id='moon' cx='0.5' cy='0.5' r='0.5'><stop offset='0' stop-color='#7FD4FF' stop-opacity='0.45'/><stop offset='1' stop-color='#7FD4FF' stop-opacity='0'/></radialGradient>
    """
    flakes = "".join(f"<circle cx='{(i * 137) % 1080}' cy='{(i * 89) % 1000}' r='{2 + (i % 4)}' fill='#FFFFFF' opacity='{0.25 + (i % 5) * 0.12:.2f}'/>" for i in range(70))
    lights = "".join(f"<circle cx='{760 + i * 34}' cy='{860 + i * 46}' r='7' fill='#FFE7A3'/><circle cx='{760 + i * 34}' cy='{860 + i * 46}' r='22' fill='#FFE7A3' opacity='0.18'/>" for i in range(9))
    towers = "".join(f"<line x1='{300 + i * 120}' y1='{760 + i * 70}' x2='{300 + i * 120}' y2='{860 + i * 70}' stroke='#2A3F5A' stroke-width='8'/>" for i in range(6))
    body = f"""
    <rect width='1080' height='1440' fill='url(#sky)'/>
    <circle cx='820' cy='300' r='360' fill='url(#moon)'/>
    <circle cx='820' cy='300' r='70' fill='#EAF6FF' opacity='0.85'/>
    <polygon points='-100,1000 260,560 520,860 760,520 1180,980 1180,1440 -100,1440' fill='url(#snowB)' opacity='0.55'/>
    <polygon points='-100,1180 340,700 620,1000 900,760 1180,1100 1180,1440 -100,1440' fill='url(#snowA)'/>
    <path d='M340,700 Q420,900 300,1440' stroke='#B7CDE3' stroke-width='60' fill='none' opacity='0.6'/>
    <path d='M900,760 Q820,1000 960,1440' stroke='#B7CDE3' stroke-width='50' fill='none' opacity='0.6'/>
    <line x1='300' y1='760' x2='960' y2='1210' stroke='#2A3F5A' stroke-width='4'/>
    {towers}{lights}{flakes}
    """
    return _wrap(defs, body)


def golf():
    defs = """
    <linearGradient id='gsky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#050B18'/><stop offset='0.6' stop-color='#0B1E2E'/><stop offset='1' stop-color='#123A2E'/></linearGradient>
    <linearGradient id='fairA' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3E8F3A'/><stop offset='1' stop-color='#14401C'/></linearGradient>
    <linearGradient id='fairB' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#2A6B2E'/><stop offset='1' stop-color='#0E2E16'/></linearGradient>
    <radialGradient id='green' cx='0.5' cy='0.45' r='0.6'><stop offset='0' stop-color='#9BE15D'/><stop offset='1' stop-color='#3C8A2E'/></radialGradient>
    <radialGradient id='gglow' cx='0.5' cy='0.5' r='0.5'><stop offset='0' stop-color='#9BE15D' stop-opacity='0.35'/><stop offset='1' stop-color='#9BE15D' stop-opacity='0'/></radialGradient>
    <clipPath id='gbc'><circle cx='900' cy='1200' r='120'/></clipPath>
    <radialGradient id='gball' cx='0.35' cy='0.3' r='0.75'><stop offset='0' stop-color='#FFFFFF'/><stop offset='0.6' stop-color='#E3E8EE'/><stop offset='1' stop-color='#8C98A6'/></radialGradient>
    """
    stars = "".join(f"<circle cx='{(i * 151) % 1080}' cy='{(i * 67) % 620}' r='{1 + (i % 3)}' fill='#FFFFFF' opacity='{0.15 + (i % 4) * 0.12:.2f}'/>" for i in range(50))
    dimples = "".join(f"<circle cx='{800 + (i % 7) * 32 + (16 if (i // 7) % 2 else 0)}' cy='{1100 + (i // 7) * 30}' r='7' fill='#B9C3CE' opacity='0.55'/>" for i in range(49))
    body = f"""
    <rect width='1080' height='1440' fill='url(#gsky)'/>
    {stars}
    <circle cx='760' cy='640' r='380' fill='url(#gglow)'/>
    <path d='M-100,900 C200,780 520,820 760,760 C920,720 1060,740 1180,780 L1180,1440 L-100,1440 Z' fill='url(#fairB)' opacity='0.8'/>
    <path d='M-100,1080 C240,960 600,1000 860,920 C980,884 1100,900 1180,930 L1180,1440 L-100,1440 Z' fill='url(#fairA)'/>
    <ellipse cx='780' cy='835' rx='230' ry='58' fill='url(#green)' opacity='0.9'/>
    <ellipse cx='820' cy='840' rx='22' ry='7' fill='#06120A'/>
    <line x1='820' y1='840' x2='820' y2='520' stroke='#E9EEF3' stroke-width='7'/>
    <path d='M820,522 L960,566 L820,610 Z' fill='#9BE15D'/>
    <ellipse cx='520' cy='965' rx='110' ry='26' fill='#D9C79A' opacity='0.55'/>
    <path d='M880,1080 Q700,760 820,700' stroke='#9BE15D' stroke-width='3' stroke-dasharray='14 16' fill='none' opacity='0.5'/>
    <rect x='889' y='1300' width='22' height='70' rx='6' fill='#E9EEF3' opacity='0.85'/>
    <circle cx='900' cy='1200' r='120' fill='url(#gball)'/>
    <g clip-path='url(#gbc)'>{dimples}</g>
    """
    return _wrap(defs, body)


def football():
    defs = """
    <linearGradient id='fsky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#040912'/><stop offset='0.5' stop-color='#0A1830'/><stop offset='1' stop-color='#0B2A1E'/></linearGradient>
    <radialGradient id='flamp' cx='0.5' cy='0.5' r='0.5'><stop offset='0' stop-color='#FFFFFF' stop-opacity='0.9'/><stop offset='1' stop-color='#FFFFFF' stop-opacity='0'/></radialGradient>
    <linearGradient id='pitch' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#1C6B3E'/><stop offset='1' stop-color='#0A3320'/></linearGradient>
    <radialGradient id='fglow' cx='0.5' cy='0.5' r='0.5'><stop offset='0' stop-color='#4DA3FF' stop-opacity='0.35'/><stop offset='1' stop-color='#4DA3FF' stop-opacity='0'/></radialGradient>
    <radialGradient id='fball' cx='0.36' cy='0.3' r='0.78'><stop offset='0' stop-color='#FFFFFF'/><stop offset='0.62' stop-color='#E2E6EC'/><stop offset='1' stop-color='#86909C'/></radialGradient>
    <clipPath id='fbc'><circle cx='820' cy='1170' r='230'/></clipPath>
    """
    lamps = ""
    for cx0, cy0 in ((140, 110), (940, 80)):
        lamps += f"<circle cx='{cx0 + 50}' cy='{cy0 + 30}' r='190' fill='url(#flamp)' opacity='0.30'/>"
        lamps += "".join(f"<rect x='{cx0 + (k % 4) * 26}' y='{cy0 + (k // 4) * 22}' width='18' height='14' fill='#EAF2FF' opacity='0.9'/>" for k in range(12))
    stripes = "".join(f"<polygon points='{-400 + i * 190},1440 {-40 + i * 120},700 {20 + i * 120},700 {-210 + i * 190},1440' fill='#FFFFFF' opacity='0.035'/>" for i in range(0, 14, 2))
    crowd = "".join(f"<circle cx='{(i * 23) % 1080}' cy='{560 + (i * 37) % 120}' r='4' fill='#8FB4E0' opacity='{0.10 + (i % 5) * 0.06:.2f}'/>" for i in range(160))
    patches = "".join(f"<polygon points='{x},{y - 46} {x + 44},{y - 14} {x + 28},{y + 38} {x - 28},{y + 38} {x - 44},{y - 14}' fill='#1A2230'/>"
                      for x, y in ((820, 1170), (640, 1040), (1000, 1040), (640, 1330), (1000, 1330), (820, 960), (820, 1400)))
    body = f"""
    <rect width='1080' height='1440' fill='url(#fsky)'/>
    {lamps}
    <rect x='0' y='540' width='1080' height='170' fill='#0E1E36' opacity='0.85'/>{crowd}
    <polygon points='-300,1440 120,700 960,700 1380,1440' fill='url(#pitch)'/>{stripes}
    <g fill='none' stroke='#E9F2FA' stroke-opacity='0.55' stroke-width='5'>
      <polygon points='-300,1440 120,700 960,700 1380,1440'/>
      <line x1='-60' y1='1020' x2='1140' y2='1020'/>
      <ellipse cx='540' cy='1020' rx='230' ry='70'/>
      <polygon points='330,700 750,700 790,790 290,790'/>
    </g>
    <rect x='420' y='630' width='240' height='72' fill='none' stroke='#F2F6FA' stroke-opacity='0.8' stroke-width='6'/>
    <circle cx='540' cy='860' r='420' fill='url(#fglow)'/>
    <circle cx='820' cy='1170' r='250' fill='#4DA3FF' opacity='0.16' filter='url(#glow)'/>
    <circle cx='820' cy='1170' r='230' fill='url(#fball)'/>
    <g clip-path='url(#fbc)'>{patches}</g>
    """
    return _wrap(defs, body)


def shorttrack():
    defs = """
    <linearGradient id='ssky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#040914'/><stop offset='0.55' stop-color='#0B1A30'/><stop offset='1' stop-color='#1A2E48'/></linearGradient>
    <linearGradient id='ice' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#CFE3F5'/><stop offset='1' stop-color='#7E9CBC'/></linearGradient>
    <radialGradient id='sglow' cx='0.5' cy='0.5' r='0.5'><stop offset='0' stop-color='#FF6FA8' stop-opacity='0.32'/><stop offset='1' stop-color='#FF6FA8' stop-opacity='0'/></radialGradient>
    <radialGradient id='slamp' cx='0.5' cy='0.5' r='0.5'><stop offset='0' stop-color='#FFFFFF' stop-opacity='0.8'/><stop offset='1' stop-color='#FFFFFF' stop-opacity='0'/></radialGradient>
    <linearGradient id='blade' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='#9AA8B8'/><stop offset='0.5' stop-color='#F4F8FC'/><stop offset='1' stop-color='#8A98A8'/></linearGradient>
    """
    lamps = "".join(f"<circle cx='{120 + i * 210}' cy='90' r='120' fill='url(#slamp)' opacity='0.25'/><rect x='{100 + i * 210}' y='80' width='40' height='16' rx='4' fill='#EAF2FF'/>" for i in range(5))
    pads = "".join(f"<rect x='{-40 + i * 120}' y='690' width='112' height='46' rx='8' fill='{'#FF6FA8' if i % 2 else '#2B5BD7'}' opacity='0.75'/>" for i in range(11))
    blocks = "".join(f"<ellipse cx='{x}' cy='{y}' rx='16' ry='8' fill='#1C2433'/>" for x, y in ((300, 960), (380, 900), (480, 870), (600, 870), (700, 900), (780, 960)))
    trails = "".join(f"<path d='M{-80 + i * 30},{1260 + i * 26} C300,{1120 + i * 20} 780,{1120 + i * 20} 1160,{1250 + i * 26}' stroke='#FFFFFF' stroke-opacity='{0.10 + i * 0.04:.2f}' stroke-width='3' fill='none'/>" for i in range(6))
    body = f"""
    <rect width='1080' height='1440' fill='url(#ssky)'/>
    {lamps}
    <g transform='translate(0,170)'>
    <rect x='0' y='600' width='1080' height='90' fill='#0E1E36' opacity='0.9'/>
    {pads}
    <rect x='0' y='736' width='1080' height='560' fill='url(#ice)'/>
    <ellipse cx='540' cy='1000' rx='470' ry='170' fill='none' stroke='#2B5BD7' stroke-opacity='0.45' stroke-width='6'/>
    <ellipse cx='540' cy='1000' rx='560' ry='230' fill='none' stroke='#FF6FA8' stroke-opacity='0.35' stroke-width='4' stroke-dasharray='20 18'/>
    {blocks}</g>{trails}
    <circle cx='800' cy='1180' r='330' fill='url(#sglow)'/>
    <path d='M560,1270 L1060,1230 Q1100,1228 1096,1262 L1090,1274 Q1080,1290 1040,1292 L560,1300 Z' fill='url(#blade)'/>
    <rect x='640' y='1180' width='34' height='90' fill='#2A3446'/><rect x='960' y='1170' width='34' height='70' fill='#2A3446'/>
    <path d='M600,1070 Q600,1180 650,1190 L1010,1170 Q1060,1166 1050,1120 L1000,1050 Q900,990 760,1010 Q640,1030 600,1070 Z' fill='#141C2A'/>
    <path d='M620,1090 Q760,1060 1000,1080' stroke='#FF6FA8' stroke-width='10' fill='none'/>
    """
    return _wrap(defs, body)


BACKGROUNDS = {"basketball": basketball, "baseball": baseball, "badminton": badminton, "ski": ski, "golf": golf,
               "football": football, "shorttrack": shorttrack}


def get(sport_key):
    fn = BACKGROUNDS.get(sport_key)
    return fn() if fn else ""


def _jersey(i, main, trim, sub, pattern, kind):
    """팀 컬러 유니폼 일러스트 1벌(500x560 좌표). 로고·글자·등번호 없음."""
    body = ("M150,40 Q250,78 350,40 L472,112 L432,236 L380,208 L382,538 Q250,566 118,538 "
            "L120,208 L68,236 L28,112 Z")
    defs = (f"<clipPath id='jc{i}'><path d='{body}'/></clipPath>"
            f"<linearGradient id='jl{i}' x1='0' y1='0' x2='1' y2='0'>"
            "<stop offset='0' stop-color='#000' stop-opacity='0.45'/><stop offset='0.22' stop-color='#000' stop-opacity='0.05'/>"
            "<stop offset='0.5' stop-color='#fff' stop-opacity='0.16'/><stop offset='0.78' stop-color='#000' stop-opacity='0.08'/>"
            "<stop offset='1' stop-color='#000' stop-opacity='0.5'/></linearGradient>"
            f"<linearGradient id='jv{i}' x1='0' y1='0' x2='0' y2='1'>"
            "<stop offset='0' stop-color='#fff' stop-opacity='0.10'/><stop offset='1' stop-color='#000' stop-opacity='0.35'/></linearGradient>")
    fill = f"<path d='{body}' fill='{main}'/>"
    if pattern == "stripes":
        fill += f"<g clip-path='url(#jc{i})'>" + "".join(
            f"<rect x='{x}' y='0' width='42' height='600' fill='{sub}'/>" for x in range(36, 480, 84)) + "</g>"
    if pattern == "hoop":
        fill += f"<g clip-path='url(#jc{i})'><rect x='0' y='250' width='520' height='70' fill='{sub}'/></g>"
    folds = (f"<g clip-path='url(#jc{i})' fill='none' stroke='#000' stroke-opacity='0.16' stroke-width='10' stroke-linecap='round'>"
             "<path d='M170,250 Q200,380 165,520'/><path d='M330,260 Q300,390 340,525'/><path d='M120,215 Q160,240 175,300'/>"
             "<path d='M380,215 Q340,240 325,300'/></g>")
    trims = (f"<path d='M150,40 Q250,{118 if kind == 'baseball' else 96} 350,40' fill='none' stroke='{trim}' stroke-width='16'/>"
             f"<path d='M432,236 L472,112' stroke='{trim}' stroke-width='18'/><path d='M68,236 L28,112' stroke='{trim}' stroke-width='18'/>"
             f"<path d='M120,208 L120,540 M382,208 L382,540' stroke='{trim}' stroke-width='8' stroke-opacity='0.9'/>")
    if kind == "baseball":
        trims += (f"<path d='M262,96 L262,548' stroke='{trim}' stroke-width='9'/>"
                  + "".join(f"<circle cx='250' cy='{y}' r='7' fill='{trim}' stroke='#000' stroke-opacity='0.3' stroke-width='2'/>"
                            for y in range(140, 520, 64)))
    # 실제 구단 로고·스폰서 자리에는 스포츠데스크 마크만 넣는다
    mark = (f"<g clip-path='url(#jc{i})'>"
            f"<path d='M318,128 L372,128 L372,170 Q372,198 345,210 Q318,198 318,170 Z' fill='{trim}' stroke='#000' stroke-opacity='0.25' stroke-width='3'/>"
            f"<text x='345' y='178' text-anchor='middle' font-family='Noto Sans CJK KR' font-weight='900' font-size='26' fill='{main}'>SD</text>"
            f"<text x='250' y='300' text-anchor='middle' font-family='Noto Sans CJK KR' font-weight='900' font-size='27' "
            f"letter-spacing='1' fill='{trim}' stroke='#000' stroke-opacity='0.2' stroke-width='1.5'>SPORTS DESK</text></g>")
    shade = mark + f"<path d='{body}' fill='url(#jl{i})'/><path d='{body}' fill='url(#jv{i})'/>"
    outline = f"<path d='{body}' fill='none' stroke='#DDE6F0' stroke-opacity='0.35' stroke-width='4'/>"
    return defs, fill + folds + trims + shade + outline


def jerseys(items, kind="baseball", layout="classic"):
    """표지 전경용 유니폼 2벌(마주 보게). items: [{main, trim, sub?, pattern?}, ...]"""
    defs, body = "", ""
    if layout == "bold":
        places = [(330, 190, -10, 0.92), (560, 300, 9, 0.92)] if len(items) == 2 else [(520, 220, 6, 1.05)]
    else:
        places = [(150, 850, -8, 0.82), (520, 850, 8, 0.82)] if len(items) == 2 else [(330, 820, 0, 0.9)]
    for i, (it, (x, y, rot, sc)) in enumerate(zip(items, places)):
        d, g = _jersey(i, it["main"], it["trim"], it.get("sub", it["trim"]), it.get("pattern", "plain"), kind)
        defs += d
        body += (f"<g transform='translate({x},{y}) rotate({rot} 250 300) scale({sc})' filter='url(#jsh)'>{g}</g>")
    defs += "<filter id='jsh' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='24' stdDeviation='22' flood-color='#000' flood-opacity='0.6'/></filter>"
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}'><defs>{defs}</defs>{body}</svg>")


def bokeh(tint="#FFD60A", seed=7):
    """경기장 조명 보케 배경(사람·로고 없음). bold 스타일 공용."""
    import random
    rnd = random.Random(seed)
    lights = ""
    for _ in range(46):
        x, y = rnd.randint(-40, 1120), rnd.randint(40, 820)
        r = rnd.choice([10, 14, 18, 26, 34, 46])
        col = rnd.choice(["#FFF4D6", "#FFFFFF", "#CFE3FF", tint])
        op = rnd.uniform(0.10, 0.45)
        lights += f"<circle cx='{x}' cy='{y}' r='{r}' fill='{col}' opacity='{op:.2f}'/>"
    body = f"""
    <rect width='1080' height='1440' fill='#07090D'/>
    <radialGradient id='bkA' cx='0.75' cy='0.2' r='0.7'><stop offset='0' stop-color='#2B3A55' stop-opacity='0.9'/><stop offset='1' stop-color='#07090D' stop-opacity='0'/></radialGradient>
    <radialGradient id='bkB' cx='0.15' cy='0.05' r='0.5'><stop offset='0' stop-color='{tint}' stop-opacity='0.20'/><stop offset='1' stop-color='#07090D' stop-opacity='0'/></radialGradient>
    <linearGradient id='bkF' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#0F3A22' stop-opacity='0'/><stop offset='1' stop-color='#0F3A22' stop-opacity='0.55'/></linearGradient>
    <rect width='1080' height='1440' fill='url(#bkA)'/><rect width='1080' height='1440' fill='url(#bkB)'/>
    <g filter='url(#glow)'>{lights}</g>
    <rect x='0' y='980' width='1080' height='460' fill='url(#bkF)'/>
    """
    return _wrap("", body)


def doodle_arrow(color="#FFD60A"):
    """손글씨 느낌 곡선 화살표 + 강조선."""
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 120' width='260' height='120'>"
            f"<path d='M12,92 C60,20 150,10 214,40' fill='none' stroke='{color}' stroke-width='6' stroke-linecap='round' stroke-dasharray='2 14'/>"
            f"<path d='M196,22 L222,42 L192,58' fill='none' stroke='{color}' stroke-width='7' stroke-linecap='round' stroke-linejoin='round'/>"
            "</svg>")


def sparks(color="#FFD60A"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 90 90' width='90' height='90' fill='none' stroke='{color}' stroke-width='7' stroke-linecap='round'>"
            "<path d='M20,58 L8,72'/><path d='M40,46 L36,20'/><path d='M58,56 L80,40'/></svg>")


def brush(color="#FFD60A", w=520):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 40' width='{w}' height='{int(w * 40 / 520)}' preserveAspectRatio='none'>"
            f"<path d='M6,26 C120,10 300,6 512,14 C420,20 260,26 120,34 C80,36 30,36 6,26 Z' fill='{color}'/></svg>")


def ball(kind):
    """히어로 오브젝트(사진이 없을 때): 종목 공/장비 큰 일러스트."""
    if kind == "baseball":
        return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600' width='600' height='600'>"
                "<defs><radialGradient id='hb' cx='0.36' cy='0.3' r='0.8'><stop offset='0' stop-color='#fff'/><stop offset='0.6' stop-color='#E6E2D8'/><stop offset='1' stop-color='#8C877C'/></radialGradient>"
                "<clipPath id='hbc'><circle cx='300' cy='300' r='280'/></clipPath></defs>"
                "<circle cx='300' cy='300' r='280' fill='url(#hb)'/><g clip-path='url(#hbc)' fill='none' stroke='#C8102E' stroke-width='9' stroke-dasharray='16 12'>"
                "<path d='M120,40 Q260,300 120,560'/><path d='M480,40 Q340,300 480,560'/></g></svg>")
    return ""
