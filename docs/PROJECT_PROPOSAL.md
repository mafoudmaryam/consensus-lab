# Project Topic Proposal

**Title:** Consensus Lab: An Interactive Blockchain Consensus Simulator  
**Student:** Maryam Mafoud  
**Student ID:** 2023521460216  
**Course:** New Software Technology

## Background

Blockchain networks consist of computers that maintain copies of transaction history. Delays in sharing new blocks can cause temporary disagreements about the latest valid history. A simplified simulation can make these processes easier to understand.

## Objective

Develop an interactive educational simulator to demonstrate blockchain transaction validation, simplified Proof-of-Work mining, block propagation, temporary forks, and eventual chain selection.

## Research question

How do network delays affect temporary forks and agreement in a simplified Proof-of-Work blockchain network?

## Proposed methodology

1. Build a simplified network of nodes, transactions, and blocks in Python.
2. Model mining, block checks, communication delays, and a rule that selects the valid chain with the most accumulated work.
3. Run repeated experiments under different network-delay settings while keeping other conditions controlled.
4. Measure temporary fork frequency, propagation time, and agreement/convergence time.
5. Visualize the outcomes and discuss the model's limitations.

## Optional extension

If the core simulator is completed on time, explore how invalid messages or selected dishonest behaviors affect the network. These are optional and should not replace the main experiments.

## Expected deliverables

- Source code and tests
- Interactive simulation interface
- Experimental data and charts
- Final course report and presentation

**Status:** Proposed topic; awaiting teacher feedback. No experimental findings are claimed yet.
