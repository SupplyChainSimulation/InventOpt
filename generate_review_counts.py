"""Write the category counts in review/counts/ from review/Reviewed papers categorization.csv.

Four files, in the layout used since August 2026:
    review_problems_counts.csv   CSV problem vocabulary, then the Table 3 scheme
    review_domains_counts.csv    CSV domain vocabulary, then the Table 2 scheme
    review_methods_counts.csv    simulation method
    review_tools_counts.csv      tool used to build the model, normalised

A paper with several problems or domains counts once in each, so those blocks sum to
more than the number of papers ("Total assignments"). Method and tool give one value
per paper.

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

# Table 3 rows. "Supply Chain Disruptions" (one legacy row) folds into resilience, and
# planning and supply chain design share a row.
PROBLEM_SCHEME = {
    "Inventory Analysis and Optimization": "Inventory analysis and optimization",
    "Resilience Modeling, Risk Estimation and Mitigation": "Resilience modeling, risk estimation, and mitigation",
    "Supply Chain Disruptions": "Resilience modeling, risk estimation, and mitigation",
    "Logistics Optimization and Route Planning": "Logistics optimization and route planning",
    "Planning, production planning": "Planning and design (analysis, optimization)",
    "Supply Chain Design": "Planning and design (analysis, optimization)",
    "Warehouse Operations Optimization": "Warehouse operations",
    "Energy and Carbon Cost Modeling and Optimization": "Energy and carbon cost modeling and optimization",
    "Demand Forecasting": "Demand forecasting",
    "Other": "Others",
}

# Table 2 rows. Healthcare and Medical splits into drugs (pharmaceutical products,
# including cell and gene therapies and biomanufacturing) and everything else in
# healthcare (blood, PPE, hospital supply, medical devices).
DOMAIN_SCHEME = {
    "Agriculture and Food": "Agriculture and food",
    "Industrial and Manufacturing": "Manufacturing and industry",
    "Humanitarian and Emergency": "Humanitarian and emergency response",
    "Information and Communication Technology (ICT)": "Electronics and ICT products",
    "Other/Not mentioned": "Other or not specified",
}
HEALTHCARE = "Healthcare and medical supplies"
PHARMA = "Pharmaceuticals"
PHARMA_TITLES = [
    "Improving Simulation Optimization Run Time When Solving for Periodic Review Inventory Policies in a Pharmacy",
    "Effects of Timing of Agents' Reactions in Pharmaceutical Supply Chains under Disruption",
    "Simulation of IT Data Integration to Optimize an Antibiotics Supply Chain with System Dynamics",
    "Assessing Resilience of Medicine Supply Chain Networks to Disruptions",
    "Deep reinforcement learning approach for dynamic capacity planning in decentralised regenerative medicine",
    "A hybrid simulation methodology for identifying and mitigating supply chain disruptions",
    "Designing Scalable Cell Therapy Processes",
    "Simulation-Based Optimization for CAR T-Cell Therapy Logistics",
    "Validating Simulated Agents With Pharmaceutical Supply Chain Game Data",
]

# Tool: the package or library the simulation model is built in. Secondary tools
# (optimisers, learning libraries, process simulators feeding parameters) are dropped.
SIM_LIBRARIES = ("SimPy", "Mesa", "pydsol")
# Names that refer to the same tool are counted under one label.
TOOL_ALIASES = {"SAS": "SAS Simulation Studio"}


def norm(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


PHARMA_KEYS = {norm(t)[:50] for t in PHARMA_TITLES}


def tool_of(value):
    value = value.strip()
    if not value or value.lower().startswith("custom code"):
        return "Not specified"
    for lib in SIM_LIBRARIES:
        if re.search(rf"\b{lib}\b", value) and not value.startswith(("Vensim", "AnyLogic")):
            return lib
    first = re.sub(r"\([^)]*\)", "", value).split(";")[0].strip()
    first = re.sub(r"^Python\s+[\d.]+$", "Python", first)
    return TOOL_ALIASES.get(first, first)


def split(value):
    return [v.strip() for v in value.split(";") if v.strip()]


def table3(rows):
    return [{PROBLEM_SCHEME[p] for p in split(r["Supply chain problem"])} for r in rows]


def table2(rows):
    out = []
    for r in rows:
        cats = set()
        for d in split(r["Application domain"]):
            if d == "Healthcare and Medical":
                cats.add(PHARMA if any(norm(r["Title"]).startswith(k) for k in PHARMA_KEYS) else HEALTHCARE)
            else:
                cats.add(DOMAIN_SCHEME[d])
        out.append(cats)
    return out


def block(title, counts, n, order=None):
    lines = [[title, "", ""], ["Category", "Papers", f"Percent of {n} papers"]]
    keys = order or [k for k, _ in counts.most_common()]
    for k in keys:
        lines.append([k, counts[k], f"{100 * counts[k] / n:.1f}"])
    total = sum(counts.values())
    lines.append(["Total assignments", total, f"{100 * total / n:.1f}"])
    return lines


def single(counts, n):
    lines = [["Category", "Papers", "Percent"]]
    for k, v in counts.most_common():
        lines.append([k, v, f"{100 * v / n:.1f}"])
    lines.append(["TOTAL", n, "100.0"])
    return lines


def write(name, lines):
    with open(os.path.join(OUT_DIR, name), "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(lines)


def main():
    with open(SOURCE_CSV, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    n = len(rows)

    problems = Counter(p for r in rows for p in split(r["Supply chain problem"]))
    scheme3 = Counter(c for cats in table3(rows) for c in cats)
    write("review_problems_counts.csv",
          block("Supply chain problem (CSV vocabulary)", problems, n) + [["", "", ""]]
          + block("Supply chain problem (Table 3 scheme)", scheme3, n))

    domains = Counter(d for r in rows for d in split(r["Application domain"]))
    scheme2 = Counter(c for cats in table2(rows) for c in cats)
    order2 = [HEALTHCARE, PHARMA] + list(DOMAIN_SCHEME.values())
    write("review_domains_counts.csv",
          block("Application domain (CSV vocabulary)", domains, n) + [["", "", ""]]
          + block("Application domain (Table 2 scheme)", scheme2, n, [k for k in order2 if scheme2[k]]))

    write("review_methods_counts.csv", single(Counter(r["Simulation method used"].strip() for r in rows), n))
    write("review_tools_counts.csv", single(Counter(tool_of(r["Tools used to build the model"]) for r in rows), n))
    print(f"wrote counts for {n} papers to {OUT_DIR}")


if __name__ == "__main__":
    main()
