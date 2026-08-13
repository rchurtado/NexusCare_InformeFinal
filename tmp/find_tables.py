from pathlib import Path
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Grupo 3 - linaresgonzalesjavier_31567_4373176_NexusCare_InformeFinal_v6pm (7).pdf"

with pdfplumber.open(PDF) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        tables = page.find_tables()
        if tables:
            print(i, [tuple(round(v, 1) for v in t.bbox) for t in tables])
