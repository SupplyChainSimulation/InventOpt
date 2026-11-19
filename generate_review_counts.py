"""Write the category counts in review/counts/ from review/Reviewed papers categorization.csv.

Files written:
    review_problems_counts.csv     CSV problem vocabulary, then the Table 3 scheme
    review_domains_counts.csv      CSV domain vocabulary, then the Table 2 scheme
    review_methods_counts.csv      simulation method
    review_tools_counts.csv        tool used to build the model, normalized, with its group
    review_reporting_counts.csv    network type, number of nodes and the four yes/no reporting fields
    review_problem_by_method.csv   studies per Table 3 cluster and simulation method (hybrids in one column)
    review_problem_by_tool.csv     studies per Table 3 cluster and tool, for the tools of six or more studies

A paper with several problems or domains counts once in each, so those blocks sum to
more than the number of papers ("Total assignments"), and a paper with two problems
appears in two clusters of the cross-tables. Method and tool give one value per paper.

The cluster by performance metric table (review_problem_by_metric.csv) and
review/construct_counts.csv come from the mapping of the `Any attributes` cells to the
rows of the attribute tables, which is not part of this repository.

Usage (from the repo root):
    python generate_review_counts.py
"""

import csv
import os
import re
from collections import Counter

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_CSV = os.path.join(REPO_DIR, "review", "Reviewed papers categorization.csv")
OUT_DIR = os.path.join(REPO_DIR, "review", "counts")
MIN_TOOL_STUDIES = 6

# Table 3 rows. Planning and supply chain design share a row.
PROBLEM_SCHEME = {
    "Inventory Analysis and Optimization": "Inventory analysis and optimization",
    "Resilience Modeling, Risk Estimation and Mitigation": "Resilience modeling, risk estimation, and mitigation",
    "Logistics Optimization and Route Planning": "Logistics optimization and route planning",
    "Planning, production planning": "Planning and design (analysis, optimization)",
    "Supply Chain Design": "Planning and design (analysis, optimization)",
    "Warehouse Operations Optimization": "Warehouse operations",
    "Energy and Carbon Cost Modeling and Optimization": "Energy and carbon cost modeling and optimization",
    "Demand Forecasting": "Demand forecasting",
    "Other": "Others",
}
CLUSTERS = list(dict.fromkeys(PROBLEM_SCHEME.values()))

# Table 2 rows. The CSV carries Pharmaceuticals and Healthcare and medical supplies as
# separate codes, and Other and Not mentioned as separate codes.
DOMAIN_SCHEME = {
    "Healthcare and medical supplies": "Healthcare and medical supplies",
    "Pharmaceuticals": "Pharmaceuticals",
    "Agriculture and Food": "Agriculture and food",
    "Industrial and Manufacturing": "Manufacturing and industry",
    "Humanitarian and Emergency": "Humanitarian and emergency response",
    "Information and Communication Technology (ICT)": "Electronics and ICT products",
    "Other": "Other",
    "Not mentioned": "Not mentioned",
}

METHODS = ["DES", "ABS", "SD", "Monte Carlo", "Hybrid", "Other"]

# Tool: the package or library the simulation model is built in. Secondary tools (optimizers,
# learning libraries, process simulators feeding parameters) are dropped.
SIM_LIBRARIES = ("SimPy", "Mesa", "pydsol")
TOOL_ALIASES = {"SAS": "SAS Simulation Studio", "Vensim PLE": "Vensim", "AnyLogistix": "anyLogistix",
                "Tecnomatix Plant Simulation": "Plant Simulation",
                "Authors' object-oriented BPSCN simulation library": "BPSCN library"}

# Tool groups: how a reader gets the tool (its availability and kind, not its quality).
# SC-specific marks a tool built to model supply chains (multi-echelon networks), whatever
# its licence.
COMMERCIAL, OPEN, CODE, UNSPEC = ("Commercial simulation software", "Open-source simulation libraries and platforms",
                                  "Programming languages, spreadsheets and in-house code", "Not specified")
TOOL_GROUPS = [COMMERCIAL, OPEN, CODE]
TOOL_GROUP = {
    **dict.fromkeys(["AnyLogic", "Arena", "Vensim", "Plant Simulation", "Simio", "anyLogistix", "SAS Simulation Studio",
                     "AutoSched AP", "Stella Architect", "FlexSim", "Simcad Pro", "ProModel", "FACTS Analyzer",
                     "SIMUL8", "Planimate"], COMMERCIAL),
    **dict.fromkeys(["SimPy", "NetLogo", "Repast", "MASON", "Mesa", "O2DES.Net", "PsychSim", "SLAPStack",
                     "CPN Tools"], OPEN),
    **dict.fromkeys(["Python", "MATLAB", "Java", "Excel", "C++", "R", "VBA", "GAMS", "Microsoft SQL Server",
                     "BPSCN library", "SCOPE", "ESL"], CODE),
    "Not specified": UNSPEC,
}
SC_SPECIFIC = {"anyLogistix", "SCOPE", "BPSCN library"}


