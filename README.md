# Genetic Algorithm Optimization for EPANET Models

## Overview

This project serves as a proof-of-concept for integrating Genetic Algorithms (GAs) with EPANET-based water distribution models. The primary goal was to gain practical experience with GAs and test their ability to optimize pipe diameters under hydraulic constraints using classic benchmark networks.

The code adapts an open-source GA implementation originally developed in a different Python wrapper and modifies it to work with our current EPANET Python toolkit.

## Repository Purpose

This repository contains:
- The modified GA optimization script
- Sample input files (.inp and .csv)
- Reproduced benchmark tests
- Comparisons with published literature

## Benchmark Problems

The optimization algorithm was tested against three well-known network problems:
- Two-Loop Network
- Hanoi Network
- GoYang Network

Results for the Two-Loop and Hanoi networks were successfully replicated. The GoYang network was underdefined in the original paper, making validation difficult.

## How It Works

### Input Requirements
- An `.inp` file exported from EPANET
- A `.csv` file:
  - Column 1: Available pipe diameters
  - Column 2: Cost per unit length
- Minimum pressure requirement
- Velocity constraints
- Population size and number of generations

### Optimization Workflow

1. **Initialization**
   - Reads network structure from `.inp` file
   - Sets up a population of random diameter configurations
   - Maps diameters to pipe lengths for cost evaluation

2. **Fitness Evaluation**
   - Penalizes configurations that violate pressure or velocity constraints
   - Applies heuristics (e.g., increasing pipe diameters for under-pressure nodes)

3. **Evolution**
   - Selects top-performing configurations
   - Generates new populations through crossover and mutation
   - Introduces random configurations each generation

4. **Termination**
   - Continues for a set number of generations
   - Outputs the most cost-effective configuration satisfying all constraints

## Sample Results

> _See `results/` folder or Table 1 for comparison with SDN-WPN (2022)._

## Future Developments

Planned improvements include:
- Fitness function based on hydraulic error rather than cost
- Domain-specific heuristics informed by engineering experience
- Calibration-focused version of the GA using real-world data
- Modular UI or wrapper for broader usability within the EPA API project

## Acknowledgments

Original code adapted from [this UCL thesis GitHub repository](https://github.com/bowenfan96/epanet-genetic-algorithm).

## Contact

For questions or suggestions, please reach out to **Ace Frazier**.
