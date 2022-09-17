import sys
import ast


_leonardo_nums = [1, 1]


# returns the k-th Leonardo number
def l_(k):
    try:
        return _leonardo_nums[k]
    except IndexError:
        while len(_leonardo_nums) <= k:
            _leonardo_nums.append(_leonardo_nums[-2] + _leonardo_nums[-1] + 1)
        return _leonardo_nums[k]


# sorts into ascending order
def smooth_sort(arr):
    size_list = _create_heap(arr)
    _sort_heap(arr, size_list)
    return arr


# sorts the max heap in-place. requires the list of sizes of leonardo trees in
# the forest
def _sort_heap(heap, size_list):
    for heap_size in reversed(range(len(heap))):
        _dequeue_max(heap, size_list, heap_size)


# removes the max value from the graph
def _dequeue_max(heap, size_list, heap_size):
    removed_size = size_list.pop()
    # case 1: rightmost tree has a single node
    if removed_size == 0 or removed_size == 1:
        pass  # already removed
    # case 2: rightmost tree has two children
    else:
        # add sizes back
        size_list.append(removed_size - 1)
        size_list.append(removed_size - 2)
        # calculate indices of left and right children
        left_idx = heap_size - l_(size_list[-1]) - 1
        right_idx = heap_size - 1
        left_size_idx = len(size_list) - 2
        right_size_idx = len(size_list) - 1
        # fix left child
        idx, size_idx = _fix_roots(heap, size_list, left_idx, left_size_idx)
        _sift_down(heap, idx, size_list[size_idx])
        # fix right child
        idx, size_idx = _fix_roots(heap, size_list, right_idx, right_size_idx)
        _sift_down(heap, idx, size_list[size_idx])


# modifies array in-place to make a heap. returns list of sizes of leonardo
# trees in the forest
def _create_heap(arr):
    size_list = []
    for heap_end in range(len(arr)):
        # Update the sizes of the trees in the forest
        _add_new_root(size_list)

        # Swap the root nodes of the trees. Return [heap index, size index]
        idx, size_idx = _fix_roots(arr, size_list, heap_end, len(size_list) - 1)

        # Fix the tree that now has the new node
        _sift_down(arr, idx, size_list[size_idx])

    return size_list


# updates the list of sizes of leonardo trees in a forest after a new node is
# added
def _add_new_root(size_list):
    # case 1: Empty forest. Add L_1 tree.
    if len(size_list) == 0:
        size_list.append(1)
    # case 2: Forest with two rightmost trees differing by 1.
    #         Replace the last two trees of size L_k-1 and L_k-2 by a single
    #         tree of size L_k.
    elif len(size_list) > 1 and size_list[-2] == size_list[-1] + 1:
        size_list[-2] = size_list[-2] + 1
        del size_list[-1]
    # case 3: Add a new tree, either L_1 or L_0
    else:
        # case 1: Rightmost tree is an L_1 tree. Add L_0 tree.
        if size_list[-1] == 1:
            size_list.append(0)
        # case 2: Rightmost tree is not an L_1 tree. Add L_1 tree.
        else:
            size_list.append(1)


# modifies 'heap' in place, assuming an implicit Leonardo heap structure exists
# with trees having sizes in the order given by 'sizes'
def _fix_roots(heap, sizes, start_heap_idx, start_size_idx):
    # variables in this function are referring to indexes
    cur = start_heap_idx
    size_cur = start_size_idx
    # keep fixing roots until we're at the leftmost root
    while size_cur > 0:
        next_ = cur - l_(sizes[size_cur])
        # stop if the next root is not strictly greater than the current root
        if heap[next_] <= heap[cur]:
            break
        # stop if the next root is not greater than both children of the
        # current root, if those children exist, i.e. the size of the current
        # tree is not 0 or 1.
        if sizes[size_cur] > 1:
            right = cur - 1
            left = right - l_(sizes[size_cur]-2)
            if heap[next_] <= heap[right] or heap[next_] <= heap[left]:
                break

        # swap the current root with the next root
        temp = heap[cur]
        heap[cur] = heap[next_]
        heap[next_] = temp
        # continue, starting with the next root as the current root
        size_cur = size_cur - 1
        cur = next_
    return cur, size_cur


# Fixes the tree of size tree_size rooted at root_idx in heap, where heap is otherwise a valid heap
def _sift_down(heap, root_idx, tree_size):
    cur = root_idx
    # continue iterating until there are no child nodes
    while tree_size > 1:
        right = cur - 1
        left = cur - 1 - l_(tree_size - 2)
        # the root is at least as large as both children
        if heap[cur] >= heap[left] and heap[cur] >= heap[right]:
            break
        # the right child is at least as large as the left child
        elif heap[right] >= heap[left]:
            heap[cur], heap[right] = heap[right], heap[cur]
            cur = right
            tree_size = tree_size - 2
        # the left child is the greatest of the three
        else:
            heap[cur], heap[left] = heap[left], heap[cur]
            cur = left
            tree_size = tree_size - 1


def main(args):
    lst = ast.literal_eval(args)
    smooth_sort(lst)
    return lst


if __name__ == "__main__":
    try:
        print(main(sys.argv[1]))
    except IndexError:
        print(main("[10, 23, 4, 1, 32, 4, 5, 11, 7, 9, 8]"))
