*This project has been created as part of the 42 curriculum by macerver.*

# Fly-in: Autonomous Drone Routing System

## Description
The **Fly-in** project focuses on designing an efficient, automated routing system that navigates a fleet of drones through a complex, interconnected network. The primary goal is to move all drones from a designated starting hub to an end hub in the absolute minimum number of simulation turns. 

The system simulates a dynamic graph where nodes (zones) and edges (connections) have strict capacity limits. Drones must coordinate to avoid collisions, respect movement costs (such as 2-turn delays for restricted zones), and dynamically adjust their paths to prevent deadlocks. The entire engine is built with strict Object-Oriented Programming (OOP) principles in Python 3.10+, ensuring complete type safety and robust error handling.

## Instructions
The project includes a `Makefile` to automate execution, linting, and environment setup. 

**Requirements:**
* Python 3.10 or higher.
* `flake8` and `mypy` for linting and type checking.

**Makefile Commands:**
* `make install`: Installs required dependencies (if using a virtual environment).
* `make lint`: Runs strict type and style checking (`flake8` and `mypy`).
* `make clean`: Removes Python cache files (`__pycache__`, `.mypy_cache`).

**Execution:**
Run the simulation by passing a map file to the main script. You can optionally enable the visualizer using the `--visual` flag.

```bash
# Standard output (grading format)
`make run` or python3 main.py maps/easy/01_linear_path.txt

# Enhanced visual output
`make run_visual` or python3 main.py maps/medium/02_circular_loop.txt --visual
```

## Algorithm Choices and Implementation Strategy
The core architecture strictly adheres to the Single Responsibility Principle, separating the simulation loop, network topology, drone state management, and visualization into distinct classes (`Simulation`, `Network`, `Drone`, `Visualizer`).

* **Dynamic BFS (Optimistic Routing):** The pathfinding relies on a Breadth-First Search (BFS) algorithm modified to handle temporal traffic. By utilizing BFS, the engine achieves an optimal time complexity of O(V + E)(Vertices + Edges) without the CPU overhead of weighted algorithms like Dijkstra. Instead of treating distant occupied zones as impenetrable walls, the BFS strictly checks capacity only for the drone's *immediate next step*. For future steps, the algorithm acts optimistically, assuming current traffic jams will clear by the time the drone arrives. This prevents artificial deadlocks while ensuring physical safety.
* **State Machine & Cooldowns:** Multi-turn movements (e.g., traveling to a `restricted` zone) are handled via a state machine. Drones enter an `IN_TRANSIT` state and receive a cooldown. They physically free up their previous zone immediately, optimizing network throughput, and only occupy their destination once the cooldown expires.
* **Instantaneous Turn Resolution:** To maximize efficiency, drones moving out of a zone immediately free up capacity within the exact same turn, allowing other drones to flow in directly behind them without artificial delays.

## Visual Representation Features
The project features a custom-built 2D visualizer that renders directly in the terminal using ANSI escape codes. 

* **Spatial Matrix Rendering:** The visualizer automatically calculates the map's boundaries, offsets negative coordinates, and scales the grid to render a proportionally accurate 2D map.
* **Transit Interpolation:** Drones traveling across connections that cost multiple turns are visually rendered suspended in the physical midpoint between the two zones. 
* **Dynamic Grouping:** To preserve grid alignment, zones with multiple drones dynamically group the display (e.g., `[ 3D ]`), preventing UI breakage in high-capacity bottlenecks.
* **UX Enhancement:** This visual feedback drastically enhances the user experience by transforming a dense text log into an intuitive, readable dashboard. It allows peers and users to instantly identify traffic bottlenecks, verify capacity compliance visually, and understand the map's topology at a glance.

## Resources
* **Graph Theory & Traversal:** Core concepts of Breadth-First Search (BFS) were adapted from classic algorithmic literature to handle unweighted shortest-path calculations.
* **Python Documentation:** Extensive use of the `collections.deque` module for O(1) queue operations, and PEP 484 for implementing strict static type hints (`mypy`).
* **AI Usage:** Artificial Intelligence was utilized as an interactive technical mentor. It was specifically used to brainstorm OOP architectural patterns to isolate the rendering engine, to debug complex coordinate offsets when rendering negative values in the 2D terminal matrix, and to discuss conceptual approaches for resolving temporal deadlocks in the BFS algorithm ("optimistic routing"). No code was used without thorough peer-level discussion and total understanding of the underlying mechanics.