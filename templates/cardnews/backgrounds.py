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


BACKGROUNDS = {"basketball": basketball, "baseball": baseball, "badminton": badminton, "ski": ski}


def get(sport_key):
    fn = BACKGROUNDS.get(sport_key)
    return fn() if fn else ""
