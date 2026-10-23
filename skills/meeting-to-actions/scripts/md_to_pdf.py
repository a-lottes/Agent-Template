#!/usr/bin/env python3
"""Convert the project-memory Markdown files to PDF (standard library only).

Usage:
    md_to_pdf.py memory                  # every *.md in memory/ except processed.md
    md_to_pdf.py memory/actions.md       # a single file
    md_to_pdf.py                         # print this help

The PDF is written next to the Markdown file (actions.md -> actions.pdf) and one line
"<md> -> <pdf>" is printed per file. Markdown stays the source of truth: never edit the
PDFs by hand, they are overwritten on every run.

Supported: headings, paragraphs, bullet lists, quotes, pipe tables (bold header row,
column widths fitted to the text, wrapped cells). Inline Markdown (**bold**, `code`,
links) is rendered as plain text. Output: A4 portrait, Helvetica (WinAnsi), header
"Project Memory · <title>" with date, page numbers "n / m" at the bottom. The PDF is
written by hand (objects, xref, trailer), no third-party libraries.
"""
import datetime
import os
import re
import sys
import unicodedata

PAGE_W, PAGE_H = 595, 842
MARGIN = 50
CONTENT_W = PAGE_W - 2 * MARGIN
TOP = PAGE_H - 70
BOTTOM = 55

# Helvetica / Helvetica-Bold advance widths for ASCII 32..126 (1/1000 em).
_REG = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
        556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
        1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
        667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
        333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
        556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584]
_BOLD = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278,
         556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611,
         975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778,
         667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556,
         333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611,
         611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584]
_SPECIAL = {"·": 278, "•": 350, "–": 556, "—": 1000, "…": 1000, "ß": 611}
_REPLACE = {"→": "->", "←": "<-", "≥": ">=", "≤": "<=", "✓": "x", " ": " ", "\t": "    "}


def char_w(ch, bold):
    if ch in _SPECIAL:
        return _SPECIAL[ch]
    if 32 <= ord(ch) <= 126:
        return (_BOLD if bold else _REG)[ord(ch) - 32]
    base = unicodedata.normalize("NFD", ch)[0]
    if 32 <= ord(base) <= 126:
        return (_BOLD if bold else _REG)[ord(base) - 32]
    return 556


def text_w(s, size, bold=False):
    return sum(char_w(c, bold) for c in s) * size / 1000.0


def clean(s):
    """Inline Markdown to plain text."""
    s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", s)
    s = re.sub(r"(\*\*|__)(.+?)\1", r"\2", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"\1", s)
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = s.replace("\\|", "|")
    for a, b in _REPLACE.items():
        s = s.replace(a, b)
    return s.strip()


def wrap(text, width, size, bold=False):
    """Greedy word wrap; words wider than the line are broken by character."""
    lines, cur = [], ""
    for word in text.split():
        while text_w(word, size, bold) > width:
            room = cur + (" " if cur else "")
            cut = len(word)
            while cut > 1 and text_w(room + word[:cut], size, bold) > width:
                cut -= 1
            if not cur and cut == 1 and text_w(word[:1], size, bold) > width:
                break
            if text_w(room + word[:cut], size, bold) > width:
                lines.append(cur)
                cur = ""
                continue
            lines.append(room + word[:cut])
            cur, word = "", word[cut:]
        cand = (cur + " " + word) if cur else word
        if cur and text_w(cand, size, bold) > width:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    if cur or not lines:
        lines.append(cur)
    return lines


def pdf_str(s):
    out = []
    for b in s.encode("cp1252", errors="replace"):
        if b in (0x28, 0x29, 0x5C):
            out.append("\\" + chr(b))
        elif 32 <= b <= 126:
            out.append(chr(b))
        else:
            out.append("\\%03o" % b)
    return "(" + "".join(out) + ")"


