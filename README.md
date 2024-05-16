# InventOpt
### Discrete-event simulation models for inventory networks and a case study

## About

This repository contains simulation models, code and results associated with the following publications:

[**An Open Tool-set for Simulation, Design-space Exploration and Optimization of Supply Chains and Inventory Problems**](https://https://www.scitepress.org/Papers/2023/121333/121333.pdf)

**Authors:** Tushar Lone, Lekshmi P, Neha Karanjkar

*Proceedings of the 13th International Conference on Simulation and Modeling Methodologies, Technologies and Applications*, July 2023, Rome, Italy
**(SIMULTECH 2023)**

## Paper Summary

This study emphasizes the critical importance of optimizing supply chain (SC) networks to enhance profitability and minimize costs. The traditional analytical methods cannot capture supply chains' complex and stochastic nature, such as demand variability and lead times. Simulation-based Optimization (SBO) models the intricate dynamics of SC systems. The paper explores the use of Metamodels alongside SBO to improve efficiency by approximating the input-output relationship of simulation models, focusing on the application of Gaussian Process Regression (GPR) and Neural Network (NN) Metamodels with local optimizers for optimization. 

Download it [here](https://github.com/SupplyChainSimulation/InventOpt/blob/main/doc/InventOpt.pdf).

## Organization of the repository

The repository is structured into four key modules, each containing Python scripts and notebook files to guide users through the Meta-model-based Optimization process for inventory optimization in a Supply Chain network. The modules are as follows:

- **Model**: Constructs the simulation model for an SC network using SimPy.
- **Cost Accuracy Tradeoff**: Estimates the computation budget for running the model.
- **Design Experimentation**: Manages the experiment setup and data collection from the model.
- **Metamodel-based Optimization**: Applies the Metamodel-based optimization approach on the collected data.

These modules are designed to be followed sequentially for a comprehensive understanding of the optimization process.

## Usage

To effectively utilize the repository for inventory optimization in a supply chain network, users are encouraged to progress through the modules in the order listed. The Python project demonstrates how to optimize inventory levels across a five-node supply chain network to maximize overall net profit. Initially, a simulation model is constructed and validated. Subsequent steps involve a comparative study of optimization approaches, sampling design points in the input space to find an approximation of the optimum value, and finally, applying Metamodel-based optimization to achieve close-to-optimal results. For a detailed walkthrough, users should refer to the notebook files within each module, which elucidate the step-by-step meta-model-based optimization process.