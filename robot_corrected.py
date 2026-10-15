# Samuel Schuetz | 10/06 - 10/10/2026 | Initially worked with Harry
import functools

def solution(frequencies, cost_per_rotation, move_cost_per_distance, cost_per_scan, memoize=True):
    n = len(frequencies)
    # Given:
    # * a left and right index on the frequencies array
    # * the index of the parent (0 when starting out)
    # * the index of the grandparent (0 when starting out)
    #
    # return a tuple with two items:
    # 1) the cost of the optimal BST
    # 2) the optimal BST
    def g(L, R, parent, grandparent):
        
        if L > R:
            return (0, ())

        
        subtree_freq_total = sum(frequencies[L : R + 1])
        best_subtree_cost = float("inf")
        best_subtree = ()

        
        # i is the index of the root of a potential best subtree
        for i in range(L, R + 1):
            left_cost, left_tree = g(L, i - 1, i, parent)
            right_cost, right_tree = g(i + 1, R, i, parent)
            
            # Add cost for subtrees
            subtree_cost = left_cost + right_cost
            
            # Add cost for scans
            subtree_cost += subtree_freq_total * cost_per_scan
            
             # Add cost for new distance to be traveled, we care about rights because rights we can double to get round trips
            if i > parent:
                subtree_cost += 2 * move_cost_per_distance * subtree_freq_total * abs(parent - i)
                
                # Add cost for new rotations
                if parent <= grandparent:
                    subtree_cost += 2 * cost_per_rotation * subtree_freq_total
            
            if subtree_cost < best_subtree_cost:
                best_subtree_cost = subtree_cost
                best_subtree = (i, left_tree, right_tree)

        return best_subtree_cost, best_subtree

    if memoize:
        g = functools.cache(g)

    return g(0, n - 1, 0, 0)

def optimal_cost_backtracking(frequencies, cost_per_rotation, move_cost_per_distance, cost_per_scan):
    best_overall_cost, best_tree = solution(frequencies, cost_per_rotation, move_cost_per_distance, cost_per_scan, memoize=False)
    return best_overall_cost

def optimal_cost_memoized(frequencies, cost_per_rotation, move_cost_per_distance, cost_per_scan):
    best_overall_cost, best_tree = solution(frequencies, cost_per_rotation, move_cost_per_distance, cost_per_scan)
    return best_overall_cost

def optimal_tree(frequencies, cost_per_rotation, move_cost_per_distance, cost_per_scan):
    return solution(frequencies, cost_per_rotation, move_cost_per_distance, cost_per_scan)

# (frequencies, rotation, move, scan, optimal cost, optimal tree)
# Each case has exactly one optimal tree, so the tree is safe to check.
OPTIMAL_BST_CASES = [
        ([5],
         3, 1, 2,
         10, (0, (), ())),
        ([4, 3],
         3, 1, 2,
         44, (0, (), (1, (), ()))),
        ([4, 30],
         3, 1, 2, 348, (1, (0, (), ()), ())),
        ([1, 1, 1],
         3, 1, 2,
         30, (0, (), (1, (), (2, (), ())))),
        ([4, 3, 28, 100, 5], 3, 1, 2, 2072, (3, (2, (1, (0, (), ()), ()), ()), (4, (), ()))),
        ([1, 1, 1, 1, 1, 50], 7, 2, 1, 1940,
         (5, (4, (3, (2, (1, (0, (), ()), ()), ()), ()), ()), ())),
        ([3, 1, 4, 1, 5, 9, 2, 6], 5, 2, 3, 1132,
         (2, (1, (0, (), ()), ()),
          (5, (4, (3, (), ()), ()), (7, (6, (), ()), ())))),
         ([20, 5, 1, 1, 30, 2, 2, 40], 4, 1, 0, 1512,
          (0, (), (1, (), (2, (), (3, (), (4, (), (5, (), (6, (), (7, (), ()))))))))),
         ]

# Fifty bins. Only a memoized solution finishes this one -- plain backtracking would
# have to look at more trees than there are atoms in anything you care about.
FIFTY_BIN_FREQUENCIES = (4, 3, 28, 100, 5) * 10
FIFTY_BIN_COST = 96532

def test_backtracking_finds_the_optimal_cost():
    for frequencies, rotation, move, scan, cost, tree in OPTIMAL_BST_CASES:
        c = optimal_cost_backtracking(
                frequencies, cost_per_rotation=rotation, move_cost_per_distance=move, cost_per_scan=scan
                )
        assert cost == c, str(frequencies) + ' ' + str(cost) + ' ' + str(c)

