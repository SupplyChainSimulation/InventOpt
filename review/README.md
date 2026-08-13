# Literature review artifacts

This folder contains artifacts from two literature reviews that are part of a manuscript in preparation for the *International Journal of Production Research* (IJPR). The first reviews the applications of simulation modeling in supply chains. The second reviews existing commercial and open-source frameworks for supply chain simulation. Both reviews were conducted in the context of simulation-based optimization in supply chains and address four broad questions:

- Which supply chain domains and problems require simulation-based methods for analysis and optimization?
- Which aspects of a supply chain are modeled?
- Which simulation methods are used to model these aspects?
- Which tools and frameworks are available for building supply chain simulation models?

The reviews draw on over one hundred papers in the simulation modeling and operations research domains, selected from leading conferences and journals. Approximately 60 papers come from the Winter Simulation Conference (WSC), 20 from *Simulation Modelling Practice and Theory* (SIMPAT), 15 from the *Journal of Simulation* (JoS), 12 from IJPR, and 5 from *ACM Transactions on Modeling and Computer Simulation* (TOMACS), with the remainder drawn from other venues.

## Contents

Every artifact is provided as a CSV file for reuse and as a PDF file for reading.

| Artifact | Contents |
| --- | --- |
| Reviewed papers categorization | 118 publications, 10 columns |
| Node attributes and performance measures | 17 attributes, 23 performance measures |
| Edge attributes and performance measures | 8 attributes, 6 performance measures |
| Graph attributes and performance measures | 3 attributes, 20 performance measures |

## Reviewed papers categorization

Each row is one publication. The columns record the problem the authors address, the supply chain aspects they model, and the methods and tools they use.

### Column definitions

| Column | Records |
| --- | --- |
| `Sr` | Serial number of the entry |
| `Supply chain problem` | Class of supply chain problem addressed, from the vocabulary below |
| `Application domain` | Industry or sector of the modeled supply chain, from the vocabulary below |
| `Title` | Title of the publication |
| `Specific aspect / SC aspect` | The particular supply chain aspect modeled or analyzed, in free text |
| `Tools used to build the model` | Simulation software, library, or programming language used by the authors |
| `Simulation method used` | Simulation paradigm applied, from the vocabulary below |
| `Optimization/prediction method used` | Optimization, prediction, or analysis method applied on the simulation model, in free text |
| `Comments` | Summary of the scope and findings of the paper |
| `Any attributes` | Supply chain attributes and parameters the paper models, in free text |

A paper that spans two classes carries both values in the cell, separated by a semicolon.

### Category vocabularies

**Supply chain problem:** Demand Forecasting; Energy and Carbon Cost Modeling and Optimization; Inventory Analysis and Optimization; Logistics Optimization and Route Planning; Planning, production planning; Resilience Modeling, Risk Estimation and Mitigation; Supply Chain Design; Supply Chain Disruptions; Warehouse Operations Optimization; Other.

**Application domain:** Agriculture and Food; Healthcare and Medical; Humanitarian and Emergency; Industrial and Manufacturing; Information and Communication Technology (ICT); Other/Not mentioned.

**Simulation method used:** discrete event simulation (DES); agent based simulation (ABS); system dynamics (SD); Monte Carlo; Other. A paper combining paradigms carries a hybrid value, such as `Hybrid DES + ABS` or `Hybrid DES + ABS + SD`.

**Tools used to build the model:** AnyLogic; AnyLogistix; Arena; AutoSched; FlexSim; Java; MATLAB; NetLogo; PySP and Gurobi; Python; Repast; SAS Simulation Studio; SimChain; SimPy; Simio; Stella Architect; SuperDecisions; Vensim; Not specified.

## Attribute and performance measure tables

Three separate files detail the key and recurring parameters identified across the reviewed supply chain issues, including node-related, edge-related, and network-related parameters, along with their associated performance measures.

Each file contains two blocks. The first block lists attributes, meaning the inputs that describe the network, such as inventory capacity and reorder level at a node, or lead time and transportation cost on an edge. The second block lists performance measures, meaning the outputs evaluated from a simulation run, such as customer service level at a node or supply chain net profit for the network. Each entry gives a serial number, the name of the attribute or measure, and a description.
