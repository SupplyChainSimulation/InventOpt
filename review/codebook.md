# Codebook

This codebook defines the columns of `Reviewed papers categorization.csv` and the rules applied in filling them. It covers our review of supply chain (SC) simulation studies, part of the manuscript described in `README.md`.

## 1. Unit, source and inclusion

- **Unit.** One row per included study. When one study is reported more than once, the fullest report is kept and the shorter, earlier one is excluded. Two reports of one model with different experiments are both kept.
- **Venues.** A study is included only when it appeared in one of the five venues we review: Simulation Modelling Practice and Theory (SIMPAT), Journal of Simulation (JoS), Simulation: Transactions of the Society for Modeling and Simulation International (SIMULATION), Winter Simulation Conference (WSC), and ACM Transactions on Modeling and Computer Simulation (TOMACS).
- **Source.** The full text. The classification fields come from the whole paper, and the reporting fields (Section 5) from the model, experiment and results sections and any appendix or supplement the paper points to. Nothing is inferred from other papers by the same authors, except the named check of a simulation tool under `Verification reported`.
- **Coding and cross-verification.** The first author coded every study, and we cross-verified all the codes using a large language model (Claude Sonnet 5.5, Opus 5.5).
- **Paraphrase.** Free-text fields are written in our own words and are not copied from the paper beyond a short term or a parameter name.

### 1.1 Inclusion decision

We include a study when it meets the four criteria of our review methodology in the manuscript, restated below and applied in order. We assess whether a study meets each criterion from the full text of the paper.

1. **Criterion 1: Subject.** All three must hold.
   - (a) *Goods.* Physical goods, or orders for goods, are a state of the model. Status only, information, money only, labor-hours, people, tasks and energy do not count.
   - (b) *Parties.* At least two parties exchange the goods. A source or sink counts as a party when the model states its own rule or delay, such as a supplier lead time or a customer order process. A model that states no arrival or order process fails.
   - (c) *Decision on the goods.* At least one varied factor or compared policy acts on the goods or their network: ordering, replenishment, sourcing, allocation, storage location, shipment, transport mode or route, pricing of the goods, network structure, or the disruption of a party or link. One such factor is enough. In one plant, the safety stock, reorder point, lot size or planned lead time of stock that serves the customer counts as replenishment, and so does a comparison of production control systems that set those stocks, while buffers of work in process between the stations of one line do not. Factors that only set the site's own resources (machines, staff, internal vehicles, layout, equipment, sequencing or batching of internal tasks) fail. So do factors that only describe the incoming goods, such as a product or container mix. A vehicle mix passes as a transport mode choice.
2. **Criterion 2: Method.** Discrete event simulation (DES), agent-based simulation (ABS), system dynamics (SD), Monte Carlo, trace-driven or time-stepped simulation, alone or combined. Sampling scenarios only as input to an optimizer (sample average approximation, scenario trees) is not simulation.
3. **Criterion 3: Role.** The paper's SC results are computed by the simulation, whatever the problem type. Two kinds of study are excluded. The first is a simulation that only reproduces an analytically solved model. The second is a study whose reported results are all about a method (forecasting, pricing, calibration, machine learning or modeling), wherever its model is defined. The stochastic evaluation of optimized solutions is kept for every problem type. A study whose subject is an SC performance metric is kept when the metric is computed on a chain whose SC factors are varied.
4. **Criterion 4: Reporting.** Every paper, short or long, specifies the components, the policy rules and a defined experiment that is run. Input values and numerical results are not required. Runs that only demonstrate features of a model, with no output, metric or comparison, fail.

## 2. Identification fields

| Column | Records |
|---|---|
| `Sr` | Serial number of the study, from 1 to 167 |
| `Title` | Title as published |
| `Year` | Year of publication. Journal papers take the year of their volume |
| `Venue` | The full name with its abbreviation, for example `Winter Simulation Conference (WSC)` or `Journal of Simulation (JoS)` |

