# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Research code accompanying the SIMULTECH 2023 paper *"An Open Tool-set for Simulation, Design-space Exploration and Optimization of Supply Chains and Inventory Problems"* (Lone, Lekshmi P, Karanjkar). It builds a discrete-event simulation of a 5-node supply chain (2 retailers, 2 distributors, 1 manufacturer) and finds inventory parameters that maximize net profit, using metamodel-based simulation optimization (GPR and Neural-Network surrogates with local optimizers).

This is exploratory/experimental scientific code, not a packaged library: there is no build system, no test suite, no linter config, and no `requirements.txt` at the repo root. Many scripts have **hardcoded paths, parameters, and output filenames** and expect to be run from inside their own module directory.

## The pipeline (run modules in order)

The four core modules are meant to be followed sequentially; each consumes the previous module's output:

1. **`model/`** — Defines the supply-chain simulation. Walkthrough is in `model/notebook/supply_chain_net_model.ipynb`.
2. **`cost_acc_tradeoff/`** — Estimates a reasonable compute budget (choice of `N` = number of sims, `L` = simulation length in days) for an acceptable relative standard error.
3. **`design_experiments/`** — Runs the model exhaustively over design points listed in `data/in_params.csv`, producing `output/supplychain_datav2_<L>_<N>.csv`.
4. **`metamodel_based_optimization/`** — Fits GPR/NN metamodels on the exhaustive-eval data (25/50/75% train splits) and runs local optimizers on the surrogate.

`visualization/` is a separate Streamlit app (a vendored copy of "DATAvis") for viewing the multidimensional sample data as 3D slices.

## The simulation core: `SupplyChainModelv2.py`

This file is **duplicated** across modules (`model/notebook/src/`, `design_experiments/src/`, `cost_acc_tradeoff/src/`, `metamodel_based_optimization/notebook/src/`). Each module imports its local copy via `sys.path.append("src")`. If you change simulation behavior, you likely need to update every copy. `SupplyChainModel.py` (no `v2`) is the older version — `v2` changes retailer sourcing to "buy from cheapest available distributor, else next cheapest."

Architecture (SimPy-based):
- **`SC_node`** — one class models every actor (customer, retailer, distributor, manufacturer); behavior is determined by which constructor args are set. A node with `S` (capacity) gets a `MonitoredContainer` inventory and an `inventory_monitor` process; a node without inventory is a customer or the manufacturer. Inventory policy is `(S, s)`: when end-of-day level falls below threshold `s`, order back up to `S`.
- **`MonitoredContainer`** — subclasses `simpy.Container` and overrides `_do_put`/`_do_get` to track a time-averaged inventory level (`avg_level`).
- **`arrivals(env, lam, p, retailers)`** — Poisson customer arrivals; each customer buys 1–10 units from a retailer chosen by probability `p`.
- **`single_sim_run(lam, D_list, R_list, ...)`** — builds the network from distributor/retailer dicts and runs one simulation, returning aggregate stats plus per-node stats. Key output is `avg_net_profit` (profit − holding cost − delivery cost, per day), the optimization objective.

Distributors/retailers are passed as plain dicts with keys `name, S, s, H, C` (per-supplier delivery costs), `D` (per-supplier delivery times). See the dict definitions at the top of the `design_experiments`/`cost_acc_tradeoff` scripts for the canonical example values.

The 8 design variables optimized throughout are: `S_R1, s_R1, S_R2, s_R2, S_D1, s_D1, S_D2, s_D2`.

## Running things

There is no entry point or runner — execute scripts directly with Python, **from within their module directory** (relative paths like `data/...`, `output/...`, `src` depend on it):

```powershell
cd design_experiments
python exhaustive_eval_supplychainmodelv2.py            # sequential
python exhaustive_eval_supplychainmodelv2_rawdatasave.py # parallel (multiprocessing.Pool(processes=64))

cd cost_acc_tradeoff
python exe_time_rse_analysis.py     # appends to data/exe_time_rse_ana.csv

cd metamodel_based_optimization
python fit_meta_optimize_calculate_mse.py   # see fit_with_x_perc(...) call at bottom

cd visualization/DATAvis-master
streamlit run Data_Visualizer_ori.py
```

Dependencies (no root manifest; install manually): `simpy`, `numpy`, `pandas`, `scikit-learn`, `scipy`. The Streamlit app additionally needs `streamlit` and `plotly` (pinned versions in `visualization/DATAvis-master/requirements.txt`).

## Conventions and gotchas

- **Output files are appended to, not overwritten.** Scripts use `open(..., 'a')`; delete stale CSVs before a fresh run or rows will accumulate.
- **Experiment configuration is by editing code**, not CLI args. Parameters (`num_days`, `num_sims`, design points, metamodel choice, optimizer) and output filenames are hardcoded near the bottom of each script — read the whole file before running.
- In `fit_meta_optimize_calculate_mse.py`, the metamodel and iteration tracker are passed through module-level globals (`metamodel_regr`, `x_fx_arr`) because the optimizer's objective function needs them. The parallel `multiprocessing.Pool` driver at the bottom is commented out in favor of a single direct call.
- The parallel exhaustive-eval script hardcodes 64 processes — adjust for the host before running.
- The `review/` directory holds paper-review artifacts (attribute/performance-measure tables as CSV+PDF), not code.
