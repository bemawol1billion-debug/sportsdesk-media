"""게시물 카드 폴더를 받아 미리보기 시트(JPG)를 만든다. 장당 540x720, 간격 20px, 가로로 이어 붙임.

사용: python templates/cardnews/preview_sheet.py <카드폴더> <출력.jpg>
"""
import sys
from pathlib import Path
from PIL import Image

W, H, GAP = 540, 720, 20


def main(card_dir, out):
    files = sorted(Path(card_dir).glob("[0-9][0-9].png"))
    sheet = Image.new("RGB", (len(files) * W + (len(files) + 1) * GAP, H + 2 * GAP), "#05080f")
    for n, f in enumerate(files):
        im = Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS)
        sheet.paste(im, (GAP + n * (W + GAP), GAP))
    sheet.save(out, quality=88)
    print("saved", out, len(files))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
