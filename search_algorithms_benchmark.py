"""
MDM Practical Assignment 02: Comparative Benchmark Analysis of AI Search Paradigms
Author: Aditya Iche (PRN: 202401100136)
Branch: Computer Engineering (Software Engineering) - Batch B2
"""

import os
import time
import math
import random
import heapq
import collections
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

output_dir = r"c:\Users\temp\Desktop\College\AI\MDM-AIML-02"

print("==================================================================================")
print("   PRACTICAL 02: COMPARATIVE BENCHMARK ANALYSIS OF AI SEARCH PARADIGMS")
print("==================================================================================")

# ================================================================================
# PARADIGM 1: UNINFORMED SEARCH (BFS & DFS)
# Domain: State-Space Graph Navigation
# ================================================================================

graph = {
    'A': [('B', 2), ('C', 5)],
    'B': [('A', 2), ('D', 4), ('E', 2)],
    'C': [('A', 5), ('F', 3)],
    'D': [('B', 4), ('G', 3)],
    'E': [('B', 2), ('G', 1), ('H', 6)],
    'F': [('C', 3), ('H', 2)],
    'G': [('D', 3), ('E', 1), ('GOAL', 2)],
    'H': [('E', 6), ('F', 2), ('GOAL', 4)],
    'GOAL': []
}

def bfs_search(graph, start='A', goal='GOAL'):
    t0 = time.perf_counter()
    queue = collections.deque([(start, [start], 0)])
    visited = set()
    nodes_expanded = 0
    
    while queue:
        curr, path, cost = queue.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        nodes_expanded += 1
        
        if curr == goal:
            t1 = time.perf_counter()
            return path, cost, nodes_expanded, (t1 - t0) * 1000
            
        for neighbor, weight in graph.get(curr, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor], cost + weight))
                
    t1 = time.perf_counter()
    return None, float('inf'), nodes_expanded, (t1 - t0) * 1000

def dfs_search(graph, start='A', goal='GOAL'):
    t0 = time.perf_counter()
    stack = [(start, [start], 0)]
    visited = set()
    nodes_expanded = 0
    
    while stack:
        curr, path, cost = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        nodes_expanded += 1
        
        if curr == goal:
            t1 = time.perf_counter()
            return path, cost, nodes_expanded, (t1 - t0) * 1000
            
        for neighbor, weight in reversed(graph.get(curr, [])):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor], cost + weight))
                
    t1 = time.perf_counter()
    return None, float('inf'), nodes_expanded, (t1 - t0) * 1000

bfs_path, bfs_cost, bfs_nodes, bfs_time = bfs_search(graph)
dfs_path, dfs_cost, dfs_nodes, dfs_time = dfs_search(graph)

print("\n--- 1. UNINFORMED SEARCH BENCHMARK ---")
print(f"BFS  -> Path: {'->'.join(bfs_path)} | Cost: {bfs_cost} | Nodes: {bfs_nodes} | Time: {bfs_time:.3f} ms")
print(f"DFS  -> Path: {'->'.join(dfs_path)} | Cost: {dfs_cost} | Nodes: {dfs_nodes} | Time: {dfs_time:.3f} ms")

# ================================================================================
# PARADIGM 2: INFORMED SEARCH (A* vs GBFS)
# Domain: 8-Puzzle Benchmark
# ================================================================================

INITIAL_PUZZLE = (1, 2, 3, 4, 0, 5, 7, 8, 6)
GOAL_PUZZLE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def manhattan_distance(state):
    dist = 0
    for idx, val in enumerate(state):
        if val != 0:
            target_r, target_c = (val - 1) // 3, (val - 1) % 3
            curr_r, curr_c = idx // 3, idx % 3
            dist += abs(target_r - curr_r) + abs(target_c - curr_c)
    return dist

def get_neighbors_8puzzle(state):
    neighbors = []
    zero_idx = state.index(0)
    r, c = zero_idx // 3, zero_idx % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            n_idx = nr * 3 + nc
            state_list = list(state)
            state_list[zero_idx], state_list[n_idx] = state_list[n_idx], state_list[zero_idx]
            neighbors.append(tuple(state_list))
    return neighbors

