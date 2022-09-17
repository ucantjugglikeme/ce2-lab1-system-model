import pytest
import ast
import random
from main import main


@pytest.mark.parametrize("lst", [
    "[10, 23, 4, 1, 32, 4, 5, 11, 7, 9, 8]",
    "[]",
])
def test_smooth_sort(lst):
    sorted_lst: list = ast.literal_eval(lst)
    sorted_lst.sort()
    assert main(lst) == sorted_lst


def test_smooth_sort_rand():
    n = random.randint(0, 2**8)
    rand_lst = [random.randint(0, 2 ** 32 - 1) for _ in range(n)]
    str_lst = str(rand_lst)
    rand_lst.sort()
    assert main(str_lst) == rand_lst
