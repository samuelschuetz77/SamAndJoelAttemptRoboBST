# How the robot works: a 7-bin walkthrough

Example input: `frequencies = [2, 6, 3, 9, 2, 7, 1]`, `cost_per_rotation = 3`, `move_cost_per_distance = 1`, `cost_per_scan = 2`.

The optimal cost is **510**.

## The rules (from the assignment)

- The robot starts at bin 0, facing negative (toward the front desk).
- It only moves in the direction it is facing. Turning around costs `cost_per_rotation`.
- Moving costs `move_cost_per_distance` per bin of distance. Distance is measured in bins on the shelf, not tree levels.
- At each tree node it visits, it scans the bin (`cost_per_scan`). The scan says "match", "choose to go left", or "choose to go right".
- On a match it faces negative, then moves back to bin 0.
- A move of distance 0 needs no rotation.
- The bin frequencies are expected requests per day. The day's cost is the sum of (per-request cost x frequency) over all bins.

## The shelf

```
 desk ◄── negative                                             positive ──►
         ┌───────┬───────┬───────┬───────┬───────┬───────┬───────┐
 bin:    │   0   │   1   │   2   │   3   │   4   │   5   │   6   │
 freq:   │   2   │   6   │   3   │   9   │   2   │   7   │   1   │
         └───────┴───────┴───────┴───────┴───────┴───────┴───────┘
          ▲
          robot starts at bin 0, facing negative
```

## The tree (the robot's instructions)

```
              (1)
             /   \
          (0)     (3)
                 /   \
              (2)     (5)
                     /   \
                  (4)     (6)
```

The tree only says which bin to check next. The robot always moves in a straight line along the shelf.

## Cost of one request for each bin

Every request starts the same way. The root is bin 1, so the robot must rotate to face positive (3) and move 0 -> 1 (1) before the first scan.

**Bin 0 (freq 2)**
```
 rotate to face pos                       3
 move 0 ──► 1                             1
 scan bin 1 → choose to go left           2
 rotate to face neg                       3
 move 1 ──► 0                             1
 scan bin 0 → match                       2
 already facing neg, already at 0         0
                                          ──
                                          12
```

**Bin 1 (freq 6)**
```
 rotate to face pos                       3
 move 0 ──► 1                             1
 scan bin 1 → match                       2
 rotate to face neg                       3
 move 1 ──► 0                             1
                                          ──
                                          10
```

**Bin 2 (freq 3)**
```
 rotate to face pos                       3
 move 0 ──► 1                             1
 scan bin 1 → choose to go right          2
 move 1 ──► 3  (already facing pos)       2
 scan bin 3 → choose to go left           2
 rotate to face neg                       3
 move 3 ──► 2                             1
 scan bin 2 → match                       2
 move 2 ──► 0  (already facing neg)       2
                                          ──
                                          18
```

**Bin 3 (freq 9)**
```
 rotate to face pos                       3
 move 0 ──► 1                             1
 scan bin 1 → choose to go right          2
 move 1 ──► 3                             2
 scan bin 3 → match                       2
 rotate to face neg                       3
 move 3 ──► 0                             3
                                          ──
                                          16
```

**Bin 4 (freq 2)**
```
 rotate to face pos                       3
 move 0 ──► 1                             1
 scan bin 1 → choose to go right          2
 move 1 ──► 3                             2
 scan bin 3 → choose to go right          2
 move 3 ──► 5                             2
 scan bin 5 → choose to go left           2
 rotate to face neg                       3
 move 5 ──► 4                             1
 scan bin 4 → match                       2
 move 4 ──► 0                             4
                                          ──
                                          24
```

**Bin 5 (freq 7)**
```
 rotate to face pos                       3
 move 0 ──► 1                             1
 scan bin 1 → choose to go right          2
 move 1 ──► 3                             2
 scan bin 3 → choose to go right          2
 move 3 ──► 5                             2
 scan bin 5 → match                       2
 rotate to face neg                       3
 move 5 ──► 0                             5
                                          ──
                                          22
```

**Bin 6 (freq 1)**
```
 rotate to face pos                       3
 move 0 ──► 1                             1
 scan bin 1 → choose to go right          2
 move 1 ──► 3                             2
 scan bin 3 → choose to go right          2
 move 3 ──► 5                             2
 scan bin 5 → choose to go right          2
 move 5 ──► 6                             1
 scan bin 6 → match                       2
 rotate to face neg                       3
 move 6 ──► 0                             6
                                          ──
                                          26
```

## Day total

| Bin | Freq | Cost per request | Freq x cost |
|---|---|---|---|
| 0 | 2 | 12 | 24 |
| 1 | 6 | 10 | 60 |
| 2 | 3 | 18 | 54 |
| 3 | 9 | 16 | 144 |
| 4 | 2 | 24 | 48 |
| 5 | 7 | 22 | 154 |
| 6 | 1 | 26 | 26 |
| **Total** | | | **510** |

## Where rotations happen

- A rotation happens only when the robot has to change direction.
- Bin 1 -> bin 3 -> bin 5 is a run of right-moves. It costs no extra rotations, because the robot is already facing positive.
- Going left (e.g. bin 3 -> bin 2, or bin 5 -> bin 4) costs one rotation to face negative.
- That rotation doubles as the "face negative" turn needed for the trip home, so the trip home costs no second rotation.
- Bin 0 is a special case. It sits to the left of the root, so the robot goes out and turns back, paying two rotations.

## Why this tree wins

| Tree | Total cost |
|---|---|
| Optimal (above) | **510** |
| Perfectly balanced, root at bin 3 | 544 |
| Chain `(0) → (1) → ... → (6)`, all right children | 580 |

The balanced tree is not the cheapest. The optimal tree puts the heavily requested bins 1, 3 and 5 on the main path, near the root. The tree is not symmetric, because the best root depends on the frequencies and on the robot starting at bin 0.

## How this was checked

The costs above were computed with a small simulation of the rules, in a throwaway script outside this project. I ran it over all 429 possible trees on 7 bins to confirm this tree is the unique cheapest one. The same simulation reproduces all eight provided test costs (10, 44, 348, 30, 2072, 1940, 1132, 1512), so the cost model matches the assignment's tests.