def test_memoized_finds_the_same_costs():
    for frequencies, rotation, move, scan, cost, tree in OPTIMAL_BST_CASES:
        assert cost == optimal_cost_memoized(frequencies, cost_per_rotation=rotation, move_cost_per_distance=move, cost_per_scan=scan), frequencies

def test_memoized_handles_fifty_bins():
    assert FIFTY_BIN_COST == optimal_cost_memoized(
            list(FIFTY_BIN_FREQUENCIES), cost_per_rotation=3, move_cost_per_distance=1, cost_per_scan=2)

def test_optimal_tree_and_its_cost():
    for frequencies, rotation, move, scan, cost, tree in OPTIMAL_BST_CASES:
        assert (cost, tree) == optimal_tree(
                frequencies, cost_per_rotation=rotation, move_cost_per_distance=move, cost_per_scan=scan
                ), frequencies

def test_optimal_tree_still_works_on_fifty_bins():
    frequencies = list(FIFTY_BIN_FREQUENCIES)
    cost, tree = optimal_tree(frequencies, cost_per_rotation=3, move_cost_per_distance=1, cost_per_scan=2)
    assert FIFTY_BIN_COST == cost
    # every bin appears exactly once, and the tree is a search tree on the bin numbers
    def bins_in_order(t):
        return [] if t == () else bins_in_order(t[1]) + [t[0]] + bins_in_order(t[2])
    assert list(range(len(frequencies))) == bins_in_order(tree)

# import functools
# @functools.cache or @functools.lru_cache in front of the method name
if __name__ == "__main__":
    # Runs the tests without pytest, so you can step through them in a debugger.
    for test in [test_backtracking_finds_the_optimal_cost,
                 test_memoized_finds_the_same_costs,
                 test_memoized_handles_fifty_bins,
                 test_optimal_tree_and_its_cost,
                 test_optimal_tree_still_works_on_fifty_bins
                 ]:
        test()
        print("passed:", test.__name__)

"""
    n = len(frequencies)
    prefsum = [0] * n
    prefsum[0] = frequencies[0]
    for i in range(1, n):
        prefsum[i] = prefsum[i - 1] + frequencies[i]
    
    def get_subarray_sum(L, R):
        sm = prefsum[R]
        if L > 0:
            sm -= prefsum[L - 1]
        return sm
"""


# Part 1 -- Planning the solution
# 1. Top-level function, parameters, and return value:
# optimal_cost_backtracking(frequencies, cost_per_rotation,
# move_cost_per_distance, cost_per_scan) returns the minimum total expected
# cost of all deliveries, including returning books to bin 0.
# frequencies[i] gives the expected number of requests for bin i.
#
# 2. Recursive subproblem and parameters:
# g(L, R, parent, grandparent) finds the best subtree for the bins from L to R.
# Parent and grandparent identify the incoming movement direction.
# All four parameters are hashable integers; frequencies and costs come
# from the enclosing function.
#
# 3. How the top-level function uses the recursive function:
# solution calls g(0, n - 1, 0, 0), covering every bin and encoding the
# starting position and negative direction. The cost-only wrapper returns
# the cost component; optimal_tree returns both cost and tree.
#
# 4(a). Base cases:
# L > R means the interval is empty. Single-bin intervals use the normal
# root calculation with two empty children.
#
# 4(b). Base-case return values:
# Return (0, ()) for an empty interval: zero additional cost and an empty
# tree. A cost-only recursive version would return just 0.
#
# 5(a). What the recursive function chooses:
# Choose the root index i for the current interval. Every request for a
# bin in that interval must scan this root first.
#
# 5(b). Options for that choice:
# Try every i from L through R, inclusive. Its left interval is L : i-1,
# and its right interval is i+1 : R
#
# 5(c). Cost of each candidate and recursive calls:
# Add costs from g(L,i-1,i,parent) and g(i+1,R,i,parent).
# With F=sum(frequencies[L:R+1]), add F*cost_per_scan.
# If i>parent, add 2*(i-parent)*F*move_cost_per_distance;
# also add 2*F*cost_per_rotation when parent<=grandparent.
# Doubling accounts for return travel and paired turns.
#
# 5(d). Combining the options:
# Keep the candidate with the smallest total cost and its tree
# (i, left_tree, right_tree). Return that cost and tree after trying
# every possible root.
