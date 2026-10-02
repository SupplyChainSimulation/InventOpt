"""Write review/Reviewed papers categorization.csv from the 'Categorization (merged)' sheet of Review.ods.

Only rows whose Included column is "yes" are written; the rejected rows stay in
Review.ods, highlighted, as the record of the screening. Rows are renumbered 1..N
in sheet order. The Link and Included columns are working columns and are not
published.

Usage (from the repo root):
    python generate_review_csv.py

Requires: odfpy. Review.ods may be open in LibreOffice while this runs, but
unsaved changes will not appear in the CSV.
"""

import csv
import os
import sys

from odf.opendocument import load
from odf.table import Table, TableCell, TableRow
from odf.text import P

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_ODS = os.path.join(REPO_DIR, "Review.ods")
SHEET_NAME = "Categorization (merged)"
OUTPUT_CSV = os.path.join(REPO_DIR, "review", "Reviewed papers categorization.csv")
PUBLIC_COLUMNS = [
    "Sr", "Supply chain problem", "Application domain", "Title", "Year", "Venue",
    "Specific aspect / SC aspect", "Tools used to build the model", "Simulation method used",
    "Optimization/prediction method used", "Comments", "Any attributes",
]


def paragraph_text(node):
    """Text of a paragraph, keeping repeated spaces (text:s), tabs and line breaks."""
    out = []
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE:
            out.append(child.data)
        elif child.qname[1] == "s":
            out.append(" " * int(child.getAttribute("c") or 1))
        elif child.qname[1] == "tab":
            out.append("\t")
        elif child.qname[1] == "line-break":
            out.append("\n")
        else:
            out.append(paragraph_text(child))
    return "".join(out)


def read_sheet(path=SOURCE_ODS, sheet_name=SHEET_NAME):
    """Return the sheet as a list of rows, each a list of cell strings (paragraphs joined by newlines)."""
    doc = load(path)
    for table in doc.spreadsheet.getElementsByType(Table):
        if table.getAttribute("name") != sheet_name:
            continue
        rows = []
        for row in table.getElementsByType(TableRow):
            cells = []
            for cell in row.getElementsByType(TableCell):
                text = "\n".join(paragraph_text(p) for p in cell.getElementsByType(P))
                repeat = int(cell.getAttribute("numbercolumnsrepeated") or 1)
                cells.extend([text] * min(repeat, 64))
            if any(c.strip() for c in cells):
                rows.append(cells)
        return rows
    sys.exit(f"Sheet {sheet_name!r} not found in {path}")


def public_rows(path=SOURCE_ODS):
    """Header plus the included rows, renumbered, restricted to PUBLIC_COLUMNS."""
    rows = read_sheet(path)
    header = rows[0]
    missing = [c for c in PUBLIC_COLUMNS + ["Included"] if c not in header]
    if missing:
        sys.exit(f"Columns missing from {SHEET_NAME!r}: {missing}")
    idx = {c: header.index(c) for c in header if c}
    out = [PUBLIC_COLUMNS]
    for cells in rows[1:]:
        cells = cells + [""] * (len(header) - len(cells))
        if cells[idx["Included"]].strip().lower() != "yes":
            continue
        values = [cells[idx[c]] for c in PUBLIC_COLUMNS]
        values[0] = str(len(out))
        out.append(values)
    return out


def main():
    rows = public_rows()
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(rows)
    print(f"wrote {len(rows) - 1} papers to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