class Doc:
    def __init__(self):
        self.pages = [[]]
        self.y = TOP

    def new_page(self):
        self.pages.append([])
        self.y = TOP

    def ensure(self, h):
        if self.y - h < BOTTOM:
            self.new_page()

    def text(self, x, y, s, size, bold=False, gray=0.0):
        font = "F2" if bold else "F1"
        self.pages[-1].append("BT %.2f g /%s %.1f Tf %.2f %.2f Td %s Tj ET"
                              % (gray, font, size, x, y, pdf_str(s)))

    def rect(self, x, y, w, h, gray):
        self.pages[-1].append("%.2f g %.2f %.2f %.2f %.2f re f" % (gray, x, y, w, h))

    def line(self, x1, y1, x2, y2, gray=0.6, width=0.5):
        self.pages[-1].append("%.2f G %.2f w %.2f %.2f m %.2f %.2f l S" % (gray, width, x1, y1, x2, y2))

    def block(self, text, size, bold=False, indent=0.0, gray=0.0, first="", bar=False, after=4.0):
        lead = size * 1.35
        hang = text_w(first, size, bold) + 4 if first else 0
        x = MARGIN + indent
        for i, ln in enumerate(wrap(text, CONTENT_W - indent - hang, size, bold)):
            self.ensure(lead)
            self.y -= lead
            if i == 0 and first:
                self.text(x, self.y, first, size, bold, gray)
            self.text(x + hang, self.y, ln, size, bold, gray)
            if bar:
                self.line(x - 8, self.y - size * 0.25, x - 8, self.y + size * 0.95, 0.75, 1.5)
        self.y -= after

    def heading(self, text, level):
        size = {1: 18, 2: 14, 3: 12}.get(level, 11)
        self.ensure(size * 1.35 * 2 + 14)
        self.y -= 8 if level > 1 else 4
        self.block(text, size, bold=True, after=4)
        if level == 1:
            self.line(MARGIN, self.y + 2, PAGE_W - MARGIN, self.y + 2)
            self.y -= 6

    def table(self, rows):
        size, pad, lead = 8.0, 3.0, 8.0 * 1.3
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        nat, low = [0.0] * ncol, [0.0] * ncol
        for ri, r in enumerate(rows):
            for ci, cell in enumerate(r):
                b = ri == 0
                nat[ci] = max(nat[ci], text_w(cell, size, b))
                for w in cell.split():
                    low[ci] = max(low[ci], min(text_w(w, size, b), 70.0))
        avail = CONTENT_W - 2 * pad * ncol
        if sum(nat) <= avail:
            widths = [n * avail / max(sum(nat), 1) for n in nat]
        else:
            low = [min(l, avail / ncol) for l in low]
            extra = max(avail - sum(low), 0)
            grow = [max(n - l, 0) for n, l in zip(nat, low)]
            widths = [l + extra * g / max(sum(grow), 1) for l, g in zip(low, grow)]
        widths = [w + 2 * pad for w in widths]

        def draw_row(ri, cells):
            wrapped = [wrap(c, widths[ci] - 2 * pad, size, ri == 0) for ci, c in enumerate(cells)]
            h = max(len(w) for w in wrapped) * lead + 2 * pad
            if self.y - h < BOTTOM:
                self.new_page()
                if ri != 0:
                    draw_row(0, rows[0])
            top = self.y
            if ri == 0:
                self.rect(MARGIN, top - h, CONTENT_W, h, 0.9)
            x = MARGIN
            for ci, lines in enumerate(wrapped):
                for li, ln in enumerate(lines):
                    self.text(x + pad, top - pad - (li + 1) * lead + 2.5, ln, size, ri == 0)
                x += widths[ci]
            self.line(MARGIN, top - h, PAGE_W - MARGIN, top - h)
            self.y = top - h

        self.y -= 2
        self.line(MARGIN, self.y, PAGE_W - MARGIN, self.y)
        for ri, r in enumerate(rows):
            draw_row(ri, r)
        self.y -= 8


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [clean(c) for c in re.split(r"(?<!\\)\|", s)]


def is_sep(cells):
    return all(re.fullmatch(r":?-{1,}:?", c.strip()) for c in cells if c.strip()) and any(cells)