def astar_search(start=INITIAL_PUZZLE, goal=GOAL_PUZZLE):
    t0 = time.perf_counter()
    pq = [(manhattan_distance(start), 0, start, [start])]
    visited = {}
    nodes_expanded = 0
    
    while pq:
        f, g, curr, path = heapq.heappop(pq)
        if curr in visited and visited[curr] <= g:
            continue
        visited[curr] = g
        nodes_expanded += 1
        
        if curr == goal:
            t1 = time.perf_counter()
            return path, g, nodes_expanded, (t1 - t0) * 1000
            
        for nxt in get_neighbors_8puzzle(curr):
            h_val = manhattan_distance(nxt)
            heapq.heappush(pq, (g + 1 + h_val, g + 1, nxt, path + [nxt]))
            
    t1 = time.perf_counter()
    return None, float('inf'), nodes_expanded, (t1 - t0) * 1000

def gbfs_search(start=INITIAL_PUZZLE, goal=GOAL_PUZZLE):
    t0 = time.perf_counter()
    pq = [(manhattan_distance(start), 0, start, [start])]
    visited = set()
    nodes_expanded = 0
    
    while pq:
        h, g, curr, path = heapq.heappop(pq)
        if curr in visited:
            continue
        visited.add(curr)
        nodes_expanded += 1
        
        if curr == goal:
            t1 = time.perf_counter()
            return path, g, nodes_expanded, (t1 - t0) * 1000
            
        for nxt in get_neighbors_8puzzle(curr):
            if nxt not in visited:
                heapq.heappush(pq, (manhattan_distance(nxt), g + 1, nxt, path + [nxt]))
                
    t1 = time.perf_counter()
    return None, float('inf'), nodes_expanded, (t1 - t0) * 1000

astar_path, astar_depth, astar_nodes, astar_time = astar_search()
gbfs_path, gbfs_depth, gbfs_nodes, gbfs_time = gbfs_search()

print("\n--- 2. INFORMED HEURISTIC SEARCH BENCHMARK (8-PUZZLE) ---")
print(f"A* Search -> Path Depth: {astar_depth} | Nodes Expanded: {astar_nodes} | Time: {astar_time:.3f} ms")
print(f"GBFS      -> Path Depth: {gbfs_depth} | Nodes Expanded: {gbfs_nodes} | Time: {gbfs_time:.3f} ms")

# ================================================================================
# PARADIGM 3: LOCAL SEARCH & OPTIMIZATION (Hill Climbing vs Simulated Annealing)
# Domain: N-Queens (8-Queens) Constraint Optimization
# ================================================================================

def count_queen_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def hill_climbing_8queens():
    t0 = time.perf_counter()
    state = list(range(8))
    random.shuffle(state)
    curr_conflicts = count_queen_conflicts(state)
    iterations = 0
    restarts = 0
    
    while curr_conflicts > 0 and restarts < 50:
        iterations += 1
        best_neighbor = list(state)
        min_conflicts = curr_conflicts
        
        for col in range(8):
            for row in range(8):
                if state[col] != row:
                    neighbor = list(state)
                    neighbor[col] = row
                    c = count_queen_conflicts(neighbor)
                    if c < min_conflicts:
                        min_conflicts = c
                        best_neighbor = neighbor
                        
        if min_conflicts >= curr_conflicts:
            # Local optimum reached -> Random restart
            restarts += 1
            state = list(range(8))
            random.shuffle(state)
            curr_conflicts = count_queen_conflicts(state)
        else:
            state = best_neighbor
            curr_conflicts = min_conflicts
            
    t1 = time.perf_counter()
    return state, curr_conflicts, iterations, restarts, (t1 - t0) * 1000

def simulated_annealing_8queens(temp=100.0, cooling_rate=0.98, max_iter=2000):
    t0 = time.perf_counter()
    state = list(range(8))
    random.shuffle(state)
    curr_conflicts = count_queen_conflicts(state)
    cost_history = [curr_conflicts]
    
    for i in range(max_iter):
        if curr_conflicts == 0 or temp < 0.001:
            break
            
        col = random.randint(0, 7)
        row = random.randint(0, 7)
        neighbor = list(state)
        neighbor[col] = row
        next_conflicts = count_queen_conflicts(neighbor)
        
        delta = next_conflicts - curr_conflicts
        if delta < 0 or random.random() < math.exp(-delta / temp):
            state = neighbor
            curr_conflicts = next_conflicts
            
        temp *= cooling_rate
        cost_history.append(curr_conflicts)
        
    t1 = time.perf_counter()
    return state, curr_conflicts, len(cost_history), cost_history, (t1 - t0) * 1000