def tool_of(value):
    value = value.strip()
    if not value or value.lower().startswith("custom code"):
        return "Not specified"
    for lib in SIM_LIBRARIES:
        if re.search(rf"\b{lib}\b", value) and not value.startswith(("Vensim", "AnyLogic")):
            return lib
    first = re.sub(r"\([^)]*\)", "", value).split(";")[0].strip()
    first = re.sub(r"^Python\s+[\d.]+$", "Python", first)
    first = re.sub(r"^(AnyLogic)\s+(Professional\s+)?[\d.]+.*$", r"\1", first)
    return TOOL_ALIASES.get(first, first)


def method_of(value):
    value = value.strip()
    return "Hybrid" if value.startswith("Hybrid") else value


def split(value):
    return [v.strip() for v in str(value).split(";") if v.strip()]


def load():
    with open(SOURCE_CSV, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows


def tally(values_per_row):
    """Counter of the categories (a row counts once per category)."""
    total = Counter()
    for cats in values_per_row:
        for c in set(cats):
            total[c] += 1
    return total


def block(title, total, n, order=None, total_label="Total assignments"):
    lines = [[title, "", ""], ["Category", "Papers", f"Percent of {n} papers"]]
    for k in order or [k for k, _ in total.most_common()]:
        lines.append([k, total[k], f"{100 * total[k] / n:.1f}"])
    lines.append([total_label, sum(total.values()), f"{100 * sum(total.values()) / n:.1f}"])
    return lines


def write(name, lines):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, name), "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(lines)


def cross_table(rows, columns, value_of):
    """Studies per Table 3 cluster and column; a study counts once in each of its clusters."""
    n = Counter()
    t = Counter()
    for r in rows:
        for c in {PROBLEM_SCHEME[p] for p in split(r["Supply chain problem"])}:
            n[c] += 1
            t[c, value_of(r)] += 1
    return [["Cluster", "Studies"] + columns] + [[c, n[c]] + [t[c, k] for k in columns] for c in CLUSTERS]


def main():
    rows = load()
    n = len(rows)

    prob = [split(r["Supply chain problem"]) for r in rows]
    dom = [split(r["Application domain"]) for r in rows]
    unknown = ({p for ps in prob for p in ps} - set(PROBLEM_SCHEME)) | ({x for ds in dom for x in ds} - set(DOMAIN_SCHEME))
    assert not unknown, unknown
    write("review_problems_counts.csv",
          block("Supply chain problem (sheet vocabulary)", tally(prob), n) + [[""] * 3]
          + block("Supply chain problem (Table 3 scheme)",
                  tally([[PROBLEM_SCHEME[p] for p in ps] for ps in prob]), n))
    write("review_domains_counts.csv",
          block("Application domain (sheet vocabulary)", tally(dom), n) + [[""] * 3]
          + block("Application domain (Table 2 scheme)",
                  tally([[DOMAIN_SCHEME[x] for x in ds] for ds in dom]), n, list(DOMAIN_SCHEME.values())))

    def single(name, col, fn=lambda v: v.strip(), extra=None):
        t = tally([[fn(r[col])] for r in rows])
        lines = [["Category", "Papers", "Percent"] + (extra[0] if extra else [])]
        for k, v in t.most_common():
            lines.append([k, v, f"{100 * v / n:.1f}"] + (extra[1](k) if extra else []))
        lines.append(["TOTAL", n, "100.0"] + ([""] * len(extra[0]) if extra else []))
        write(name, lines)

    single("review_methods_counts.csv", "Simulation method used")
    tool_n = Counter(tool_of(r["Tools used to build the model"]) for r in rows)
    assert set(tool_n) <= set(TOOL_GROUP), set(tool_n) - set(TOOL_GROUP)
    single("review_tools_counts.csv", "Tools used to build the model", tool_of,
           extra=(["Group", "SC-specific"], lambda k: [TOOL_GROUP[k], "yes" if k in SC_SPECIFIC else "no"]))
    lines = []
    for col in ("Network type", "Number of nodes", "Verification reported", "Parameter values given",
                "Replications and run length given", "Model or code shared"):
        lines += block(col, tally([[r[col].strip()] for r in rows]), n, total_label="TOTAL") + [[""] * 3]
    write("review_reporting_counts.csv", lines)

    assert {method_of(r["Simulation method used"]) for r in rows} <= set(METHODS)
    write("review_problem_by_method.csv",
          cross_table(rows, METHODS, lambda r: method_of(r["Simulation method used"])))
    # Tool columns in the order of the tool groups, by number of studies within a group, Not specified last.
    tools = []
    for g in TOOL_GROUPS:
        tools += sorted((k for k, v in tool_n.items() if v >= MIN_TOOL_STUDIES and TOOL_GROUP[k] == g),
                        key=lambda k: (-tool_n[k], k.lower()))
    tools.append(UNSPEC)
    write("review_problem_by_tool.csv",
          cross_table(rows, tools, lambda r: tool_of(r["Tools used to build the model"])))
    print(f"counts for {n} papers written to {OUT_DIR}")


if __name__ == "__main__":
    main()