def render(md, fallback_title):
    doc = Doc()
    title = None
    lines = md.splitlines()
    if lines and lines[0].strip() == "---":  # skip front matter
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        lines = lines[end + 1:] if end else lines
    i, para = 0, []

    def flush():
        if para:
            doc.block(clean(" ".join(para)), 10, after=6)
            para.clear()

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if not s:
            flush()
        elif s.startswith("|"):
            flush()
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = split_row(lines[i])
                if not is_sep(cells):
                    tbl.append(cells)
                i += 1
            if tbl:
                doc.table(tbl)
            continue
        elif re.match(r"#{1,6}\s", s):
            flush()
            level = len(s) - len(s.lstrip("#"))
            text = clean(s[level:])
            title = title or (text if level == 1 else None)
            doc.heading(text, level)
        elif re.match(r"[-*+]\s+", s):
            flush()
            depth = (len(raw) - len(raw.lstrip())) // 2
            doc.block(clean(re.sub(r"^[-*+]\s+", "", s)), 10, indent=12 + 14 * depth, first="•", after=2)
        elif s.startswith(">"):
            flush()
            doc.block(clean(s.lstrip("> ")), 10, indent=18, gray=0.4, bar=True, after=4)
        elif re.fullmatch(r"([-*_])\1{2,}", s):
            flush()
            doc.ensure(10)
            doc.y -= 4
            doc.line(MARGIN, doc.y, PAGE_W - MARGIN, doc.y)
            doc.y -= 6
        else:
            para.append(s)
        i += 1
    flush()
    return doc, title or fallback_title


def build_pdf(doc, title):
    today = datetime.date.today().isoformat()
    total = len(doc.pages)
    head = "Project Memory · " + title
    for n, ops in enumerate(doc.pages, 1):
        saved, doc.pages = doc.pages, [ops]
        doc.text(MARGIN, PAGE_H - 40, head, 9, bold=True, gray=0.3)
        doc.text(PAGE_W - MARGIN - text_w(today, 9), PAGE_H - 40, today, 9, gray=0.3)
        doc.line(MARGIN, PAGE_H - 46, PAGE_W - MARGIN, PAGE_H - 46)
        foot = "%d / %d" % (n, total)
        doc.text((PAGE_W - text_w(foot, 9)) / 2, 28, foot, 9, gray=0.3)
        doc.pages = saved

    objs = {1: "<< /Type /Catalog /Pages 2 0 R >>"}
    kids = []
    objs[3] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    objs[4] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
    num = 5
    for ops in doc.pages:
        page, content = num, num + 1
        num += 2
        kids.append("%d 0 R" % page)
        stream = "\n".join(ops).encode("cp1252", errors="replace")
        objs[page] = ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
                      "/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents %d 0 R >>"
                      % (PAGE_W, PAGE_H, content))
        objs[content] = stream
    objs[2] = "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join(kids), len(kids))

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = {}
    for n in sorted(objs):
        offsets[n] = len(out)
        body = objs[n]
        if isinstance(body, bytes):
            out += b"%d 0 obj\n<< /Length %d >>\nstream\n" % (n, len(body)) + body + b"\nendstream\nendobj\n"
        else:
            out += ("%d 0 obj\n%s\nendobj\n" % (n, body)).encode("latin-1")
    xref = len(out)
    out += ("xref\n0 %d\n%010d 65535 f \n" % (num, 0)).encode()
    for n in range(1, num):
        out += ("%010d 00000 n \n" % offsets[n]).encode()
    out += ("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (num, xref)).encode()
    return bytes(out)


def convert(md_path):
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    stem = os.path.splitext(os.path.basename(md_path))[0]
    doc, title = render(md, stem.replace("-", " ").replace("_", " ").title())
    pdf_path = os.path.splitext(md_path)[0] + ".pdf"
    with open(pdf_path, "wb") as f:
        f.write(build_pdf(doc, title))
    print("%s -> %s" % (md_path, pdf_path))


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    target = argv[0]
    if os.path.isdir(target):
        files = sorted(os.path.join(target, n) for n in os.listdir(target)
                       if n.endswith(".md") and n != "processed.md")
        if not files:
            print("No Markdown files in %s" % target, file=sys.stderr)
            return 1
    elif os.path.isfile(target):
        files = [target]
    else:
        print("Not found: %s" % target, file=sys.stderr)
        return 1
    for f in files:
        convert(f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
