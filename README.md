# CPTS440-Group6-Project

This repository contains the final group project for CPTS440/540: an AI-driven implementation of the game **Quoridor**, including an interactive game app and multiple agent testing frameworks.

## 🔧 Project Structure


## 🎮 GameApp

The `GameApp/` folder includes a playable version of Quoridor. It supports:
- Human vs AI
- Visual wall placements and movements
- A* agent-controlled gameplay

## 🧪 Agent Testing

The `Tests/` folder contains three types of agent testing:
- **CaseTestsandBFSAgent**: Structured evaluation of A* performance, including 4 case tests and tests vs a BFS agent.
- **RandomMoveAgent**: Simulation of A* performance against randomly moving opponents.
- **baselineAgent**: Legacy agent testing scripts for historical comparison (not used in current evaluations).

## 📝 Notes

- The `boardState.py` inside `Tests/` is an older version and may differ from the one in `GameApp/`.
- Output JSON files (e.g., `shortTest.json`) include win/loss results, move paths, and timing.

## 💻 How to Run

To run the game:
```bash
cd GameApp
python interactive_ui_pygame.py

To run A* vs BFS tests:
cd Tests/CaseTestsandBFSAgent
python testAgent.py

To run A* vs Random tests:
cd Tests/RandomMoveAgent
python testRandomAgent.py
