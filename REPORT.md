# Assignment Report

## 8-Puzzle Problem

**Comparative Performance Analysis of Uninformed and Informed Search Strategies**  
**Algorithms Evaluated:** Breadth-First Search (BFS), Depth-First Search (DFS), Iterative Deepening DFS (IDFS), $A^*$ (Manhattan Distance), and $A^*$ (Euclidean Distance).

## 1. Executive Summary

The **8-Puzzle** is a board problem, consisting of a $3 \times 3$ grid with 8 numbered square tiles (1 through 8) and an empty space (denoted as `0`). The goal is to have initial state reach the goal by moving the tiles within the board, utilising the empty space.

- **INITIAL STATE**

```text

    6 | 3 | 2               
   -----------               
    7 | 1 | 5                
   -----------              
    0 | 4 | 8               
```

- **GOAL STATE**

```text
    0 | 1 | 2
   -----------
    3 | 4 | 5
   -----------
    6 | 7 | 8
```

This report analyzes an experimental evaluation of five state-space search agents initialized from an identical 8-step permutation. The experiment provides a direct empirical comparison between **blind (uninformed)** search mechanisms (BFS, Graph-DFS, IDFS) and **heuristic (informed)** search mechanisms ($A^*$ with Manhattan and Euclidean distances).

## 2. Assumptions

The implementation is grounded in the following design decisions and assumptions:

