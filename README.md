# 🌾 The Farmer Was Replaced: my Python journey

The code behind my automated farm in **The Farmer Was Replaced**, a game where you program a drone in Python to plant, harvest and solve challenges. This repository is the record of my learning journey: trial, error, measuring and iterating until I reached efficient, parallel solutions.

> File and function names are in Portuguese (`FAZENDA` = farm, `ABOBORA` = pumpkin, `CACTO` = cactus, `CENOURA` = carrot, `GRAMA` = grass, `MADERA` = wood, `DINHEIRO` = money, `MEDIR` = measure, `POLICULTURA` = polyculture).

## ✨ Technologies

- `Python` (the game's built-in dialect)
- Multi-drone parallelism
- Search algorithms: DFS, BFS, wall following
- Hamiltonian cycles, bubble sort

## 🚀 Highlights

- **3.4× faster maze solver** - A mapping + reuse strategy cut each treasure from 201,874 to 58,977 ticks
- **Multi-drone parallelism** - `for_all(f)` runs a function on every tile using all available drones, with no race conditions
- **3-phase polyculture** - Crops and companion plants planted in parallel without drones fighting over tiles
- **Hamiltonian-cycle snake** - Covers the whole field without the dinosaur ever biting itself
- **Measured, not guessed** - Every optimization benchmarked with `get_tick_count()`

## 🎯 Files

| File | What it does |
|---|---|
| `main.py` | Main loop (runs the current strategy) |
| `Utilidades.py` | Core helpers: `move_to`, `for_all` (multi-drone parallelism), fertilizer with hysteresis and hat switching |
| `FAZENDA.py` | `plantar_e_colher(tipo)` plants, fertilizes, harvests and replants each tile **in the same pass**, in parallel |
| `GRAMA.py` / `MADERA.py` / `CENOURA.py` | Simple parallel crops |
| `ABOBORA.py` | Pumpkins merging into a giant block (yields `n×n×6`) |
| `CACTO.py` | Cactus: plants, **sorts the field** (rows and columns) and harvests everything at once |
| `POLICULTURA.py` | Parallel polyculture **in 3 phases**: crop + companion (`get_companion`) with no drone contention |
| `MAZE.py` | Maze: wall follower (left hand) |
| `segundoMAZE.py` | Maze: DFS guided by `measure()` |
| `mapaMAZE.py` | Maze: **map + maze reuse** (the fastest) |
| `MEDIR.py` | Race between the maze algorithms, timed with `get_tick_count()` |
| `DINOSSAURO.py` | "Snake" with the dinosaur hat: Hamiltonian cycle to harvest bones |
| `DINHEIRO.py` | Runner that farms gold with `mapaMAZE` |

## 🧠 Technical Deep Dive

### Multi-drone parallelism
`Utilidades.for_all(f)` runs a function on every tile using **all available drones** (one per row), with the pattern `if not spawn_drone(task): task()`, then waits for all of them to finish. Each drone works on disjoint tiles to avoid race conditions.

### Maze with a map (`mapaMAZE.py`)
Using `Weird_Substance` **on top of the treasure** collects the gold and places a new treasure **in the same maze** (up to 300 times). So while it moves, the drone records the reachable neighbors of each tile in a table:
- **1st treasure:** explores with DFS guided by `measure()`, mapping as it goes.
- **Next ones:** **BFS on the map** gives the shortest path through known tiles, with no exploring. If the treasure lands in an unmapped area, the drone goes to the closest known tile and explores from there.
- Walls only **disappear** between treasures, so a passage recorded as open stays open.
- A fresh map for each maze.

### Measuring with the timer (`MEDIR.py`)
`get_tick_count()` counts execution ticks, the game's cost unit, which does not change with speed or power. Measuring is free. Results for 30 treasures on a 32×32 field:

| Version | ticks/treasure | real time |
|---|---|---|
| `segundoMAZE` (new maze for every treasure) | 201,874 | ~33 min |
| `mapaMAZE` (first version) | 103,299 | ~17 min |
| `mapaMAZE` optimized | **58,977** | **~10 min** |

**3.4× faster** than `segundoMAZE`, with the same gold and the same amount of substance spent.

### Fertilizer with hysteresis
Each tile is fertilized until the plant is ready. When the stock **runs out**, it stops, and only starts fertilizing again once it has **50,000** saved up. Fertilized plants get infected and half the harvest becomes `Weird_Substance`, which feeds the mazes. Cactus is left out on purpose: it grows in ~1s, and the infection would halve the sorted field's harvest.

### One hat per function
Each function equips its own hat (`Straw`, `Tree`, `Carrot`, `Pumpkin`, `Cactus`, `Green`, `Brown`, `Wizard`, `Gold`, `Dinosaur`), so I can tell from afar what is running. Switching hats at the start of the mazes also removes the dinosaur hat, which was stopping the maze from growing.

### Cactus
The harvest only spreads when the field is **sorted** (rows ascending W→E, columns S→N). Since you can only swap neighbors (`swap`), I use **bubble sort** per row and per column, in parallel.

### Pumpkin
Pumpkins merge into a giant block when **all** of them are grown (`n×n×6`). Since 20% die while growing, the code replants in parallel until the field merges.

### Dinosaur (snake)
It eats apples (bought with cactus) to grow its tail; switching hats rewards `length²` bones. The final version uses a **Hamiltonian cycle** that covers the whole field without the snake biting itself, with `set_world_size` guaranteeing an even-sized field.

## 📍 The Process (the trial-and-error part)

- **Maze, three generations:** wall follower (simple, but sweeps everything) → DFS guided by `measure()` → **map + reuse**. For a single-treasure maze, mapping doesn't help, because you have to walk to discover the map. The turning point was realizing that **the same maze can yield up to 300 treasures**, and then the map becomes very valuable.

- **Measure before optimizing:** the first measurement showed the map's curve **backwards**: the 1st treasure cost 45k ticks, and the following ones 105k. The timing docs explained it: **every code operation also costs ticks**, and sets and dictionaries charge by key size. The BFS was recomputing the entire map for every treasure. The fixes: stop the BFS once the treasure is found, store tiles as a number (`y * size + x`) instead of a tuple, keep the neighbors precomputed in the map, and read the field size only once. After that, the following treasures dropped to ~52k ticks, **4.5× cheaper than the first**.

- **The `move_to` that went around the world:** to move 2 tiles West, the distance is −2, and −2 is always less than `size/2`, so it went East and wrapped around the whole field. It barely showed on the farm, but in polyculture (short hops backwards all the time) it was very costly. Now it takes the shortest path and moves a fixed number of steps, so it never gets stuck in a `while`.

- **Polyculture, three versions until there was no contention:** one drone per row gave *"Can't plant Carrot on Grassland"* warnings: `till()` **toggles** the soil, and two drones tilling the same tile cancelled each other out. Running in **waves** of rows 7 apart fixed it, but used few drones. The final version has **3 phases** (plant and record requests → plant companions → harvest), and in each phase every drone only touches its own row. Drones return their requests through `wait_for`.

- **Cactus, not every algorithm fits:** since you can only swap neighbors, I had to use **bubble sort**. The game's hint saved me: "once the rows are sorted, sorting the columns doesn't unsort them".

- **Dinosaur, the snake saga:** pure cycle (**safe but slow**) → greedy with `measure()` (**fast but got cornered**) → hybrid with shortcuts (spun in the corner, in the middle, in loops). The bugs: a wrong shortcut limit, the missing Tapsell margin, and `set.discard()`, which **does not exist** in the game's Python. In the end, I kept the safe version. And the Hamiltonian cycle only closes on an **even field**, solved with `set_world_size`.

- **The tooling gotcha:** while the game is open, it **rewrites/deletes** files on disk on every autosave. I learned to edit inside the game's editor or close the game before saving from outside.

- **Scaling with drones:** `for_all` uses up to `max_drones()` (one per row). As long as the number of drones is ≤ the number of rows, it uses all of them automatically.

## 🚦 Running the Project

1. Get **The Farmer Was Replaced** on Steam
2. Copy the `.py` files into the game's save folder (close the game first, see the tooling gotcha above)
3. Open the game and run `main.py` from the in-game editor
