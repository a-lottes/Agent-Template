#!/usr/bin/env python3
"""Render project-memory Markdown files as PDF, next to the .md file. No dependencies.

    md_to_pdf.py memory                 # every memory/*.md (except processed.md)
    md_to_pdf.py memory/actions.md      # single file

Supports what the memory files use: headings, paragraphs, bullet lists, quotes and
pipe tables. Inline Markdown (**bold**, `code`, links) is rendered as plain text.
"""
import re
import sys
from datetime import date
from pathlib import Path

PAGE_W, PAGE_H = 595.28, 841.89          # A4 portrait, points
MARGIN = 50
BODY, SMALL = 10, 8
SKIP = {"processed.md"}

# Approximate Helvetica widths (1/1000 em), good enough for line wrapping.
NARROW = set("ijl.,:;'|!()[]{}-/ ftrI")
WIDE = set("mwMW@%")


def text_width(text: str, size: float, bold: bool = False) -> float:
    units = sum(278 if c in NARROW else 833 if c in WIDE else 667 if c.isupper() else 556 for c in text)
    return units * size / 1000 * (1.05 if bold else 1)


def plain(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`]{1,3}([^*_`]+)[*_`]{1,3}", r"\1", text)
    return text.replace("→", "->").replace("✓", "v").replace("✗", "x").strip()


def wrap(text: str, width: float, size: float, bold: bool = False) -> list:
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if text_width(candidate, size, bold) <= width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines or [""]


def pdf_string(text: str) -> str:
    raw = text.encode("cp1252", errors="replace").decode("latin-1")
    return "(" + raw.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ")"


class Pdf:
    def __init__(self, title: str):
        self.title = title
        self.pages, self.ops = [], []
        self.y = 0
        self.new_page()

    def new_page(self):
        if self.ops:
            self.pages.append(self.ops)
        self.ops = []
        self.y = PAGE_H - MARGIN
        self.text(MARGIN, PAGE_H - 30, f"Project Memory · {self.title}", SMALL, gray=0.45)
        self.text(PAGE_W - MARGIN - 60, PAGE_H - 30, date.today().isoformat(), SMALL, gray=0.45)
        self.y -= 10

    def need(self, height: float):
        if self.y - height < MARGIN + 20:
            self.new_page()

    def text(self, x, y, s, size, bold=False, gray=0.0):
        font = "F2" if bold else "F1"
        self.ops.append(f"BT {gray} g /{font} {size} Tf {x:.1f} {y:.1f} Td {pdf_string(s)} Tj ET")

    def rect(self, x, y, w, h, fill=None):
        if fill is not None:
            self.ops.append(f"{fill} g {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f")
        self.ops.append(f"0.7 G 0.5 w {x:.1f} {y:.1f} {w:.1f} {h:.1f} re S")

    def paragraph(self, s, size=BODY, bold=False, indent=0, gap=4, gray=0.0, prefix=""):
        width = PAGE_W - 2 * MARGIN - indent
        for i, line in enumerate(wrap(s, width - 12, size, bold)):
            self.need(size + 3)
            self.y -= size + 3
            if prefix and i == 0:
                self.text(MARGIN + indent - 10, self.y, prefix, size)
            self.text(MARGIN + indent, self.y, line, size, bold, gray)
        self.y -= gap

    def table(self, rows):
        header, body = rows[0], rows[1:]
        cols = len(header)
        usable = PAGE_W - 2 * MARGIN
        size, pad = 8, 3
        cell = lambda r, i: r[i] if i < len(r) else ""
        # Each column at least as wide as its longest word, the rest shared by text length.
        minimum = [max(text_width(w, size, True) for r in rows for w in (cell(r, i).split() or [""])) + 2 * pad + 2
                   for i in range(cols)]
        want = [max(min(len(cell(r, i)), 60) for r in rows) + 4 for i in range(cols)]
        spare = max(usable - sum(minimum), 0)
        widths = [m + spare * n / sum(want) for m, n in zip(minimum, want)]
        widths = [w * usable / sum(widths) for w in widths]

        def draw_row(cells, bold, fill):
            wrapped = [wrap(cells[i] if i < len(cells) else "", widths[i] - 2 * pad, size, bold)
                       for i in range(cols)]
            height = max(len(w) for w in wrapped) * (size + 2) + 2 * pad
            self.need(height)
            x = MARGIN
            for i, lines in enumerate(wrapped):
                self.rect(x, self.y - height, widths[i], height, fill)
                for j, line in enumerate(lines):
                    self.text(x + pad, self.y - pad - (j + 1) * (size + 2) + 2, line, size, bold)
                x += widths[i]
            self.y -= height

        draw_row(header, True, 0.92)
        for row in body:
            if self.y - 20 < MARGIN + 20:
                self.new_page()
                draw_row(header, True, 0.92)
            draw_row(row, False, None)
        self.y -= 8

    def save(self, path: Path):
        self.pages.append(self.ops)
        objs = ["<< /Type /Catalog /Pages 2 0 R >>", None,
                "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
                "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"]
        kids = []
        for n, ops in enumerate(self.pages, 1):
            ops = ops + [f"BT 0.45 g /F1 {SMALL} Tf {PAGE_W / 2 - 15:.1f} 30 Td "
                         f"{pdf_string(f'{n} / {len(self.pages)}')} Tj ET"]
            stream = "\n".join(ops).encode("latin-1")
            objs.append(f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream")
            objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
                        f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {len(objs)} 0 R >>")
            kids.append(f"{len(objs)} 0 R")
        objs[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>"

        out, offsets = bytearray(b"%PDF-1.4\n"), []
        for i, obj in enumerate(objs, 1):
            offsets.append(len(out))
            body = obj if isinstance(obj, bytes) else obj.encode("latin-1")
            out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
        xref = len(out)
        out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
        out += "".join(f"{o:010d} 00000 n \n" for o in offsets).encode()
        out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
        path.write_bytes(bytes(out))


def render(md_path: Path) -> Path:
    pdf = Pdf(md_path.stem.replace("-", " ").title())
    lines = md_path.read_text(encoding="utf-8").splitlines()
    if not any(l.startswith("# ") for l in lines):
        pdf.paragraph(pdf.title, size=16, bold=True, gap=8)
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [plain(c) for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                pdf.table(rows)
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            pdf.y -= 6
            pdf.paragraph(plain(line.lstrip("#")), size={1: 16, 2: 13}.get(level, 11), bold=True, gap=6)
        elif re.match(r"^\s*[-*] ", line):
            pdf.paragraph(plain(re.sub(r"^\s*[-*] ", "", line)), indent=14, gap=2, prefix="•")
        elif line.startswith(">"):
            pdf.paragraph(plain(line.lstrip("> ")), indent=14, gray=0.35)
        elif line.strip():
            pdf.paragraph(plain(line))
        i += 1
    target = md_path.with_suffix(".pdf")
    pdf.save(target)
    return target


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    paths = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        paths += sorted(f for f in p.rglob("*.md") if f.name not in SKIP) if p.is_dir() else [p]
    for path in paths:
        print(f"{path} -> {render(path)}")


if __name__ == "__main__":
    main()
