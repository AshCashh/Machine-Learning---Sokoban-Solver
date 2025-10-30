# Weighted Sokoban — Project README

Overview
--------
This repository contains an implementation and solver for the weighted Sokoban assignment used in CAB320. It includes:
- a domain model for warehouses (`Warehouse`) and I/O,
- a solver implementation using A* search and heuristics,
- a simple GUI to load and play levels,
- helper scripts and notebooks.

Quick links
-----------
- Core solver implementation: [`mySokobanSolver.py`](mySokobanSolver.py)  
  - Key symbols: [`taboo_cells`](mySokobanSolver.py), [`taboo_cells_map`](mySokobanSolver.py), [`SokobanPuzzle`](mySokobanSolver.py), [`solve_weighted_sokoban`](mySokobanSolver.py), [`check_elem_action_seq`](mySokobanSolver.py)
- Search utilities: [`search.py`](search.py) — use functions like [`astar_graph_search`](search.py)
- Domain model: [`sokoban.py`](sokoban.py) — class [`Warehouse`](sokoban.py)
- GUI app: [`gui_sokoban.py`](gui_sokoban.py)
- Quick sanity tests: [`sanity_check.py`](sanity_check.py)
- Warehouse level files: [`warehouses/`](warehouses/)

How to run
----------
1. Run the GUI
   - From the repo root: `python gui_sokoban.py`
   - Use File -> Open to load files from the [`warehouses/`](warehouses/) folder.

2. Run the solver directly (headless)
   - Import and call the solver from Python:
     ```py
     from mySokobanSolver import solve_weighted_sokoban
     from sokoban import Warehouse
     wh = Warehouse()
     wh.load_warehouse("warehouses/warehouse_01.txt")
     actions, cost = solve_weighted_sokoban(wh)
     ```
   - The solver uses [`SokobanPuzzle`](mySokobanSolver.py) together with [`astar_graph_search`](search.py).

3. Run the sanity checks
   - `python sanity_check.py` will run simple tests using the functions in [`mySokobanSolver.py`](mySokobanSolver.py).

Notes on implementation
-----------------------
- Taboo detection: implemented in [`taboo_cells`](mySokobanSolver.py) and [`taboo_cells_map`](mySokobanSolver.py).
- Weighted costs: `SokobanPuzzle.path_cost` accounts for box weights.
- Heuristic: A Hungarian-assignment based heuristic is implemented as `SokobanPuzzle.h` in [`mySokobanSolver.py`](mySokobanSolver.py).
- Search compatibility: `SokobanPuzzle` subclasses [`search.Problem`](search.py) and is compatible with functions like [`astar_graph_search`](search.py).

Files to inspect first
----------------------
- [`mySokobanSolver.ipynb`](mySokobanSolver.ipynb) — notebook walkthrough and development notes.
- [`mySokobanSolver.py`](mySokobanSolver.py) — main implementation used by scripts.
- [`search.py`](search.py) — generic search utilities (A* / BFS / etc.).
- [`sokoban.py`](sokoban.py) — warehouse parsing and representation.
- [`gui_sokoban.py`](gui_sokoban.py) — Tkinter GUI.

Authors / Team
--------------
See `my_team()` in [`mySokobanSolver.ipynb`](mySokobanSolver.ipynb) / [`mySokobanSolver.py`](mySokobanSolver.py).

License / Notes
---------------
This code is part of an assignment. Do not change public function/class interfaces used by the grader (e.g. names and signatures in `mySokobanSolver.py`).