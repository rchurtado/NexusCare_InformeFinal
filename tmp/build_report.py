import json
import re
import shutil
import unicodedata
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "NexusCare_InformeFinal_UTEC"
PDF = ROOT / "Grupo 3 - linaresgonzalesjavier_31567_4373176_NexusCare_InformeFinal_v6pm (7).pdf"
TXT = ROOT / "tmp" / "pdfs" / "nexuscare-source.txt"
INV = ROOT / "tmp" / "pdfs" / "layout_inventory.json"
ASSETS = PROJECT / "images" / "recuperados"

CHAPTER_PAGES = {
    1: (4, 4), 2: (5, 10), 3: (11, 12), 4: (13, 15), 5: (16, 17),
    6: (18, 21), 7: (22, 36), 8: (37, 42), 9: (43, 45), 10: (46, 55),
    11: (56, 59), 12: (60, 62), 13: (63, 65), 14: (66, 67), 15: (70, 70),
}

CHAPTER_TITLES = {
    1: "Introducción", 2: "Contexto del problema", 3: "Objetivos del proyecto",
    4: "Marco metodológico", 5: "Autodiagnóstico inicial", 6: "Definición del MVP",
    7: "Arquitectura de la solución", 8: "Desarrollo y construcción",
    9: "Métrica principal de validación", 10: "Evaluación de resultados",
    11: "Limitaciones y riesgos", 12: "Aprendizajes y lecciones",
    13: "Conclusiones", 14: "Trabajo futuro", 15: "Anexos",
}


