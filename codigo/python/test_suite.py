"""
Suíte de Testes Obrigatória para Algoritmos de Ordenação.
Executa os cenários exigidos pelo enunciado do TP1.
"""

import random
import unittest
from typing import Callable, List, Tuple

from authorial import dpes_sort
from classical import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from oeba import oeba_sort


class BaseSortMixin:
    """Classe base contendo a bateria completa de cenários de teste."""
    sort_fn: Callable[[List], Tuple[List, int, int]]
    name: str

    def assert_sorted(self, original: List, result: List):
        self.assertEqual(len(result), len(original), f"Tamanho divergente em {self.name}")
        self.assertEqual(sorted(original), result, f"Ordenação incorreta em {self.name}")

    def test_01_empty_list(self):
        data = []
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_02_single_element(self):
        data = [42]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_03_already_sorted(self):
        data = list(range(1, 101))
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_04_strictly_reverse_sorted(self):
        data = list(range(100, 0, -1))
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_05_all_identical_elements(self):
        data = [7] * 50
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_06_many_duplicates(self):
        random.seed(42)
        data = [random.choice([1, 2, 3, 4, 5]) for _ in range(200)]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_07_negative_and_floating_point(self):
        data = [-10.5, 3.14, 0.0, -0.01, 100.2, -50.0, 2.718, 0.0, -10.5]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_08_random_uniform_small(self):
        random.seed(123)
        data = [random.randint(-1000, 1000) for _ in range(25)]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_09_random_uniform_medium(self):
        random.seed(456)
        data = [random.randint(-10000, 10000) for _ in range(1000)]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_10_almost_sorted(self):
        data = list(range(200))
        for i in (10, 50, 120, 180):
            data[i], data[i + 1] = data[i + 1], data[i]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)


class TestBubbleSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(bubble_sort)
    name = "Bubble Sort"


class TestSelectionSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(selection_sort)
    name = "Selection Sort"


class TestInsertionSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(insertion_sort)
    name = "Insertion Sort"


class TestMergeSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(merge_sort)
    name = "Merge Sort"


class TestQuickSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(quick_sort)
    name = "Quick Sort"


class TestDPESSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(dpes_sort)
    name = "DPES (Referência)"


class TestOEBASort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(oeba_sort)
    name = "OEBA (Autoral)"


if __name__ == "__main__":
    unittest.main(verbosity=2)
