"""Write review/Reviewed papers categorization.csv from the 'Categorization (merged)' sheet of Review.ods.

Only rows whose Included column is "yes" are written; the rejected rows stay in
Review.ods, highlighted, as the record of the screening. Rows are sorted by their
first supply chain problem (alphabetical, 'Other' last), then year, then title,
and renumbered 1..N; Review.ods keeps its working order. The Link and Included
columns are working columns and are not published.

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
    kept = []
    for cells in rows[1:]:
        cells = cells + [""] * (len(header) - len(cells))
        if cells[idx["Included"]].strip().lower() == "yes":
            kept.append([cells[idx[c]] for c in PUBLIC_COLUMNS])
    kept.sort(key=sort_key)
    for n, values in enumerate(kept, start=1):
        values[0] = str(n)
    return [PUBLIC_COLUMNS] + kept


def sort_key(values):
    """Group by the first supply chain problem (alphabetical, 'Other' last), then year, then title."""
    problem = values[PUBLIC_COLUMNS.index("Supply chain problem")].split(";")[0].strip()
    year = values[PUBLIC_COLUMNS.index("Year")]
    title = values[PUBLIC_COLUMNS.index("Title")]
    return (problem == "Other", problem.lower(), int(year) if year.isdigit() else 0, title.lower())


def main():
    rows = public_rows()
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(rows)
    print(f"wrote {len(rows) - 1} papers to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
