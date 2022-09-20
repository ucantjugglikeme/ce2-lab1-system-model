import pytest
import random
from main import smooth_sort


@pytest.mark.parametrize("lst", [
    [10, 23, 4, 1, 32, 4, 5, 11, 7, 9, 8],
    [5, 1, 0, 3, 4, 2],
    [],
])
def test_smooth_sort(lst):
    sorted_lst = lst.copy()
    sorted_lst.sort()
    assert smooth_sort(lst) == sorted_lst


def test_smooth_sort_rand():
    n = random.randint(0, 2**8)
    rand_lst = [random.randint(0, 2 ** 32 - 1) for _ in range(n)]
    sorted_lst = rand_lst.copy()
    sorted_lst.sort()
    assert smooth_sort(rand_lst) == sorted_lst


def test_smooth_sort_rand_max():
    n = 2**8
    rand_lst = [2 ** 32 - 1 - i for i in range(n)]
    sorted_lst = rand_lst.copy()
    sorted_lst.sort()
    assert smooth_sort(rand_lst) == sorted_lst
