Explanations

The algorithm builds the total cost for the tree by first calculating the cost for the smaller trees, then putting them together to calculate the cost for larger trees. Cost for scans is always equal to the sum of the frequencies in the subtree. (In fact, if this problem only cared about scanning as a cost, then this week's HW would be identical to last week's.)





Calculating the cost for movement of the robot (using the constant "move_cost_per_distance") is a little more tricky. To see this, look at line 35:

	if i > parent:

This comes into play when we've recursed to a child in the tree that's further to the right (further from the front desk) than its parent. (In other words, the current node must be the right child node of its parent.) When this happens, new cost will always be added on. Even if the robot has already been further to the right during the journey to retrieve the current book, because the robot is forced to follow the BST, it will still go further to the right if its parent has a lesser value than it does, so more distance will need to be added. We add as follows:

	subtree_cost += 2 * move_cost_per_distance * subtree_freq_total * abs(parent - i)

We have the constant "2" in front because any distance we travel to the right, we will have to travel back again the other way. It's a round trip. move_cost_per_distance is given in the problem. subtree_freq_total is the total number of book retrievals that will be affected by this new increase in distance. And abs(parent - i) is the distance from the parent node to the current node, which corresponds to a physical distance for the robot.





Conceptualizing cost for rotations takes some visualization. 

The robot always has to come back to the start after it retrieves a book. Initially, the robot's journey contains no rotations, for example if it only needs to grab a book from index 0. The moment it has to go fetch a book from a non-zero index, two rotations are added. The robot now has the ability to go right by any amount, then left again that same amount back home.

It turns out the robot's rotations are always added in pairs of two. This is because otherwise, the robot would be stuck moving to the right and would be unable to return home.

If we grant the robot four rotations, it will then go (in this order): right, left, right, left. 

And so on for all even numbers of rotations. Bear in mind we want to minimize cost, so we will never add more rotations than is necessary.

For children of a parent node, there are only two options: you can either be the left node or the right node. For grandchildren, there are four options: left-left, left-right, right-left, and right-right. I found that the only case when new rotations are added is for the left-right case. Think of this as the case where a new "zig zag" is added.

New rotations aren't necessarily added for the left-left case because moving to the left is "on the way" home.

For the right-left case, rotations don't necessarily need to be added because the parent node may be the furthest to the right the robot ever goes.

For the right-right case, rotations don't necessarily need to be added because the current node may be the furthest to the right the robot ever goes.

For the left-right case, a new pair of rotations does need to be added because it is guaranteed that the robot was moving to the left, then had to switch and go to the right (and will need to switch back again at some point later on), and it is also guaranteed that this has not yet been accounted for.

The code for this is nested inside the check

	if i > parent:

because this makes sure that the current node is its parent's right child.

We then check that our parent is the left child of its parent using the check

	if parent <= grandparent:

then we add to our cost as follows:

	subtree_cost += 2 * cost_per_rotation * subtree_freq_total

This is because rotations always come in pairs, cost_per_rotation is given in the problem, and the new rotations will apply to the current node's entire subtree.

We use <= instead of just < because initially, parent and grandparent are set to zero. (They aren't technically part of the BST, but we need to be able to give them some kind of initial value.) We want rotations to still be accounted for the first time the robot moves out to the right to some non-zero node. When this happens, i will be > parent (passing the first check) and parent will also be <= grandparent since both will be zero (passing the second check). 

