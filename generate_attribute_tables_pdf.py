"""Render the node, edge, and graph attribute tables in review/ from CSV to PDF.

Each CSV holds two blocks, attributes followed by performance measures, in
three columns (Sr, name, description). This script rebuilds each CSV as a
print-formatted spreadsheet and converts it with LibreOffice headless, so the
three PDFs stay consistent with each other and with their CSV sources.

Usage (from the repo root):
    python generate_attribute_tables_pdf.py

Requires: odfpy, LibreOffice.
"""

import csv
import io
import os
import shutil
import subprocess
import tempfile

from odf.namespaces import STYLENS
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import (Footer, FooterStyle, Header, HeaderFooterProperties,
                       HeaderStyle, MasterPage, PageLayout,
                       PageLayoutProperties, ParagraphProperties, RegionCenter,
                       Style, TableCellProperties, TableColumnProperties,
                       TableProperties, TableRowProperties, TextProperties)
from odf.table import CoveredTableCell, Table, TableCell, TableColumn, TableRow
from odf.text import P, PageNumber

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
REVIEW_DIR = os.path.join(REPO_DIR, "review")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

TABLES = [
    "Node attributes and performance measures",
    "Edge attributes and performance measures",
    "Graph attributes and performance measures",
]

# Print settings
PAGE_WIDTH = "29.7cm"      # A4 landscape
PAGE_HEIGHT = "21cm"
MARGIN = "2cm"
FONT_FAMILY = "Liberation Sans"
FONT_SIZE = "10pt"
# Column widths (cm): Sr, name, description. Together they must fit the page
# width minus margins, and the description column must be wide enough for the
# longest description so that no row wraps.
COLUMN_WIDTHS = [0.7, 5.6, 19.4]


def read_table(path):
    """Return the CSV rows padded to three columns, trailing blanks dropped."""
    with io.open(path, encoding="utf-8-sig", newline="") as handle:
        rows = [(row + ["", "", ""])[:3] for row in csv.reader(handle)]
    while rows and not any(cell.strip() for cell in rows[-1]):
        rows.pop()
    return rows


def build_styles(doc, title):
    layout = PageLayout(name="PL1")
    props = PageLayoutProperties(
        pagewidth=PAGE_WIDTH, pageheight=PAGE_HEIGHT,
        printorientation="landscape",
        margintop=MARGIN, marginbottom=MARGIN,
        marginleft=MARGIN, marginright=MARGIN,
    )
    props.setAttrNS(STYLENS, "print", "grid")   # print the cell grid, no borders
    props.setAttrNS(STYLENS, "scale-to-X", "1")  # fit all columns to one page wide
    layout.addElement(props)

    header_style = HeaderStyle()
    header_style.addElement(HeaderFooterProperties(
        minheight="0.75cm", marginleft="0cm", marginright="0cm",
        marginbottom="0.25cm", dynamicspacing="true"))
    layout.addElement(header_style)

    footer_style = FooterStyle()
    footer_style.addElement(HeaderFooterProperties(
        minheight="0.75cm", marginleft="0cm", marginright="0cm",
        margintop="0.25cm", dynamicspacing="true"))
    layout.addElement(footer_style)
    doc.automaticstyles.addElement(layout)

    master = MasterPage(name="Default", pagelayoutname=layout)

    header = Header()
    header_region = RegionCenter()
    header_region.addElement(P(text=title))
    header.addElement(header_region)
    master.addElement(header)

    footer = Footer()
    footer_region = RegionCenter()
    footer_paragraph = P(text="Page ")
    footer_paragraph.addElement(PageNumber(selectpage="current"))
    footer_region.addElement(footer_paragraph)
    footer.addElement(footer_region)
    master.addElement(footer)

    doc.masterstyles.addElement(master)

    table_style = Style(name="ta1", family="table", masterpagename="Default")
    table_style.addElement(TableProperties(display="true"))
    doc.automaticstyles.addElement(table_style)

    column_styles = []
    for index, width in enumerate(COLUMN_WIDTHS):
        style = Style(name="co%d" % index, family="table-column")
        style.addElement(TableColumnProperties(columnwidth="%scm" % width))
        doc.automaticstyles.addElement(style)
        column_styles.append(style)

    row_style = Style(name="ro1", family="table-row")
    row_style.addElement(TableRowProperties(useoptimalrowheight="true"))
    doc.automaticstyles.addElement(row_style)

    cell_properties = dict(wrapoption="wrap", verticalalign="top",
                           paddingleft="0.05cm", paddingright="0.05cm",
                           paddingtop="0.02cm", paddingbottom="0.02cm")

    body_cell = Style(name="ce_body", family="table-cell")
    body_cell.addElement(TableCellProperties(**cell_properties))
    body_cell.addElement(TextProperties(fontfamily=FONT_FAMILY, fontsize=FONT_SIZE))
    doc.automaticstyles.addElement(body_cell)

    # Block titles ("Supply Chain Node Attributes" and the like) are centred
    # across the name and description columns.
    section_cell = Style(name="ce_section", family="table-cell")
    section_cell.addElement(TableCellProperties(**cell_properties))
    section_cell.addElement(TextProperties(fontfamily=FONT_FAMILY, fontsize=FONT_SIZE))
    section_cell.addElement(ParagraphProperties(textalign="center"))
    doc.automaticstyles.addElement(section_cell)

    return table_style, column_styles, row_style, body_cell, section_cell


def build_print_ods(rows, title, out_path):
    doc = OpenDocumentSpreadsheet()
    table_style, column_styles, row_style, body_cell, section_cell = \
        build_styles(doc, title)

    table = Table(name=title[:31], stylename=table_style)
    for style in column_styles:
        table.addElement(TableColumn(stylename=style, defaultcellstylename=body_cell))

    def add_cell(row, text, style, spanned=0):
        cell = TableCell(valuetype="string", stylename=style)
        if spanned:
            cell.setAttribute("numbercolumnsspanned", str(spanned))
            cell.setAttribute("numberrowsspanned", "1")
        cell.addElement(P(text=text))
        row.addElement(cell)

    for values in rows:
        row = TableRow(stylename=row_style)
        is_section = not values[0].strip() and values[1].strip() and not values[2].strip()
        if is_section:
            add_cell(row, values[0], body_cell)
            add_cell(row, values[1], section_cell, spanned=2)
            row.addElement(CoveredTableCell())
        else:
            for value, style in zip(values, (body_cell, body_cell, body_cell)):
                add_cell(row, value, style)
        table.addElement(row)

    doc.spreadsheet.addElement(table)
    doc.save(out_path)


def main():
    for title in TABLES:
        csv_path = os.path.join(REVIEW_DIR, title + ".csv")
        pdf_path = os.path.join(REVIEW_DIR, title + ".pdf")
        rows = read_table(csv_path)
        entries = sum(1 for row in rows if row[0].strip().isdigit())
        print("read %d rows (%d numbered entries) from %s"
              % (len(rows), entries, os.path.basename(csv_path)))

        with tempfile.TemporaryDirectory() as tmp:
            tmp_ods = os.path.join(tmp, "print_tmp.ods")
            build_print_ods(rows, title, tmp_ods)
            subprocess.run(
                [SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", tmp, tmp_ods],
                check=True,
            )
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            shutil.move(os.path.join(tmp, "print_tmp.pdf"), pdf_path)
        print("saved %s" % pdf_path)


if __name__ == "__main__":
    main()