## 3. Classification fields

A cell with two values separates them with a semicolon and lists the main value first. `Other` and `Not mentioned` are never combined with another value.

### 3.1 Supply chain problem

- A second value is given only for a stated objective or decision.
- A row has at most two values.
- Energy and carbon is given only when energy or emissions is an objective.

| Value | Definition |
|---|---|
| Inventory Analysis and Optimization | The main question concerns stock at one or more nodes: replenishment policies and their parameters, safety stock, perishability and shelf life, or inventory cost and service trade-offs |
| Resilience Modeling, Risk Estimation and Mitigation | Disruptions to supply, capacity, transport or demand, how they propagate, how risk is measured, and how it is mitigated or recovered from (backup sourcing, buffers, recovery policies) |
| Logistics Optimization and Route Planning | Movement of goods between nodes: routing, fleet sizing, mode choice, shipment scheduling, and the flow of goods through port and freight terminals |
| Planning, production planning | Production, capacity and replenishment planning of one or more SC parties, including collaborative planning and planning under forecast updates |
| Supply Chain Design | Decisions on the structure of the network: facility location, number of echelons, sourcing structure and capacity configuration |
| Warehouse Operations Optimization | Decisions about the goods held in or passing through a warehouse or distribution center in its SC role, such as storage assignment, slotting, replenishment, and shipping |
| Energy and Carbon Cost Modeling and Optimization | Energy use, carbon cost or emissions as an objective or decision |
| Demand Forecasting | Forecasting methods or forecast behavior and their effect on the SC |
| Other | None of the above |

For counting, in the manuscript we group Planning, production planning and Supply Chain Design as one cluster, planning and design.

### 3.2 Application domain

| Value | Definition |
|---|---|
| Agriculture and Food | Farm products, food processing and food distribution, including relief food (which also takes Humanitarian and Emergency) |
| Pharmaceuticals | Drugs, including cell and gene therapies and biomanufacturing |
| Healthcare and medical supplies | Everything else in healthcare: blood, personal protective equipment, hospital supplies and medical devices |
| Humanitarian and Emergency | Disaster relief and emergency response |
| Industrial and Manufacturing | Manufacture of goods (automotive, aerospace, chemicals, machinery, consumer goods) and their supply networks |
| Information and Communication Technology (ICT) | Electronics and ICT products, such as semiconductors |
| Other | A domain is named but lies outside the six above, such as warehousing, ports and freight, retail of non-food goods, construction, mining, or energy and fuel supply |
| Not mentioned | No domain is named, as in a generic or stylized SC |

A study can take two domains. Electronics made for another industry take ICT and that industry's value. When a domain is unclear, it follows the coding of an included study of a similar product.

### 3.3 Simulation method used

The method the authors name is coded. If the authors name none, the value is `Other`. A hybrid value is given when the paper names two or more methods combined in one model, or in models coupled in one framework. An optimization method coupled with the simulation is not a simulation method and is recorded in `Optimization/prediction method used`.

| Value | Definition |
|---|---|
| DES | The state changes at discrete event times: entities, queues and resources |
| ABS | Autonomous agents with their own decision rules interact |
| SD | Stocks, flows and feedback loops, solved in continuous or small discrete time |
| Monte Carlo | Repeated random sampling of a static or period-by-period model without event scheduling |
| Hybrid A + B (+ C) | Two or more of the above combined in one model, in the order DES, ABS, SD, Monte Carlo (for example `Hybrid DES + ABS`) |
| Other | No method is named, for example a time-stepped loop, a trace-driven replay or disruption propagation over a graph |

### 3.4 Tools used to build the model

The tools are recorded as the authors report them, with versions and secondary tools in brackets, for example `Python (SimPy)` or `Simio; MATLAB; CPLEX`. If no tool is named, the value is `Not specified`. For counting, `generate_review_counts.py` assigns each study the package its simulation model is built in:

