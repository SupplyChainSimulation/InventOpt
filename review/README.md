# Literature review artifacts

This folder contains the data of our review of simulation studies of supply chains, part of our manuscript in preparation for the *Journal of Simulation* (JoS). In the manuscript, we review the applications of simulation modeling in supply chains and the commercial and open-source tools for supply chain simulation. Most of the data here belong to the review of applications, which addresses three questions:

- In which application domains is supply chain simulation modeling reported?
- Across these domains, which supply chain problems are considered, and which model components, parameters, decision variables, and performance metrics are modeled?
- Which simulation tools, libraries, or frameworks do the authors use?

We review 167 studies published between 2019 and 30 September 2026 in five venues of the simulation modeling domain: 115 from the Winter Simulation Conference (WSC), 27 from the *Journal of Simulation* (JoS), 13 from *Simulation Modelling Practice and Theory* (SIMPAT), 11 from *SIMULATION: Transactions of the Society for Modeling and Simulation International* (SIMULATION), and one from *ACM Transactions on Modeling and Computer Simulation* (TOMACS). A study is included when it models a supply chain, or a single facility in its supply chain role, simulates the system over time or under uncertainty, uses the simulation as a primary instrument of the analysis, and specifies the model components, the policy rules, and an experiment that is run.

## Contents

| Artifact | Contents |
| --- | --- |
| `Reviewed papers categorization.csv` / `.pdf` | 167 studies, 18 columns |
| `codebook.md` | The definition of every column of the categorization and the rules applied in filling it, including the inclusion criteria |
| `Node attributes and performance measures.csv` / `.pdf` | 40 attributes, 19 performance measures |
| `Edge attributes and performance measures.csv` / `.pdf` | 12 attributes, 4 performance measures |
| `Graph attributes and performance measures.csv` / `.pdf` | 6 attributes, 15 performance measures |
| `construct_counts.csv` | Number of studies that record each attribute and performance measure, overall and per problem cluster |
| `counts/` | Study counts behind the manuscript's tables and figures |
| `tools/tool_comparison_evidence.csv` | The evidence for every cell of the manuscript's tool comparison (Table 4) |

The CSV files are for reuse and the PDF files for reading. `generate_review_pdf.py` in the repository root prints the categorization CSV to the PDF.

In the manuscript, we call an edge a link, an attribute a parameter, and a performance measure a performance metric.

## Reviewed papers categorization

Each row is one study. The columns record the problem the authors address, the supply chain aspects they model, the methods and tools they use, and how they report the model.

### Column definitions

| Column | Records |
| --- | --- |
| `Sr` | Serial number of the study, from 1 to 167 |
| `Supply chain problem` | Class of supply chain problem addressed, from the vocabulary below |
| `Application domain` | Industry or sector of the modeled supply chain, from the vocabulary below |
| `Title` | Title of the publication |
| `Year` | Year of publication. Journal papers take the year of their volume |
| `Venue` | Conference or journal in which the paper appeared |
| `Specific aspect / SC aspect` | The supply chain aspect analyzed or optimized, beginning `Analysis:`, `Optimization:`, `Analysis and optimization:`, or `Analysis and prediction:` |
| `Tools used to build the model` | Simulation software, library, or programming language used by the authors, as they report it, with versions and secondary tools in brackets |
| `Simulation method used` | Simulation method applied, from the vocabulary below |
| `Optimization/prediction method used` | Optimization, prediction, or analysis method coupled with the simulation, or a scenario comparison when the simulation is used alone, in free text |
| `Comments` | Summary of the system modeled, how the model is built, and the main finding |
| `Any attributes` | The parameters and decision variables of the model, then, after `performance:`, its performance metrics, in free text. A parameter is recorded under the name of the matching row of the attribute tables where there is one |
| `Verification reported` | `yes` if the paper names at least one check that the model is implemented and behaves as intended, such as tracing, extreme-condition tests, or a comparison with an analytical result or another model. A bare claim that the model was verified is `no`, and so is a comparison of outputs with the real supply chain (validation, not recorded). A `no` means that the paper does not clearly report a check, although the authors may have made one |
| `Parameter values given` | `yes` if the paper reports numerical values, or distributions with their parameters, for at least some inputs of the model. Values given only for the experimental settings (horizon, replications, factor levels) are `no` |
| `Replications and run length given` | `yes` if the paper states both the number of replications and the simulated horizon. A model stated to be deterministic counts as one replication |
| `Model or code shared` | `yes` if the paper links to the model file or code, or to a repository or supplement that holds them. Input data alone, and "available on request", are `no` |
| `Network type` | `Real` for a specific existing supply chain defined by a named company, region, or case data (including published data sets of real chains), `Generic` for stylized and benchmark networks |
| `Number of nodes` | Size of the largest network simulated, in bands: `1`, `2 to 10`, `11 to 50`, `more than 50`, or `NR` (not reported). A node is a location that holds, transforms, or ships goods, and a demand point counts when it is modeled as a fixed location |

