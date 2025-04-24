# CPTS440-Group6-Project

This repository contains the final group project for CPTS440/540: an AI-driven implementation of the game **Quoridor**, including an interactive game app and multiple agent testing frameworks.

## Project Structure
```text
CPTS440-Group6-Project/
├── GameApp/                            # Main game logic and interactive UI
│   ├── .vs/
│   ├── .gitignore
│   ├── GameManager.py
│   ├── README.md
│   ├── aStarAgent.py
│   ├── aStarAgentTesting.py
│   ├── astarpathfinding.py
│   ├── astartesting.py
│   ├── boardState.py
│   ├── interactive_ui_pygame.py
│   ├── moveLogic.py
│   ├── player.py
│   ├── space.py
│   └── wall.py
│
├── Tests/                              # All agent testing scripts and results
│   ├── boardState.py                   # Legacy board implementation
│   ├── baselineAgent/                  # Legacy agent testing scripts
│   │   ├── boardState.py
│   │   ├── randomMove.py
│   │   ├── shortMove.py
│   │   ├── shortMoveWallPlace.py
│   │   └── testWallPlace.py
│   ├── CaseTestsandBFSAgent/
│   │   ├── .vs/
│   │   ├── .gitignore
│   │   ├── GameManager.py
│   │   ├── README.md
│   │   ├── aStarAgent.py
│   │   ├── aStarAgentTesting.py
│   │   ├── astarpathfinding.py
│   │   ├── astartesting.py
│   │   ├── bfsAgent.py
│   │   ├── boardState.py
│   │   ├── caseTest.py
│   │   ├── moveLogic.py
│   │   ├── player.py
│   │   ├── shortTest.json
│   │   ├── space.py
│   │   ├── randomAStarTesting.py
│   │   └── testAgent.py
│   └── RandomMoveAgent/
│       ├── .gitignore
│       ├── GameManager.py
│       ├── README.md
│       ├── aStarAgent.py
│       ├── aStarAgentTesting.py
│       ├── astarpathfinding.py
│       ├── astartesting.py
│       ├── boardState.py
│       ├── moveLogic.py
│       ├── player.py
│       ├── randomMove.py
│       ├── shortRandomTest.json
│       ├── space.py
│       └── testRandomAgent.py
│
├── .gitignore
└── README.md
```

## Requirements

Before running the project, install the required Python libraries:

```bash
pip install pygame numpy
```
## GameApp

The `GameApp/` folder includes a playable version of Quoridor. It supports:
- Human vs AI
- Visual wall placements and movements
- A* agent-controlled gameplay

## Agent Testing

The `Tests/` folder contains three types of agent testing:
- **CaseTestsandBFSAgent**: Structured evaluation of A* performance, including 4 case tests and tests vs a BFS agent.
- **RandomMoveAgent**: Simulation of A* performance against randomly moving opponents.
- **baselineAgent**: Legacy agent testing scripts for historical comparison (not used in current evaluations).

## Notes

- The `boardState.py` inside `Tests/` is an older version and may differ from the one in `GameApp/`.
- Output JSON files include win/loss results, move paths, and timing.

## How to Run

To run the game:
```bash
cd GameApp
python interactive_ui_pygame.py
```

To run A* vs BFS tests:
```bash
cd Tests/CaseTestsandBFSAgent
python testAgent.py
```

To run A* vs Random tests:
```bash
cd Tests/RandomMoveAgent
python testRandomAgent.py
```