- A named simulation library (SimPy, Mesa, pydsol) takes precedence over the language.
- Secondary tools such as optimizers and learning libraries are dropped.
- Names of one tool are merged, for example SAS as SAS Simulation Studio.

## 4. Descriptive fields and constructs

| Column | Records |
|---|---|
| `Specific aspect / SC aspect` | One line beginning `Analysis:`, `Optimization:`, `Analysis and optimization:` or `Analysis and prediction:`, stating what the study analyzes or optimizes |
| `Optimization/prediction method used` | The method coupled with the simulation (for example a genetic algorithm, reinforcement learning with the agent named, a mixed-integer program as benchmark), or `Simulation-based scenario comparison` when the simulation is used alone |
| `Comments` | A summary in our own words of the system modeled, how the model is built and the main finding |
| `Any attributes` | The constructs of the model, in the form `<parameters and decision variables>; performance: <performance metrics>` |

**Constructs.** We record the constructs a general SC simulation model needs to represent: nodes and their types, links, products, demand, policies and their parameters, costs and prices, capacities, lead times, disruptions, and the performance metrics computed from a run. Where a construct is a synonym of a row of the three attribute tables (`Node`, `Edge` and `Graph attributes and performance measures.csv`), it is recorded under the table's name, for example "reorder point" as "Reorder level". Other constructs keep the paper's name. Constructs specific to one model's internals are left out, such as learning hyperparameters, optimizer settings, physical process parameters inside a machine, and computational metrics such as run time.

**Attribute tables.** The node, edge and graph tables list 96 constructs, and in Appendix A of the manuscript we print the rows recorded by four or more included studies. A node row that applies only to some node types ends "(node-specific attribute: <node type>)". `construct_counts.csv` gives the number of studies that record each row.

## 5. Reporting fields

Each field is `yes` or `no`, judged from what the paper reports (Section 1). A `no` means that the item is not clearly reported in the paper, although the authors may have done it.

| Column | `yes` when the paper |
|---|---|
| `Verification reported` | Names at least one check that the model is implemented and behaves as intended. Examples are tracing or animation, debugging or code review, extreme-condition or degenerate tests, conservation checks, unit tests, and comparison with an analytical result, with another model or with published results. A named check of the simulation tool or its components also counts, even when the check is reported in an earlier paper. A bare claim ("the model was verified and validated") is `no`. A comparison of outputs with the real SC is validation and does not count, and validation is not recorded in any field. Comparing the policies or scenarios that the model evaluates is not a check of the model |
| `Parameter values given` | Reports numerical values, or distributions with their parameters, for the inputs of its experiments, in the text, a table, an appendix or a supplement. Values for some but not all of the model's inputs are `yes`. Parameters named without values, values for only an illustrative example, and values given only for the experimental settings (horizon, number of replications or iterations, warm-up and the levels of the factors varied) are `no` |
| `Replications and run length given` | States both the number of replications and the simulated horizon. A deterministic model counts as one replication only if the paper says that the model is deterministic or that its inputs carry no randomness. A warm-up period is not required |
| `Model or code shared` | Gives a link to the model file or code, or to a repository or supplement that contains them. A deposit of input data alone, and "available on request", are `no` |
| `Network type` | Takes `Real` or `Generic`. `Real` means the network models a specific existing SC whose structure is defined by a named company, region or case data. A published data set of real company chains is `Real` even when the companies are not named, and a paper that simulates both is `Real` when at least one experiment runs on a real network. `Generic` covers stylized and benchmark networks, including generated instances and those with realistic parameter values |
| `Number of nodes` | The size of the largest network simulated, in bands: `1`, `2 to 10`, `11 to 50`, `more than 50`, or `NR` (not reported). A node is a location that holds, transforms or ships goods (supplier, plant, warehouse, distribution center, retailer). A demand point counts when the paper models it as a fixed location, such as a customer firm, a store or an aggregated demand area. Individual end consumers, and machines and agents inside a facility, do not count. A single facility is `1` |
