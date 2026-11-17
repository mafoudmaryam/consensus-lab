# Consensus Lab — Blockchain Consensus and Network Delay Simulator

**Author:** Maryam Mafoud  
**Student ID:** 2023521460216  
**Course:** New Software Technology  
**Major:** Software Engineering

## Overview

Consensus Lab is a Python educational research project investigating **how network propagation delay affects competing branches and chain agreement in simplified blockchain simulations**.

The repository contains step-by-step learning scripts, simplified transaction validation and Proof-of-Work demonstrations, simulations of network delays and temporary forks, and reproducible statistical experiments. It uses simulated transactions and does **not** connect to a real cryptocurrency network.

## Research question

**How do network delays affect temporary forks and agreement in a simplified Proof-of-Work blockchain network?**

## Main findings

Five miners were simulated in a fully connected network. For each network delay, the experiment performed **100 independent repetitions** (500 total), using a 1,000-second mining horizon, equal mining rates, an expected network-wide block interval of 10 seconds, and fixed delivery delay. Mining times are exponentially distributed. Pending block messages are delivered after mining ends.

| Network delay (s) | Competing blocks (% of mined blocks) | Stale blocks (% of mined blocks) | Final agreement |
|---|---:|---:|---:|
| 0.1 | 1.723% | 0.861% | 100% |
| 0.5 | 7.167% | 3.619% | 100% |
| 1.0 | 13.643% | 6.917% | 100% |
| 3.0 | 34.911% | 18.329% | 100% |
| 5.0 | 48.723% | 26.514% | 100% |

Results are from `results/multi_node_summary.csv`. As delay increases, the proportion of competing and stale blocks rises in this model.

**Metric definitions:** Competing blocks are mined blocks whose parent has more than one child; stale blocks are mined blocks excluded from the final preferred chain. Both percentages are computed per simulation, then averaged over 100 repetitions. These differ from the two-miner **probability of at least one fork** and should not be compared as the same metric.

All simulations ended in agreement because messages are reliably delivered and nodes follow a deterministic height-based chain choice with a consistent tie-break. This is **not** evidence that real-world networks always agree.

## Reproduce the experiments

Requires Python 3 and Matplotlib for plotting:

```bash
python3 -m pip install matplotlib
python3 fork_rate_repeated.py
python3 final_statistics.py
python3 multi_node_simulator.py
python3 multi_node_experiments.py
```

Generated CSV files and figures are saved under `results/`. The scripts use fixed seeds so rerunning the same version reproduces the same simulated outcomes.

## Key files

| File | Purpose |
|---|---|
| `blockchain.py`, `validated_blockchain.py` | Early blockchain and validation demonstrations |
| `mining.py`, `mining_difficulty.py` | Simplified Proof-of-Work demonstrations |
| `network_delay.py`, `network_fork_v2.py` | Propagation delay and fork examples |
| `fork_rate_experiment.py` | Two-miner fork probability experiment |
| `fork_rate_repeated.py`, `final_statistics.py` | Repeated two-miner estimates and 95% confidence intervals |
| `multi_node_simulator.py` | Single illustrative five-node simulation |
| `multi_node_experiments.py` | 500-run five-node comparison and final chart |
| `results/multi_node_final_graph.png` | Final results visualization |
| `docs/PROJECT_PROPOSAL.md` | Original proposal, retained as historical planning document |

## Model assumptions and limitations

- The main five-node experiment models block discovery and propagation events, **not actual Proof-of-Work hash computation**. Separate scripts demonstrate hash-based mining.
- All five miners have equal mining power and every node connects directly to every other node.
- Block delivery is reliable and has a fixed delay per experiment, with no packet loss or bandwidth limits.
- Nodes choose the chain with the greatest height; equal-height ties use the smaller block ID. This is a simplified approximation of accumulated-work selection, not full Bitcoin consensus.
- All nodes eventually receive all mined blocks; the reported 100% final agreement is therefore dependent on the model assumptions.
- The simulator counts competing and stale blocks, not explicit fork *lifetimes* or time-to-convergence. Measuring those remains future work.
- The project has a command-line simulation and saved charts, **not a Streamlit interactive UI**.

## Status

**Core simulation experiments complete; reporting and final course submission preparation in progress.**

## Author

Maryam Mafoud