def clean_unicode(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("ı́", "í").replace("ı", "i")
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    return unicodedata.normalize("NFC", text)


def dewrap(lines):
    out = ""
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if out and out.endswith("-") and s[:1].islower():
            out = out[:-1] + s
        else:
            out += (" " if out else "") + s
    return re.sub(r"\s+", " ", out).strip()


def tex_escape(text: str) -> str:
    text = clean_unicode(text)
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "≤": r"$\leq$", "≥": r"$\geq$", "∼": r"$\sim$",
        "σ": r"$\sigma$", "ρ": r"$\rho$", "𝜎": r"$\sigma$", "𝜌": r"$\rho$", "×": r"$\times$",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def tex_reference(text: str) -> str:
    parts = re.split(r"(https?://\S+)", clean_unicode(text))
    out = []
    for part in parts:
        if part.startswith(("http://", "https://")):
            trailing = ""
            while part and part[-1] in ".,;":
                trailing = part[-1] + trailing
                part = part[:-1]
            out.append(r"\url{" + part.replace("%", r"\%") + "}" + tex_escape(trailing))
        else:
            out.append(tex_escape(part))
    return "".join(out)


def split_paragraphs(page_text: str):
    return [p for p in re.split(r"(?:\r?\n){2,}", page_text) if p.strip()]


def is_page_number(text):
    return bool(re.fullmatch(r"\s*\d+\s*", text))


def crop_assets(inventory):
    ASSETS.mkdir(parents=True, exist_ok=True)
    assets = {}
    with pdfplumber.open(PDF) as pdf:
        for page_info in inventory:
            page_no = page_info["page"]
            if not page_info["captions"]:
                continue
            page = pdf.pages[page_no - 1]
            lines = sorted(page_info["blocks"], key=lambda b: b["bbox"][1])
            rendered = page.to_image(resolution=220, antialias=True)
            table_i = figure_i = 0
            for cap in page_info["captions"]:
                compact = cap["text"].replace(" ", "").upper()
                if compact.startswith("FIGURA"):
                    figure_i += 1
                    candidates = [im for im in page.images if im["bottom"] <= cap["bbox"][1] + 2]
                    if not candidates:
                        continue
                    im = max(candidates, key=lambda x: x["bottom"])
                    bbox = (max(55, im["x0"] - 4), max(80, im["top"] - 4),
                            min(page.width - 55, im["x1"] + 4), min(page.height - 60, im["bottom"] + 4))
                    kind, idx = "figure", figure_i
                else:
                    table_i += 1
                    start = max(80, cap["bbox"][3] + 3)
                    after = [b for b in lines if b["bbox"][1] > cap["bbox"][3] + 2]
                    end = min(page.height - 55, start + 285)
                    prev_bottom = cap["bbox"][3]
                    seen = 0
                    for b in after:
                        top, bottom = b["bbox"][1], b["bbox"][3]
                        gap = top - prev_bottom
                        if seen >= 2 and top > start + 45 and gap > 18:
                            end = min(page.height - 55, prev_bottom + 7)
                            break
                        prev_bottom = max(prev_bottom, bottom)
                        seen += 1
                    bbox = (65, start, page.width - 65, end)
                    kind, idx = "table", table_i
                name = f"p{page_no:02d}_{kind}_{idx}.png"
                scale = 220 / 72
                pixel_bbox = tuple(int(round(v * scale)) for v in bbox)
                rendered.original.crop(pixel_bbox).save(ASSETS / name, format="PNG")
                assets[(page_no, kind, idx)] = name
    return assets


def parse_page(page_no, text, asset_map):
    paras = split_paragraphs(text)
    output = []
    table_i = figure_i = 0
    skip_next = False
    for para in paras:
        if skip_next:
            skip_next = False
            continue
        lines = para.splitlines()
        joined = dewrap(lines)
        if not joined or is_page_number(joined):
            continue
        upper = clean_unicode(joined).upper()
        if upper.startswith("CAPÍTULO ") or (upper.isupper() and upper in {v.upper() for v in CHAPTER_TITLES.values()}):
            continue
        compact = re.sub(r"\s+", "", upper)
        if compact.startswith("TABLA") and re.match(r"TABLA[IVXLCDM]+\.\d+", compact):
            table_i += 1
            caption = re.sub(r"^\s*TABLA\s+[IVXLCDM]+\.\d+:\s*", "", clean_unicode(joined), flags=re.I)
            asset = asset_map.get((page_no, "table", table_i))
            if asset:
                output.append("\\begin{table}[H]\n\\centering\n"
                              f"\\includegraphics[width=0.96\\textwidth,height=0.62\\textheight,keepaspectratio]{{images/recuperados/{asset}}}\n"
                              f"\\caption{{{tex_escape(caption)}}}\n\\end{{table}}")
            skip_next = True
            continue
        if compact.startswith("FIGURA") and re.match(r"FIGURA[IVXLCDM]+\.\d+", compact):
            figure_i += 1
            caption = re.sub(r"^\s*F\s*IGURA\s+[IVXLCDM]+\.\d+:\s*", "", clean_unicode(joined), flags=re.I)
            asset = asset_map.get((page_no, "figure", figure_i))
            if asset:
                output.append("\\begin{figure}[H]\n\\centering\n"
                              f"\\includegraphics[width=0.96\\textwidth,height=0.72\\textheight,keepaspectratio]{{images/recuperados/{asset}}}\n"
                              f"\\caption{{{tex_escape(caption)}}}\n\\end{{figure}}")
            continue
        heading = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?\s+(.+)$", clean_unicode(joined))
        if heading:
            title = tex_escape(heading.group(4))
            output.append(("\\subsection" if heading.group(3) else "\\section") + "{" + title + "}")
            continue
        # Lists exported from the source PDF generally retain a visible numeric marker.
        if re.match(r"^\d+\.\s+", joined):
            output.append("\\noindent " + tex_escape(joined))
        else:
            output.append(tex_escape(joined))
    return "\n\n".join(output)


def repair_template_encoding():
    for path in [PROJECT / "main.tex", PROJECT / "tesisutec.cls", *PROJECT.glob("secciones/*.tex"), *PROJECT.glob("encabezados/*.tex")]:
        raw = path.read_text(encoding="utf-8")
        if "Ã" in raw or "Â" in raw:
            try:
                raw = raw.encode("latin1").decode("utf-8")
            except UnicodeError:
                raw = raw.replace("Ã", "Í").replace("Ã³", "ó").replace("Ã¡", "á").replace("Ãº", "ú")
            path.write_text(raw, encoding="utf-8")


def build():
    repair_template_encoding()
    pages = TXT.read_text(encoding="utf-8").split("\f")
    inventory = json.loads(INV.read_text(encoding="utf-8"))
    asset_map = crop_assets(inventory)

    # Spanish abstract from the source report.
    resumen_parts = []
    for p in split_paragraphs(pages[1]):
        joined = dewrap(p.splitlines())
        if not joined or is_page_number(joined) or clean_unicode(joined).upper() == "RESUMEN":
            continue
        resumen_parts.append(tex_escape(joined))
    (PROJECT / "secciones" / "resumen.tex").write_text(
        "\\chapter*{RESUMEN}\n\\addcontentsline{toc}{chapter}{RESUMEN}\n\n" + "\n\n".join(resumen_parts) + "\n",
        encoding="utf-8",
    )

    for chapter, (first, last) in CHAPTER_PAGES.items():
        chunks = [f"\\chapter{{{CHAPTER_TITLES[chapter].upper()}}}"]
        for page_no in range(first, last + 1):
            chunks.append(parse_page(page_no, pages[page_no - 1], asset_map))
        (PROJECT / "secciones" / f"capitulo{chapter}.tex").write_text("\n\n".join(chunks) + "\n", encoding="utf-8")

    # References are retained as numbered entries because the PDF does not expose citation keys.
    ref_text = "\n".join(dewrap(p.splitlines()) for n in (68, 69) for p in split_paragraphs(pages[n - 1]))
    ref_text = clean_unicode(ref_text)
    ref_text = re.sub(r"REFERENCIAS BIBLIOGRAFICAS", "", ref_text, flags=re.I)
    refs = re.split(r"(?=\[\d+\])", ref_text)
    refs = [re.sub(r"^\[\d+\]\s*", "", r).strip() for r in refs if re.match(r"^\[\d+\]", r.strip())]
    ref_lines = ["\\chapter*{REFERENCIAS BIBLIOGRÁFICAS}", "\\addcontentsline{toc}{chapter}{REFERENCIAS BIBLIOGRÁFICAS}", "\\begin{enumerate}"]
    ref_lines += [f"\\item {tex_reference(r)}" for r in refs]
    ref_lines.append("\\end{enumerate}")
    (PROJECT / "secciones" / "referencias.tex").write_text("\n".join(ref_lines) + "\n", encoding="utf-8")

    main = r'''\documentclass[a4paper,12pt,oneside]{tesisutec}
\graphicspath{{images/}}
\usepackage[spanish,es-tabla,es-nodecimaldot]{babel}
\usepackage{float}
\usepackage{enumitem}
\usepackage{microtype}
\usepackage{hyperref}
\hypersetup{urlcolor=blue,colorlinks=true,linkcolor=black,citecolor=blue}
\setlist{nosep,leftmargin=1.25cm}
\emergencystretch=3em

\begin{document}
\degree{Maestro en Ciencia de Datos e Inteligencia Artificial}
\title{NexusCare: Solución de auditoría automatizada de liquidaciones médicas basada en inteligencia artificial}
\author{Roberto Hurtado \\ Javier Linares}
\supervisor{Renzo Osso}
\date{2026}
\maketitle
\setcounter{page}{1}
\setstretch{1.5}

\renewcommand{\contentsname}{\Large\bfseries TABLA DE CONTENIDO}
\tableofcontents
\clearpage
\renewcommand{\listtablename}{\Large\bfseries ÍNDICE DE TABLAS}
\listoftables
\clearpage
\renewcommand{\listfigurename}{\Large\bfseries ÍNDICE DE FIGURAS}
\listoffigures
\clearpage

\pagestyle{fancy}
\input{secciones/resumen}
'''
    main += "\n".join(f"\\input{{secciones/capitulo{i}}}" for i in range(1, 15))
    main += "\n\\input{secciones/referencias}\n\\input{secciones/capitulo15}\n\\end{document}\n"
    (PROJECT / "main.tex").write_text(main, encoding="utf-8")

    readme = """# NexusCare - Informe Final UTEC\n\nProyecto reconstruido a partir de la plantilla oficial UTEC Posgrado y del informe PDF suministrado.\n\n## Compilación\n\n```powershell\nlatexmk -xelatex main.tex\n```\n\nEl texto permanece editable en `secciones/`. Las tablas y figuras recuperadas del PDF se encuentran en `images/recuperados/`.\n"""
    (PROJECT / "README.md").write_text(readme, encoding="utf-8")
    print(f"generated chapters=15 assets={len(asset_map)} refs={len(refs)}")


if __name__ == "__main__":
    build()