1. **Unit Step Cost ($c(s, a, s') = 1$):** Every action (sliding a tile into the blank space) has a uniform cost of 1. Therefore, path cost strictly equals the path length $d$.
2. **State Immutability:** The `Puzzle8` board class is immutable. Invoking `move(action)` yields a new instance of `Puzzle8`, ensuring parent board configurations remain unaltered during recursive or backtracking traversals.
3. **Node Decoupling via Search Tree Nodes:** The `Node` class encapsulates search metadata ($g(n)$, $h(n)$, $f(n)$, depth, parent pointer, incoming action) independently of the domain state (`Puzzle8`), facilitating tree and graph traversals without contaminating game logic.
4. **Action Semantics:** Movement is framed from the perspective of the **blank space (`0`)**:
   - `Up`: The blank moves up (tile above swaps down).
   - `Down`: The blank moves down (tile below swaps up).
   - `Left`: The blank moves left (tile to the left swaps right).
   - `Right`: The blank moves right (tile to the right swaps left).
5. **Goal Definition:** The canonical goal state is row-major ordered: `[0, 1, 2, 3, 4, 5, 6, 7, 8]`.

## 3. Initial State Generation & Solvability Proof

### 3.1 Random Generation Mechanism

Arbitrary configurations generated uniformly at random have a $50\%$ probability of being unreachable due to parity constraints. To guarantee solvability without rejection sampling, the experiment utilizes `random_solvable_board(num_moves=8)`:

```python
_REVERSE = {
    Action.Up: Action.Down,
    Action.Down: Action.Up,
    Action.Left: Action.Right,
    Action.Right: Action.Left,
}


def random_solvable_board(num_moves: int = 12) -> Puzzle8:
  board = Puzzle8(list(Puzzle8.complete_state))
  last = None
  for _ in range(num_moves):
    choices = [a for a in board.get_possible_actions() if a != _REVERSE.get(last)]
    last = random.choice(choices)
    board = board.move(last)
  return board
```

#### Operational Logic:

- Starts from the known `complete_state` (the goal).
- Performs a backward random walk of $k = 8$ steps.
- Excludes immediate reverse actions (`_REVERSE.get(last)`) to prevent trivial cycles ($s \to s' \to s$).
- Because the initial state is constructed via valid transitions from the goal, it is **guaranteed to be solvable** in at most 8 moves.

### 3.2 Analytical Solvability (Inversion Parity)

For an $N \times N$ puzzle where $N$ is odd ($N = 3$), a state is solvable if and only if its **inversion count** is **even**.  
An inversion occurs when a tile $i$ precedes tile $j$ in row-major order such that $i > j$ (ignoring the empty tile `0`).

For our initial board: `[6, 3, 2, 7, 1, 5, 0, 4, 8]`

- Tile array (excluding 0): `[6, 3, 2, 7, 1, 5, 4, 8]`
- Inversions:
  - After 6: 3, 2, 1, 5, 4 $\rightarrow 5$ inversions
  - After 3: 2, 1 $\rightarrow 2$ inversions
  - After 2: 1 $\rightarrow 1$ inversion
  - After 7: 1, 5, 4 $\rightarrow 3$ inversions
  - After 1: none $\rightarrow 0$ inversions
  - After 5: 4 $\rightarrow 1$ inversion
  - After 4: none $\rightarrow 0$ inversions
  - After 8: none $\rightarrow 0$ inversions
- Total Inversions = $5 + 2 + 1 + 3 + 0 + 1 + 0 + 0 = 12$.  
Because $12 \pmod 2 \equiv 0$, the initial board is mathematically confirmed to be **solvable**.

## 4. Agent Design, Data Structures & Operation

| Agent | Primary Frontier Data Structure | Closed List / Cycle Detection | Frontier Ingestion / Eviction Strategy | Theoretical Optimality |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | `collections.deque` | Hash Set (`seen`) | First-In, First-Out (FIFO) | Optimal (unit cost) |
| **DFS** | Dynamic Array (`list`) | Hash Set (`explored`) | Last-In, First-Out (LIFO) | Non-Optimal |
| **IDFS** | Recursion / Stack (`list`) | Ancestor Path Check (`_on_path`) | Depth-Bounded LIFO | Optimal (unit cost) |
| **$A^*$ (Manh.)** | Binary Min-Heap (`heapq`) | Hash Set (`explored`) | Priority: $f(n) = g(n) + h(n)$ | Optimal (admissible) |
| **$A^*$ (Eucl.)** | Binary Min-Heap (`heapq`) | Hash Set (`explored`) | Priority: $f(n) = g(n) + h(n)$ | Optimal (admissible) |

### 4.1 Breadth-First Search (BFS)

- **Data Structure:** `collections.deque` for the frontier, Python `set` of state tuples for `seen`.
- **Method of Operation:** BFS explores the state space level-by-level. As soon as a child node is generated, its state is verified against `seen`. If novel, it is added to `seen` immediately (early goal test / frontier containment) and enqueued.
- **Characteristics:** Complete and optimal for uniform step costs. However, its memory consumption grows exponentially as $O(b^d)$.

### 4.2 Depth-First Search (DFS - Graph Search)

- **Data Structure:** Standard Python `list` used as a LIFO stack for the frontier; Python `set` for `explored`.
- **Method of Operation:** Pops the most recently added node. Graph DFS adds states to `explored` upon node expansion. Children are pushed in reverse order (`reversed(self._expand(current_node))`) to visit actions deterministically.
- **Empirical Observation:** DFS found the goal in only **8 node expansions** ($0.000062\text{ s}$). Because the initial state was generated by an 8-step walk from the goal and DFS expanded child nodes in reverse order, the search stack directly unwound the generative sequence. In general 8-puzzle instances, DFS is non-optimal and can explore thousands of sub-optimal branches.

### 4.3 Iterative Deepening DFS (IDFS)

- **Data Structure:** Frontier stack bounded by integer `limit`; cycle detection performed via `_on_path()` traversing node parent pointers.
- **Method of Operation:** Executes Depth-Limited Search iteratively for $\text{limit} = 0, 1, 2, \dots, d$. If the depth limit is reached without finding a goal, `limit` increments.
- **Characteristics:** Combines the space efficiency of DFS ($O(bd)$ memory) with the optimality of BFS. The trade-off is node re-expansion: states at depth $k$ are regenerated $d - k + 1$ times, resulting in **207 expanded nodes** for this run.

### 4.4 $A^*$ Search with Manhattan Distance

- **Data Structure:** Priority Queue using `heapq` storing tuples `(f_score, Node)`; Python `set` for `explored`.
- **Heuristic Function:**
  $$h_{\text{Manhattan}}(s) = \sum_{i=1}^{8} \left( |x_i - x_i^*| + |y_i - y_i^*| \right)$$
  Computes the sum of horizontal and vertical distances each tile must traverse to reach its goal slot.
- **Characteristics:** Admissible ($h(n) \le h^*(n)$) and consistent (monotonic). Guided directly toward the minimum-cost path, expanding only 8 nodes.

### 4.5 $A^*$ Search with Euclidean Distance

- **Data Structure:** Priority Queue via `heapq` storing `(f_score, Node)`; Python `set` for `explored`.
- **Heuristic Function:**
  $$h_{\text{Euclidean}}(s) = \sum_{i=1}^{8} \sqrt{(x_i - x_i^*)^2 + (y_i - y_i^*)^2}$$
- **Characteristics:** Admissible, but strictly dominated by Manhattan distance in grid spaces with orthogonal moves:
  $$h_{\text{Euclidean}}(n) \le h_{\text{Manhattan}}(n) \le h^*(n)$$
  For this specific 8-step problem, both heuristics provided sufficient gradient to follow the optimal path without extraneous branch exploration.

## 5. Experimental Results & Comparative Metrics

The following metrics were logged from the execution of all five agents on the identical initial state:

### Summary Comparison Table

| Metric | Breadth-First Search (BFS) | Depth-First Search (DFS) | Iterative Deepening (IDFS) | $A^*$ Search (Manhattan) | $A^*$ Search (Euclidean) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Solution Found** | **True** | **True** | **True** | **True** | **True** |
| **Path Cost ($g$)** | 8 | 8 | 8 | 8 | 8 |
| **Search Depth ($d$)** | 8 | 8 | 8 | 8 | 8 |
| **Max Depth Reached** | 8 | 8 | 8 | 7 | 7 |
| **Nodes Expanded** | **91** | **8** | **207** | **8** | **8** |
| **Running Time (s)** | 0.000579 | 0.000062 | 0.001589 | 0.000104 | 0.000092 |
| **Optimality Guaranteed?** | Yes | No | Yes | Yes | Yes |

## 6. Performance Analysis

1. **Nodes Expanded:** IDFS expanded the greatest number of nodes (207) due to iterative re-evaluations across depths 0 through 8:
   $$\sum_{i=1}^{8} N_i = 1 + 2 + 5 + 10 + 20 + 36 + 65 + \dots = 207$$
   BFS expanded 91 nodes before encountering the goal at depth 8.
2. **Informed vs. Uninformed Search:** Both $A^*$ variants expanded only 8 nodes—identical to the solution length. The heuristic gradients directed the priority queue directly along the optimal path with zero dead-end expansions.
3. **Execution Runtime:** IDFS required the most CPU time ($1.589\text{ ms}$) due to duplicate node expansions. BFS required $0.579\text{ ms}$, while $A^*$ finished in $\approx 0.1\text{ ms}$. Graph DFS finished in $0.062\text{ ms}$ because of its fortunate reverse-walk trajectory.

## 7. Execution

Each agent successfully generated the identical optimal 8-step transition sequence:
$$\text{Up} \longrightarrow \text{Up} \longrightarrow \text{Right} \longrightarrow \text{Down} \longrightarrow \text{Down} \longrightarrow \text{Left} \longrightarrow \text{Up} \longrightarrow \text{Up}$$

### Trace

```text
------------------------------------------------------------
Step-by-step trace
------------------------------------------------------------
Initial state:

6 | 3 | 2
---------
7 | 1 | 5
---------
0 | 4 | 8

Step 1: move Up

6 | 3 | 2
---------
0 | 1 | 5
---------
7 | 4 | 8

Step 2: move Up

0 | 3 | 2
---------
6 | 1 | 5
---------
7 | 4 | 8

Step 3: move Right

3 | 0 | 2
---------
6 | 1 | 5
---------
7 | 4 | 8

Step 4: move Down

3 | 1 | 2
---------
6 | 0 | 5
---------
7 | 4 | 8

Step 5: move Down

3 | 1 | 2
---------
6 | 4 | 5
---------
7 | 0 | 8

Step 6: move Left

3 | 1 | 2
---------
6 | 4 | 5
---------
0 | 7 | 8

Step 7: move Up

3 | 1 | 2
---------
0 | 4 | 5
---------
6 | 7 | 8

Step 8: move Up

0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8

Goal reached in 8 steps (cost = 8)
```