# Literature review artifacts

This folder contains artifacts from two literature reviews that are part of a manuscript in preparation for the *International Journal of Production Research* (IJPR). The first reviews the applications of simulation modeling in supply chains. The second reviews existing commercial and open-source frameworks for supply chain simulation. Both reviews were conducted in the context of simulation-based optimization in supply chains and address four broad questions:

- Which supply chain domains and problems require simulation-based methods for analysis and optimization?
- Which aspects of a supply chain are modeled?
- Which simulation methods are used to model these aspects?
- Which tools and frameworks are available for building supply chain simulation models?

The reviews draw on 198 papers published between 2019 and September 2026 in the simulation modeling and operations research domains, selected from leading conferences and journals. A paper is included when it models a supply chain or a facility in its supply chain role, simulates the system over time or under uncertainty, uses the simulation as a primary instrument of the analysis, and describes the model in enough detail to record its components, parameters, and performance metrics. 104 papers come from the Winter Simulation Conference (WSC), 49 from IJPR, 26 from the *Journal of Simulation* (JoS), and 17 from *Simulation Modelling Practice and Theory* (SIMPAT). The remaining two are from *ACM Transactions on Modeling and Computer Simulation* (TOMACS) and the International Conference on Management Science and Industrial Engineering (MSIE).

## Contents

Every artifact is provided as a CSV file for reuse and as a PDF file for reading.

| Artifact | Contents |
| --- | --- |
| Reviewed papers categorization | 198 publications, 12 columns |
| Node attributes and performance measures | 33 attributes, 27 performance measures |
| Edge attributes and performance measures | 14 attributes, 7 performance measures |
| Graph attributes and performance measures | 6 attributes, 22 performance measures |

The `counts/` folder holds the paper counts behind the manuscript's tables and figures, by supply chain problem, application domain, simulation method, and tool.

## Reviewed papers categorization

Each row is one publication. The columns record the problem the authors address, the supply chain aspects they model, and the methods and tools they use.

### Column definitions

| Column | Records |
| --- | --- |
| `Sr` | Serial number of the entry |
| `Supply chain problem` | Class of supply chain problem addressed, from the vocabulary below |
| `Application domain` | Industry or sector of the modeled supply chain, from the vocabulary below |
| `Title` | Title of the publication |
| `Year` | Year of publication |
| `Venue` | Conference or journal in which the paper appeared |
| `Specific aspect / SC aspect` | The particular supply chain aspect modeled or analyzed, in free text |
| `Tools used to build the model` | Simulation software, library, or programming language used by the authors, as they report it |
| `Simulation method used` | Simulation paradigm applied, from the vocabulary below |
| `Optimization/prediction method used` | Optimization, prediction, or analysis method applied on the simulation model, in free text |
| `Comments` | Summary of the scope and findings of the paper |
| `Any attributes` | Supply chain attributes and parameters the paper models, in free text |

A paper that spans two classes carries both values in the cell, separated by a semicolon. The main problem is listed first.

### Category vocabularies

**Supply chain problem:** Demand Forecasting; Energy and Carbon Cost Modeling and Optimization; Inventory Analysis and Optimization; Logistics Optimization and Route Planning; Planning, production planning; Resilience Modeling, Risk Estimation and Mitigation; Supply Chain Design; Warehouse Operations Optimization; Other.

**Application domain:** Agriculture and Food; Healthcare and Medical; Humanitarian and Emergency; Industrial and Manufacturing; Information and Communication Technology (ICT); Other/Not mentioned. Other/Not mentioned covers both papers that name no domain and papers whose domain lies outside the other categories, such as warehousing, ports and freight, or retail.

**Simulation method used:** discrete event simulation (DES); agent based simulation (ABS); system dynamics (SD); Monte Carlo; Other. A paper combining paradigms carries a hybrid value, such as `Hybrid DES + ABS` or `Hybrid DES + ABS + SD`. Other covers papers that name no simulation paradigm.

**Tools used to build the model:** recorded as the authors report them. For counting, each paper is assigned the package or library its simulation model is built in (a named simulation library such as SimPy, Mesa, or pydsol takes precedence over the language), and secondary tools such as optimizers are dropped. The tools counted are @RISK; AnyLogic; AnyLogistix; Arena; AutoSched; Excel; FACTS Analyzer; FlexSim; Java; MASON; MATLAB; Mesa; NetLogo; O2DES.Net; Plant Simulation; Process Simulator; ProModel; pydsol; Python; R; Repast; SAS Simulation Studio; SimChain; Simio; SimPy; Simul8; Stella Architect; Vensim; Witness Horizon; Not specified.

### Counts

The files in `counts/` are generated from the categorization CSV by `generate_review_counts.py` in the repository root. Each file lists the categories in the CSV vocabulary and, for problems and domains, also in the grouping used by the manuscript's tables. The manuscript groups Planning, production planning and Supply Chain Design as planning and design. It splits Healthcare and Medical into pharmaceuticals (drugs, including cell and gene therapies) and healthcare and medical supplies (blood, hospital supplies, personal protective equipment). Because a paper can carry two values, the problem and domain counts add up to more than the number of papers.

## Attribute and performance measure tables

Three separate files detail the key and recurring parameters identified across the reviewed supply chain issues, including node-related, edge-related, and network-related parameters, along with their associated performance measures.

Each file contains two blocks. The first block lists attributes, meaning the inputs that describe the network, such as inventory capacity and reorder level at a node, or lead time and transportation cost on an edge. The second block lists performance measures, meaning the outputs evaluated from a simulation run, such as customer service level at a node or supply chain net profit for the network. Each entry gives a serial number, the name of the attribute or measure, and a description. A node attribute that applies only to some kinds of node, such as production capacity, says so at the end of its description.

Nodes and edges carry a parallel set of disruption entries: a probability of failure, a disruption duration, a recovery duration, and a disruption cost. The node table pairs these with a disruption waste measure that records the inventory destroyed by a disruption, and the graph table records the time the network takes to recover.
