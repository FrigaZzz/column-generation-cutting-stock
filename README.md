# Cutting Stock Optimization with Column Generation Heuristics

## Overview

This repository contains an implementation of simple column generation heuristics to solve the Cutting Stock Optimization Problem, which is formulated as a Mixed-Integer Linear Programming (MILP) problem. The implementation is done using the PULP library in Python.

## Problem Description

The Cutting Stock Optimization Problem involves cutting raw materials into smaller pieces to fulfill orders, minimizing waste, and maximizing the utilization of resources. This problem is modeled as a MILP, where decisions involve selecting cutting patterns to meet demand while minimizing the total cost.


## Files

- **cg_stock.ipynb**: Jupyter notebook containing the main implementation of the cutting stock optimization.
- **cg_tests.ipynb**: Jupyter notebook for testing and validating the implementation.
- **data_gen.py**: Python script for generating data for problem instances.
- **init_prob.lp**: File containing the initial LP relaxation of the problem.
- **learning.ipynb**: Jupyter notebook for learning and experimentation.
- **output.csv**: CSV file containing the output of the optimization.
- **prob.lp**: File containing the current LP relaxation of the problem.
- **slaveprob.lp**: File containing the LP relaxation of the slave problem.
- **tesina.pdf**: Documentation or report related to the project.
