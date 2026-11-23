"""Konverter laporan markdown menjadi dokumen Word (.docx) berformat rapi."""
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "Dokumentasi/laporan_project.md"
DOCX_PATH = ROOT / "Dokumentasi/laporan_project.docx"


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def make_docx():
    lines = MD_PATH.read_text(encoding="utf-8").splitlines()
    doc = docx.Document()

    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(0x2d, 0x37, 0x48)

    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return
        
        # Determine number of columns
        cols_count = max(len(r) for r in table_rows)
        tbl = doc.add_table(rows=len(table_rows), cols=cols_count)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.style = 'Table Grid'

        for r_idx, row in enumerate(table_rows):
            is_header = (r_idx == 0)
            for c_idx, cell_text in enumerate(row):
                if c_idx < cols_count:
                    cell = tbl.cell(r_idx, c_idx)
                    cell.text = cell_text.strip()
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(3)
                    run = p.runs[0]
                    run.font.name = 'Calibri'
                    run.font.size = Pt(9.5)
                    if is_header:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(0xff, 0xff, 0xff)
                        set_cell_background(cell, "16817A")
                    else:
                        if r_idx % 2 == 1:
                            set_cell_background(cell, "F7FAFC")
                        else:
                            set_cell_background(cell, "EDF2F7")

        doc.add_paragraph()  # Spacing
        table_rows = []
        in_table = False

    for line in lines:
        stripped = line.strip()

        # Handle Markdown Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # Check if separator row
            if all(set(c).issubset({'-', ':', ' '}) for c in cells):
                continue
            in_table = True
            table_rows.append(cells)
            continue
        elif in_table:
            flush_table()

        if not stripped:
            continue

        if stripped.startswith("# "):
            h = doc.add_heading(level=1)
            run = h.add_run(stripped[2:])
            run.font.name = 'Calibri'
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x10, 0x2a, 0x43)
            h.paragraph_format.space_before = Pt(12)
            h.paragraph_format.space_after = Pt(6)
        elif stripped.startswith("## "):
            h = doc.add_heading(level=2)
            run = h.add_run(stripped[3:])
            run.font.name = 'Calibri'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x16, 0x81, 0x7a)
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
        elif stripped.startswith("### "):
            h = doc.add_heading(level=3)
            run = h.add_run(stripped[4:])
            run.font.name = 'Calibri'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x24, 0x3b, 0x53)
            h.paragraph_format.space_before = Pt(8)
            h.paragraph_format.space_after = Pt(2)
        elif stripped.startswith("---"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            text = stripped[2:]
            run = p.add_run(text)
            run.font.name = 'Calibri'
            run.font.size = Pt(10.5)
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1:3] in ['. ', ') ']:
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            text = stripped[3:]
            run = p.add_run(text)
            run.font.name = 'Calibri'
            run.font.size = Pt(10.5)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(stripped)
            run.font.name = 'Calibri'
            run.font.size = Pt(11)

    if in_table:
        flush_table()

    doc.save(DOCX_PATH)
    print("Dokumen Word tersimpan di:", DOCX_PATH)


if __name__ == "__main__":
    make_docx()
