# MDM Practical Assignment 02: Performance Evaluation of Search Algorithm Paradigms

**Student Name:** Aditya Iche  
**PRN:** 202401100136  
**Branch:** Computer Engineering (Software Engineering)  
**Division:** B | **Batch:** B2 | **Roll No:** 48  
**Faculty In-Charge:** Mr. Khushal Khairnar  

---

## 📌 Problem Overview
This repository implements, profiles, and benchmarks four fundamental paradigms of artificial intelligence problem-solving through search:

1. **Uninformed (Blind) Search**: Breadth-First Search (BFS) and Depth-First Search (DFS) evaluated on state-space graph navigation.
2. **Informed (Heuristic) Search**: A* Search and Greedy Best-First Search (GBFS) utilizing Manhattan Distance heuristic on the 8-Puzzle domain.
3. **Local Search & Optimization**: Steepest-Ascent Hill Climbing (with Random Restarts) and Simulated Annealing evaluated on the N-Queens (8-Queens) constraint optimization landscape.
4. **Constraint Satisfaction Problems (CSP)**: Backtracking Search integrated with Minimum Remaining Values (MRV) heuristic, Degree heuristic, and AC-3 constraint propagation evaluated on Australia Map 3-Coloring.

---

## 📊 Benchmark Empirical Results

| Paradigm | Algorithm | Test Domain | Solution Cost / Depth | Nodes Expanded / Iterations | Runtime (ms) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Uninformed** | **BFS** | Graph Navigation | Path Cost = `11` | `9` Nodes | `0.025 ms` | **Pass (Optimal)** |
| **Uninformed** | **DFS** | Graph Navigation | Path Cost = `20` | `9` Nodes | `0.019 ms` | **Pass (Suboptimal)** |
| **Informed** | **A* Search** | 8-Puzzle | Path Depth = `2` | `3` Nodes | `0.067 ms` | **Pass (Optimal)** |
| **Informed** | **GBFS** | 8-Puzzle | Path Depth = `2` | `3` Nodes | `0.046 ms` | **Pass (Greedy)** |
| **Local Search**| **Hill Climbing**| 8-Queens | Conflicts = `0` | `4` Restarts | `16.413 ms` | **Pass** |
| **Local Search**| **Simulated Annealing**| 8-Queens | Conflicts = `1` | `571` Iterations | `9.448 ms` | **Pass** |
| **CSP** | **Backtracking + MRV**| Map Coloring | Valid Color Map | `0` Backtracks | `0.045 ms` | **Pass (Consistent)**|

---

## 🛠️ Installation & Execution

```bash
# Clone repository
git clone https://github.com/aniche59/MDM-AIML-02.git
cd MDM-AIML-02

# Install dependencies
pip install -r requirements.txt

# Run search benchmark script
python search_algorithms_benchmark.py
```

---

## 🌐 Ethical, Societal & Sustainability Impact
- **Resource Allocation Efficiency**: Heuristic-guided search ($A^*$) drastically reduces node expansions, directly minimizing CPU energy expenditure in large-scale logistics routing.
- **Algorithmic Bias in Search Heuristics**: Biased heuristic design can inadvertently restrict search space exploration, impacting fair decision-making in automated planning systems.