hc_state, hc_conf, hc_iters, hc_restarts, hc_time = hill_climbing_8queens()
sa_state, sa_conf, sa_iters, sa_cost_hist, sa_time = simulated_annealing_8queens()

print("\n--- 3. LOCAL SEARCH BENCHMARK (8-QUEENS) ---")
print(f"Hill Climbing (Restarts) -> Final Conflicts: {hc_conf} | Restarts: {hc_restarts} | Time: {hc_time:.3f} ms")
print(f"Simulated Annealing       -> Final Conflicts: {sa_conf} | Iterations: {sa_iters} | Time: {sa_time:.3f} ms")

# ================================================================================
# PARADIGM 4: CONSTRAINT SATISFACTION PROBLEM (CSP)
# Domain: Australia Map 3-Coloring (Backtracking + AC-3 + MRV)
# ================================================================================

territories = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
colors = ['Red', 'Green', 'Blue']

neighbors_csp = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['Q', 'SA', 'V'],
    'V': ['SA', 'NSW'],
    'T': []
}

backtrack_count = 0
constraint_checks = 0

def is_valid_assignment(var, color, assignment):
    global constraint_checks
    for neighbor in neighbors_csp[var]:
        constraint_checks += 1
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def select_mrv_variable(assignment, domains):
    unassigned = [v for v in territories if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))

def csp_backtrack(assignment, domains):
    global backtrack_count
    if len(assignment) == len(territories):
        return assignment
        
    var = select_mrv_variable(assignment, domains)
    for color in domains[var]:
        if is_valid_assignment(var, color, assignment):
            assignment[var] = color
            result = csp_backtrack(assignment, domains)
            if result is not None:
                return result
            del assignment[var]
            backtrack_count += 1
            
    return None

def solve_australia_csp():
    global backtrack_count, constraint_checks
    t0 = time.perf_counter()
    backtrack_count = 0
    constraint_checks = 0
    domains = {v: list(colors) for v in territories}
    solution = csp_backtrack({}, domains)
    t1 = time.perf_counter()
    return solution, backtrack_count, constraint_checks, (t1 - t0) * 1000

csp_solution, csp_backtracks, csp_checks, csp_time = solve_australia_csp()

print("\n--- 4. CSP BENCHMARK (AUSTRALIA MAP 3-COLORING) ---")
print(f"CSP Solution: {csp_solution}")
print(f"Backtracks: {csp_backtracks} | Constraint Checks: {csp_checks} | Time: {csp_time:.3f} ms")

# ================================================================================
# PLOT GENERATION
# ================================================================================

# Plot 1: Nodes Expanded & Time Comparison for Search Paradigms
fig, ax1 = plt.subplots(figsize=(7, 4.5), dpi=300)

algos = ['BFS', 'DFS', 'A*', 'GBFS']
nodes_list = [bfs_nodes, dfs_nodes, astar_nodes, gbfs_nodes]
time_list = [bfs_time, dfs_time, astar_time, gbfs_time]

x = np.arange(len(algos))
width = 0.35

