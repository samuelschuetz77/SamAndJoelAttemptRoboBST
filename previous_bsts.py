# previous_bsts.py
#
# Sam's optimal binary search tree code from the earlier assignment
# "Backtracking for Optimal Binary Search Trees" (JEA section 2.8), kept here as
# reference for the robot version. The logic is unchanged from the submitted
# file; only the explanatory comments are new.
#
# The shared idea in every version:
#   * The keys are sorted and fixed. Only the SHAPE of the tree is up to us.
#   * frequencies[i] = how many times key i will be searched for.
#   * Cost of a tree = sum over keys of (frequency * number of comparisons),
#     where the root costs 1 comparison, its children 2, and so on.
#   * To solve the range start..end, try EVERY key in the range as the root.
#     Keys left of the root must go in the left subtree, keys right of it in the
#     right subtree. Solve both sides recursively, add them up, keep the cheapest.
#   * Each level adds sum(frequencies[start..end]): every search in this range
#     must compare against this range's root once before going deeper.
#   * Base case: an empty range (start > end) costs 0.
#   * There is no memoization, so these are exponential. That is intended for
#     this assignment, and it is the exact thing the robot project fixes with
#     lru_cache in Part 3.


# ---------------------------------------------------------------------------
# Version 1: plain backtracking, cost only (Parts 1 and 2 of that assignment)
# ---------------------------------------------------------------------------
# opt_cost(start, end, frequencies) returns the minimum total cost of a BST over
# the keys start..end. `frequencies` is passed down through every recursive call.
def opt_cost(start, end, frequencies):
    if start > end:
        return 0  # empty range: no keys, no cost

    best = float("inf")

    for root in range(start, end + 1):  # try each key as the root
        level_sum = sum(frequencies[start:end + 1])  # every search pays 1 at this root
        left = opt_cost(start, root - 1, frequencies)  # best tree for keys left of root
        right = opt_cost(root + 1, end, frequencies)  # best tree for keys right of root
        temp = left + right + level_sum  # total cost if `root` is chosen

        if temp < best:
            best = temp  # keep the cheapest choice of root

    return best


# ---------------------------------------------------------------------------
# Version 2: same algorithm, with a nested function (Part 2 of that assignment)
# ---------------------------------------------------------------------------
# Refactor: `frequencies` is no longer a parameter of the recursive function.
# solve() reads it from the enclosing function, so a subproblem is identified by
# just (start, end). This is the shape you want before adding memoization,
# because the cache key becomes only those two hashable integers.
def opt_cost_part2(frequencies):
    def solve(start, end):
        if start > end:
            return 0

        best = float("inf")

        for root in range(start, end + 1):
            left = solve(start, root - 1)
            right = solve(root + 1, end)
            slice_sum = sum(frequencies[start:end + 1])
            total = slice_sum + left + right

            if total < best:
                best = total

        return best

    return solve(0, len(frequencies) - 1)  # top-level call covers every key


# ---------------------------------------------------------------------------
# Version 3: cost AND the tree itself (Part 3 of that assignment)
# ---------------------------------------------------------------------------
# solve() now returns a (cost, tree) pair. A tree is the nested tuple
# (key, left_tree, right_tree), and None is the empty tree. For every candidate
# root we build the tuple from the two already-built subtrees, and we keep the
# tree that goes with the cheapest cost. Cost and tree are tracked together, so
# the running time stays the same as Version 2.
def opt_cost_and_tree(keys, frequencies):
    def solve(start, end):
        if start > end:
            return 0, None  # empty range: cost 0, empty tree

        best = float("inf")
        best_root = None
        best_tree = None

        for root in range(start, end + 1):
            left_cost, left_tree = solve(start, root - 1)
            right_cost, right_tree = solve(root + 1, end)
            slice_sum = sum(frequencies[start:end + 1])
            total = slice_sum + left_cost + right_cost
            candidate_tree = (keys[root], left_tree, right_tree)  # only references are copied

            if total < best:
                best = total
                best_root = root
                best_tree = candidate_tree

        return best, best_tree

    return solve(0, len(frequencies) - 1)


# ---------------------------------------------------------------------------
# Version 4: variation with a "left penalty" L (Parts 4 and 5 of that assignment)
# ---------------------------------------------------------------------------
# New rule: every time a search goes LEFT, it pays an extra constant L.
# Which searches go left at a given root? Exactly the ones for keys in the left
# part of the range (start..root-1). So choosing this root adds
#     L * sum(frequencies[start:root])
# on top of the usual cost. Everything else is identical to Version 3, and the
# penalty for deeper left turns is paid inside the recursive calls.
# This is the same kind of reasoning the robot problem needs: work out what each
# choice of root charges to the whole span, then let the recursion handle the rest.
def opt_cost_and_tree_with_l(keys, frequencies, L):
    def solve(start, end):
        if start > end:
            return 0, None

        best = float("inf")
        best_root = None
        best_tree = None

        for root in range(start, end + 1):
            left_cost, left_tree = solve(start, root - 1)
            right_cost, right_tree = solve(root + 1, end)
            slice_sum = sum(frequencies[start:end + 1])
            sum_left_slice = sum(frequencies[start:root])  # searches that turn left here
            left_penalty_cost = L * sum_left_slice  # each pays L
            total = slice_sum + left_cost + right_cost + left_penalty_cost
            candidate_tree = (keys[root], left_tree, right_tree)

            if total < best:
                best = total
                best_root = root
                best_tree = candidate_tree

        return best, best_tree

    return solve(0, len(frequencies) - 1)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
# Versions 1, 2 and 3 must report the same minimum cost on any input.
def assert_all_cost_versions_match(frequencies):
    part1 = opt_cost(0, len(frequencies) - 1, frequencies)
    part2 = opt_cost_part2(frequencies)
    keys = [chr(ord("A") + i) for i in range(len(frequencies))]
    part3_cost, _ = opt_cost_and_tree(keys, frequencies)

    assert part1 == part2 == part3_cost


def run_tests():
    # One key: the tree is a single node, cost = its frequency.
    keys = ["A"]
    frequencies = [7]
    assert opt_cost(0, 0, frequencies) == 7
    assert opt_cost_and_tree(keys, frequencies) == (7, ("A", None, None))

    # The five-key anchor example (frequencies 2 1 1 2 3), optimal cost 19.
    keys = ["A", "B", "C", "D", "E"]
    frequencies = [2, 1, 1, 2, 3]
    assert_all_cost_versions_match(frequencies)
    assert opt_cost_and_tree(keys, frequencies) == (
        19,
        ("D", ("A", None, ("B", None, ("C", None, None))), ("E", None, None)),
    )
    # With L = 1 the best tree keeps its shape and costs 4 more.
    assert opt_cost_and_tree_with_l(keys, frequencies, 1) == (
        23,
        ("D", ("A", None, ("B", None, ("C", None, None))), ("E", None, None)),
    )
    # With L = 3 left turns are expensive enough that the best tree changes shape.
    assert opt_cost_and_tree_with_l(keys, frequencies, 3) == (
        28,
        ("A", None, ("C", ("B", None, None), ("D", None, ("E", None, None)))),
    )

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
