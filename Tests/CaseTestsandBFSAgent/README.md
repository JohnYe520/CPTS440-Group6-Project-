# CPTS440-Group6-Project - CaseTest and BFS Agent

This branch is focused on evaluating the performance of the AStarAgent through automated testing.

## Overview

The purpose of this branch is to:
- Run simulations between the `AStarAgent` and a baseline `BFSAgent`.
- Evaluate win/loss outcomes, movement paths, and wall placement behavior.
- Output detailed logs to a JSON file.
- Include specific unit test cases to verify AStarAgent functionality.

## New Files in This Branch

- `bfsAgent.py`: Contains the implementation of the baseline BFSAgent.
- `caseTest.py`: Defines 5 test cases that verify the basic functionality of the AStarAgent.
- `testAgent.py`: Runs 100 simulation games between AStarAgent and BFSAgent.
  - Logs each game's result, movement path, and wall placement to `shortTest.json`.
- `2AStarAgentsTesting.py`: Runs 100 randomized self-play games using two AStarAgents.
  - Each game starts from random positions (excluding goal rows).
  - Logs each game's result, movement path, and wall placement to `2AStarAgentsTesting.json`.
- `shortTest.json`: Stores the simulation results of 100 games against BFS agent.
- `2AStarAgentsTesting.json`: Stores the simulations results of 100 games between 2 A* agents for performancce review.

## How to Use

1. Make sure all dependencies are installed.
2. Run the test simulation:
   for case tests:
   ```bash
   python caseTests.py
   ```
   for tests with BFS Agent:
   ```bash
   python testAgent.py
   ```
   for tests with two A* Agents:
   ```bash
   python randomAStarTesting.py
   ```