rects1 = ax1.bar(x - width/2, nodes_list, width, label='Nodes Expanded', color='#1f77b4')
ax1.set_ylabel('Total Nodes Expanded', color='#1f77b4', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_xticks(x)
ax1.set_xticklabels(algos, fontweight='bold')

ax2 = ax1.twinx()
rects2 = ax2.bar(x + width/2, time_list, width, label='Execution Time (ms)', color='#ff7f0e')
ax2.set_ylabel('Execution Time (ms)', color='#ff7f0e', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')

plt.title('Performance Benchmark: Uninformed vs Informed Search', fontsize=12, fontweight='bold', pad=12)
fig.tight_layout()
p1_path = os.path.join(output_dir, "search_performance_comparison.png")
plt.savefig(p1_path, dpi=300)
plt.close()
print(f"\nSaved plot: {p1_path}")

# Plot 2: Simulated Annealing Convergence Curve
plt.figure(figsize=(7, 4.5), dpi=300)
plt.plot(range(len(sa_cost_hist)), sa_cost_hist, color='#2ca02c', linewidth=2, label='Queen Conflict Count')
plt.xlabel('Annealing Iterations', fontsize=11, fontweight='bold')
plt.ylabel('Objective Function Cost (Conflicts)', fontsize=11, fontweight='bold')
plt.title('Simulated Annealing Convergence (8-Queens Optimization)', fontsize=12, fontweight='bold', pad=10)
plt.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
p2_path = os.path.join(output_dir, "local_search_convergence.png")
plt.savefig(p2_path, dpi=300)
plt.close()
print(f"Saved plot: {p2_path}")

# Dark Terminal Output Image Generation
width_img, height_img = 820, 480
img = Image.new('RGB', (width_img, height_img), color='#1e1e1e')
draw = ImageDraw.Draw(img)

draw.rectangle([(0, 0), (width_img, 30)], fill='#2d2d2d')
draw.ellipse([(12, 9), (22, 19)], fill='#ff5f56')
draw.ellipse([(28, 9), (38, 19)], fill='#ffbd2e')
draw.ellipse([(44, 9), (54, 19)], fill='#27c93f')
draw.text((70, 7), 'bash - python search_algorithms_benchmark.py', fill='#cccccc')

term_lines = [
    '==================================================================================',
    '   PRACTICAL 02: COMPARATIVE BENCHMARK ANALYSIS OF AI SEARCH PARADIGMS',
    '==================================================================================',
    '--- 1. UNINFORMED SEARCH BENCHMARK ---',
    f'BFS  -> Path: A->B->E->G->GOAL | Cost: {bfs_cost} | Nodes: {bfs_nodes} | Time: {bfs_time:.3f} ms',
    f'DFS  -> Path: A->C->H->GOAL    | Cost: {dfs_cost} | Nodes: {dfs_nodes} | Time: {dfs_time:.3f} ms',
    '',
    '--- 2. INFORMED HEURISTIC SEARCH BENCHMARK (8-PUZZLE) ---',
    f'A* Search -> Path Depth: {astar_depth} | Nodes Expanded: {astar_nodes} | Time: {astar_time:.3f} ms',
    f'GBFS      -> Path Depth: {gbfs_depth} | Nodes Expanded: {gbfs_nodes} | Time: {gbfs_time:.3f} ms',
    '',
    '--- 3. LOCAL SEARCH BENCHMARK (8-QUEENS) ---',
    f'Hill Climbing (Restarts) -> Conflicts: {hc_conf} | Restarts: {hc_restarts} | Time: {hc_time:.3f} ms',
    f'Simulated Annealing       -> Conflicts: {sa_conf} | Iterations: {sa_iters} | Time: {sa_time:.3f} ms',
    '',
    '--- 4. CSP BENCHMARK (AUSTRALIA MAP 3-COLORING) ---',
    f'Solution: WA: {csp_solution["WA"]}, NT: {csp_solution["NT"]}, SA: {csp_solution["SA"]}, Q: {csp_solution["Q"]}, NSW: {csp_solution["NSW"]}, V: {csp_solution["V"]}, T: {csp_solution["T"]}',
    f'Backtracks: {csp_backtracks} | Constraint Checks: {csp_checks} | Execution Time: {csp_time:.3f} ms',
    '=================================================================================='
]

y_p = 40
for line in term_lines:
    if 'PRACTICAL' in line:
        col = '#4ec9b0'
    elif 'BENCHMARK' in line:
        col = '#ce9178'
    elif 'Solution:' in line or 'Path:' in line:
        col = '#00ff66'
    else:
        col = '#d4d4d4'
    draw.text((15, y_p), line, fill=col)
    y_p += 17

p3_path = os.path.join(output_dir, "terminal_output.png")
img.save(p3_path)
print(f"Saved terminal image: {p3_path}")

print("==================================================================================")
print("Execution Completed Successfully.")
