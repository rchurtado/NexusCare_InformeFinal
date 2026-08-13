import json
import re
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Grupo 3 - linaresgonzalesjavier_31567_4373176_NexusCare_InformeFinal_v6pm (7).pdf"
OUT = ROOT / "tmp" / "pdfs" / "layout_inventory.json"

inventory = []
with pdfplumber.open(PDF) as doc:
    for page_no, page in enumerate(doc.pages, 1):
        words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
        lines_by_y = {}
        for w in words:
            key = round(w["top"] / 2) * 2
            lines_by_y.setdefault(key, []).append(w)
        blocks = []
        for _, line_words in sorted(lines_by_y.items()):
            line_words.sort(key=lambda w: w["x0"])
            text = " ".join(w["text"] for w in line_words).strip()
            if text:
                blocks.append({
                    "bbox": [round(min(w["x0"] for w in line_words), 2), round(min(w["top"] for w in line_words), 2),
                             round(max(w["x1"] for w in line_words), 2), round(max(w["bottom"] for w in line_words), 2)],
                    "text": text,
                })
        captions = [b for b in blocks if re.search(r"^(TABLA|FIGURA)[IVXLCDM]+\.\d+", b["text"].replace(" ", ""), re.I)]
        headings = [b for b in blocks if re.match(r"^\d+(?:\.\d+)+\s+\S", b["text"])]
        inventory.append({"page": page_no, "size": [page.width, page.height], "captions": captions, "headings": headings, "blocks": blocks})

OUT.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"pages={len(inventory)} captions={sum(len(p['captions']) for p in inventory)} headings={sum(len(p['headings']) for p in inventory)}")
for p in inventory:
    for c in p["captions"]:
        label = c["text"].replace(chr(10), " ").encode("ascii", "backslashreplace").decode()
        print(f"p{p['page']}: {label} @ {c['bbox']}")
