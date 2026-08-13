from pathlib import Path
from PIL import Image, ImageDraw
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "tmp" / "pdfs" / "final-render"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "tmp" / "pdfs" / "final-contact-sheets"
OUT.mkdir(parents=True, exist_ok=True)

files = sorted(SOURCE.glob("page-*.jpg"), key=lambda p: int(p.stem.split("-")[-1]))
thumb_w, thumb_h = 300, 424
cols, rows = 4, 4
for sheet_index in range(0, len(files), cols * rows):
    batch = files[sheet_index:sheet_index + cols * rows]
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + 24)), "#d8d8d8")
    draw = ImageDraw.Draw(sheet)
    for pos, path in enumerate(batch):
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_w - 8, thumb_h - 8))
        x = (pos % cols) * thumb_w + (thumb_w - img.width) // 2
        y = (pos // cols) * (thumb_h + 24) + 4
        sheet.paste(img, (x, y))
        draw.text((x, y + img.height + 2), f"p. {int(path.stem.split('-')[-1])}", fill="black")
    sheet.save(OUT / f"contact-{sheet_index // (cols * rows) + 1:02d}.jpg", quality=90)
print(f"pages={len(files)} sheets={(len(files) + cols*rows - 1)//(cols*rows)}")
