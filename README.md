# SamAndJoelAttemptRoboBST

Our attempt at the Advanced Algorithms group project "Optimal Binary Search Tree"
(Problem 40, Chapter 3 of Jeff Erickson's *Algorithms*): a warehouse robot fetches
books from a row of bins, and we want the binary search tree over the bins that
minimizes the total expected cost of a day's deliveries.

The starting code came from Harry's repo (dharryc/optBinSearchTree); its commit
history is kept here.

## The problem in one paragraph

Bins sit in a row in ISBN order. The robot starts at bin 0 facing the negative
direction, and a pre-programmed BST over bin indexes tells it which bin to check
next. It can only move in the direction it faces. Three costs apply:
`cost_per_rotation` (turning around), `move_cost_per_distance` (per bin of
distance) and `cost_per_scan` (reading a bin). The input is the expected number of
requests per bin for the day. The goal is the tree with the lowest total cost.

## Where we are

Done:
- Project set up (`uv`, Python 3.14) and the problem described in `description.md`.
- `main.py` has the provided test cases and test functions pasted in.
- `how_robot_works.md` is a worked 7-bin walkthrough of what one robot trip costs,
  where rotations happen, and why the chosen tree wins.
- `previous_bsts.py` holds our earlier optimal-BST code, with each version
  explained: plain backtracking, the nested-function refactor, returning the tree,
  and the left-penalty variation. It is the pattern we are adapting.
- Hand-checked the cost model on the first test case ([5] costs 10). Next up are
  [4, 3] and [4, 30].

Not done yet:
- Part 1 written answers (function name and parameters, subproblem, base cases,
  the choice of root and how costs combine).
- `optimal_cost_backtracking`, `optimal_cost_memoized` and `optimal_tree`.
  The tests in `main.py` call these, so they fail until we write them.
- Test screenshots for Parts 2, 3 and 4, and the reflection.

Open question: during a search, does each left or right step need another
rotation? We have not hand-checked an example of this yet.

## Running

```
python previous_bsts.py   # earlier BST versions; passes
python main.py            # robot tests; fails until the three functions exist
```