A study that spans two classes carries both values in the cell, separated by a semicolon, with the main one first. `Other` and `Not mentioned` are never combined with another value.

### Category vocabularies

**Supply chain problem:** Demand Forecasting; Energy and Carbon Cost Modeling and Optimization; Inventory Analysis and Optimization; Logistics Optimization and Route Planning; Planning, production planning; Resilience Modeling, Risk Estimation and Mitigation; Supply Chain Design; Warehouse Operations Optimization; Other. A second problem is given only for a stated objective or decision, and energy and carbon only when energy or emissions is an objective.

**Application domain:** Agriculture and Food; Healthcare and medical supplies (blood, personal protective equipment, hospital supplies, medical devices); Humanitarian and Emergency; Industrial and Manufacturing; Information and Communication Technology (ICT); Pharmaceuticals (drugs, including cell and gene therapies and biomanufacturing); Other (a named domain outside these, such as warehousing, ports and freight, retail of non-food goods, construction, mining, or energy and fuel supply); Not mentioned (no domain named, as in a generic or stylized supply chain).

**Simulation method used:** DES (discrete event simulation); ABS (agent-based simulation); SD (system dynamics); Monte Carlo; Other. A study that combines methods in one model, or in coupled models, carries a hybrid value such as `Hybrid DES + ABS` or `Hybrid DES + ABS + SD`. The method is coded only when the authors name it, so Other covers the studies that name no method, for example a time-stepped loop, a trace-driven replay, or disruption propagation over a graph.

**Tools used to build the model:** recorded as the authors report them. For counting, each study is assigned the package or library its simulation model is built in (a named simulation library such as SimPy, Mesa, or pydsol takes precedence over the language), secondary tools such as optimizers are dropped, and names of one tool are merged (for example Vensim PLE as Vensim). The tools counted, with their groups, are listed in `counts/review_tools_counts.csv`.

### Counts

The files in `counts/` are generated from the categorization CSV by `generate_review_counts.py` in the repository root, except `review_problem_by_metric.csv` and `review_problem_by_parameter.csv` (see below).

| File | Contents |
| --- | --- |
| `review_problems_counts.csv` | Studies per problem, in the CSV vocabulary and in the clusters of the manuscript's Table 3 |
| `review_domains_counts.csv` | Studies per domain, in the CSV vocabulary and in the rows of the manuscript's Table 2 |
| `review_methods_counts.csv` | Studies per simulation method |
| `review_tools_counts.csv` | Studies per tool, with the tool's group and whether it is built for supply chains |
| `review_reporting_counts.csv` | Studies per value of `Network type`, `Number of nodes`, and the four reporting columns |
| `review_problem_by_method.csv` | Studies per cluster and simulation method, with the hybrid values in one column |
| `review_problem_by_tool.csv` | Studies per cluster and tool, for the tools used in six or more studies |
| `review_problem_by_metric.csv` | Studies per cluster and performance metric, for the metrics recorded by 12 or more studies |
| `review_problem_by_parameter.csv` | Studies per cluster and parameter, for 17 parameters that we selected from those modeled across the clusters and those modeled mainly in one cluster |

In the manuscript, we group the problems into eight clusters, with Planning, production planning and Supply Chain Design together as planning and design. Because a study can carry two problems or two domains, the problem and domain counts add up to more than the number of studies, and a study with two problems counts in two clusters.

## Attribute and performance measure tables

Three files list the parameters that the reviewed studies model at the node, edge (link), and network (graph) level, together with the performance metrics computed from a run.

Each file contains two blocks. The first lists attributes, meaning the inputs that describe the network, such as the inventory capacity and reorder level of a node, or the lead time and transportation cost of an edge. The second lists performance measures, meaning the outputs evaluated from a simulation run, such as the customer service level of a node or the net profit of the supply chain. Each entry gives a serial number, the name of the attribute or measure, and a description. A node attribute that applies only to some kinds of node, such as production capacity, says so at the end of its description.

`construct_counts.csv` gives, for each row, the number of studies that record it (`Studies`) and the number in each of the eight clusters (`C1` to `C8`). `Clusters` names the clusters in which three or more studies record the row, and `In table` marks the 80 rows recorded by four or more studies, which we print in Appendix A of the manuscript. The counts come from mapping the `Any attributes` cell of each study to the rows of the three tables. `review_problem_by_metric.csv` and `review_problem_by_parameter.csv` are taken from the same mapping.

## Tool comparison

`tools/tool_comparison_evidence.csv` holds one row per tool and criterion of the manuscript's Table 4, which compares 15 commercial platforms and open-source frameworks and libraries. The columns give the tool, its group, the criterion, the value printed in the table, the evidence for the value, the source it was read from, and the access date (27 October 2026). The values of each criterion are defined in the manuscript's Appendix B.
