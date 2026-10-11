import functools 


def opt_cost(start, end, frequencies):
    if start > end:
        return 0

    best = float("inf")

    for root in range(start, end + 1):
        sum_new_root_and_posterity = sum(frequencies[start:end + 1])
        left = opt_cost(start, root - 1, frequencies)
        right = opt_cost(root + 1, end, frequencies)
        temp = left + right + sum_new_root_and_posterity

        if temp < best:
            best = temp

    return best


def opt_cost_part2(frequencies):
    @functools.cache
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

    return solve(0, len(frequencies) - 1)


def opt_cost_and_tree(keys, frequencies):
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
            total = slice_sum + left_cost + right_cost
            candidate_tree = (keys[root], left_tree, right_tree)

            if total < best:
                best = total
                best_root = root
                best_tree = candidate_tree

        return best, best_tree

    return solve(0, len(frequencies) - 1)


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
            sum_left_slice = sum(frequencies[start:root])
            left_penalty_cost = L * sum_left_slice
            total = slice_sum + left_cost + right_cost + left_penalty_cost
            candidate_tree = (keys[root], left_tree, right_tree)

            if total < best:
                best = total
                best_root = root
                best_tree = candidate_tree

        return best, best_tree

    return solve(0, len(frequencies) - 1)


def assert_all_cost_versions_match(frequencies):
    part1 = opt_cost(0, len(frequencies) - 1, frequencies)
    part2 = opt_cost_part2(frequencies)
    keys = [chr(ord("A") + i) for i in range(len(frequencies))]
    part3_cost, _ = opt_cost_and_tree(keys, frequencies)

    assert part1 == part2 == part3_cost


def run_tests():
    keys = ["A"]
    frequencies = [7]
    assert opt_cost(0, 0, frequencies) == 7
    assert opt_cost_and_tree(keys, frequencies) == (7, ("A", None, None))

    keys = ["A", "B", "C", "D", "E"]
    frequencies = [2, 1, 1, 2, 3]
    assert_all_cost_versions_match(frequencies)
    assert opt_cost_and_tree(keys, frequencies) == (
        19,
        ("D", ("A", None, ("B", None, ("C", None, None))), ("E", None, None)),
    )
    assert opt_cost_and_tree_with_l(keys, frequencies, 1) == (
        23,
        ("D", ("A", None, ("B", None, ("C", None, None))), ("E", None, None)),
    )
    assert opt_cost_and_tree_with_l(keys, frequencies, 3) == (
        28,
        ("A", None, ("C", ("B", None, None), ("D", None, ("E", None, None)))),
    )

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
