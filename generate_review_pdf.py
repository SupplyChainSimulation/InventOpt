"""Print the 'Categorization (merged)' sheet of Review.ods to review/Reviewed papers categorization.pdf.

Converting Review.ods directly gives a bad printout (the sheet carries stored
print state that breaks the page every ~2 rows), so this script rebuilds a
clean single-sheet spreadsheet from the cell values with print-friendly
formatting, then converts it with LibreOffice headless.

Usage (from the repo root):
    python generate_review_pdf.py

Requires: odfpy, LibreOffice. Review.ods may be open in LibreOffice while
this runs, but unsaved changes will not appear in the PDF.
"""

import os
import shutil
import subprocess
import sys
import tempfile

from odf.namespaces import STYLENS
from odf.opendocument import OpenDocumentSpreadsheet, load
from odf.style import (MasterPage, PageLayout, PageLayoutProperties,
                       ParagraphProperties, Style, TableCellProperties,
                       TableColumnProperties, TableProperties,
                       TableRowProperties, TextProperties)
from odf.table import (Table, TableCell, TableColumn, TableHeaderRows,
                       TableRow)
from odf.text import P

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_ODS = os.path.join(REPO_DIR, "Review.ods")
SHEET_NAME = "Categorization (merged)"
OUTPUT_PDF = os.path.join(REPO_DIR, "review", "Reviewed papers categorization.pdf")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

# Print settings
PAGE_WIDTH = "42cm"        # A3 landscape
PAGE_HEIGHT = "29.7cm"
MARGIN = "1cm"
FONT_SIZE = "8pt"
HEADER_BG = "#B3C6E7"
# Column widths (cm): Sr, Supply chain problem, Application domain, Title,
# Specific aspect, Tools, Simulation method, Optimization method, Comments,
# Any attributes. Together they must fit the page width minus margins.
COLUMN_WIDTHS = [0.9, 3.2, 3.0, 5.5, 6.0, 2.4, 2.4, 3.0, 7.5, 5.0]


def read_sheet(path, sheet_name):
    doc = load(path)
    for table in doc.spreadsheet.getElementsByType(Table):
        if table.getAttribute("name") == sheet_name:
            rows = []
            for row in table.getElementsByType(TableRow):
                cells = []
                for cell in row.getElementsByType(TableCell):
                    cells.append("\n".join(str(p) for p in cell.getElementsByType(P)))
                rows.append(cells[: len(COLUMN_WIDTHS)])
            return rows
    sys.exit(f"Sheet {sheet_name!r} not found in {path}")


def build_print_ods(rows, out_path):
    doc = OpenDocumentSpreadsheet()

    layout = PageLayout(name="PL1")
    props = PageLayoutProperties(
        pagewidth=PAGE_WIDTH, pageheight=PAGE_HEIGHT,
        printorientation="landscape",
        margintop=MARGIN, marginbottom=MARGIN,
        marginleft=MARGIN, marginright=MARGIN,
    )
    props.setAttrNS(STYLENS, "scale-to-X", "1")  # fit all columns to one page wide
    layout.addElement(props)
    doc.automaticstyles.addElement(layout)
    doc.masterstyles.addElement(MasterPage(name="Default", pagelayoutname=layout))

    table_style = Style(name="ta1", family="table", masterpagename="Default")
    table_style.addElement(TableProperties(display="true"))
    doc.automaticstyles.addElement(table_style)

    column_styles = []
    for i, width in enumerate(COLUMN_WIDTHS):
        style = Style(name=f"co{i}", family="table-column")
        style.addElement(TableColumnProperties(columnwidth=f"{width}cm"))
        doc.automaticstyles.addElement(style)
        column_styles.append(style)

    row_style = Style(name="ro1", family="table-row")
    row_style.addElement(TableRowProperties(useoptimalrowheight="true"))
    doc.automaticstyles.addElement(row_style)

    body_cell = Style(name="ce_base", family="table-cell")
    # The generous bottom padding is load-bearing: LibreOffice's optimal row
    # height comes out one text line short for some wrapped cells, clipping
    # the last line into the row below. The padding absorbs that error.
    body_cell.addElement(TableCellProperties(
        wrapoption="wrap", verticalalign="top",
        border="0.5pt solid #808080",
        paddingleft="0.05cm", paddingright="0.05cm",
        paddingtop="0.05cm", paddingbottom="0.4cm"))
    body_cell.addElement(TextProperties(fontsize=FONT_SIZE))
    doc.automaticstyles.addElement(body_cell)

    head_cell = Style(name="ce_head", family="table-cell")
    head_cell.addElement(TableCellProperties(
        wrapoption="wrap", verticalalign="middle",
        border="0.5pt solid #808080", backgroundcolor=HEADER_BG,
        padding="0.05cm"))
    head_cell.addElement(TextProperties(fontsize=FONT_SIZE, fontweight="bold"))
    head_cell.addElement(ParagraphProperties(textalign="center"))
    doc.automaticstyles.addElement(head_cell)

    table = Table(name=SHEET_NAME, stylename=table_style)
    for style in column_styles:
        table.addElement(TableColumn(stylename=style, defaultcellstylename=body_cell))

    def make_row(values, cell_style):
        row = TableRow(stylename=row_style)
        for value in values:
            cell = TableCell(valuetype="string", stylename=cell_style)
            for paragraph in value.split("\n"):
                cell.addElement(P(text=paragraph))
            row.addElement(cell)
        return row

    header = TableHeaderRows()  # repeats the heading row on every printed page
    header.addElement(make_row(rows[0], head_cell))
    table.addElement(header)
    for values in rows[1:]:
        table.addElement(make_row(values, body_cell))

    doc.spreadsheet.addElement(table)
    doc.save(out_path)


def main():
    rows = read_sheet(SOURCE_ODS, SHEET_NAME)
    print(f"read {len(rows) - 1} data rows from {SHEET_NAME!r}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_ods = os.path.join(tmp, "print_tmp.ods")
        build_print_ods(rows, tmp_ods)
        subprocess.run(
            [SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", tmp, tmp_ods],
            check=True,
        )
        tmp_pdf = os.path.join(tmp, "print_tmp.pdf")
        os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)
        if os.path.exists(OUTPUT_PDF):
            os.remove(OUTPUT_PDF)
        shutil.move(tmp_pdf, OUTPUT_PDF)
    print(f"saved {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
