"""Testes específicos do algoritmo autoral OEBA."""

import unittest

from oeba import oeba_sort


class TestOEBASpecific(unittest.TestCase):
    """Valida decisões internas que são exclusivas da OEBA."""

    def test_lista_ordenada_dispara_corte_rapido(self):
        data = list(range(50))
        result, comps, moves = oeba_sort(data)
        self.assertEqual(data, result)
        # Em entrada ordenada, não deve explodir para ~n² comparações.
        self.assertLess(comps, 50 * 50)
        self.assertEqual(sorted(data), result)

    def test_elementos_identicos_param_cedo(self):
        data = [7] * 40
        result, _, moves = oeba_sort(data)
        self.assertEqual(data, result)
        self.assertEqual(0, moves)

    def test_dois_elementos_invertidos(self):
        result, _, moves = oeba_sort([2, 1])
        self.assertEqual([1, 2], result)
        self.assertGreaterEqual(moves, 2)

    def test_reajusta_max_quando_maximo_comeca_em_left(self):
        result, _, _ = oeba_sort([9, 2, 1, 8])
        self.assertEqual([1, 2, 8, 9], result)

    def test_parametros_tau_kappa_aceitam_override(self):
        data = [5, 1, 4, 2, 8, 0, 3]
        result, _, _ = oeba_sort(data, tau=0.5, kappa=4)
        self.assertEqual(sorted(data), result)

    def test_vazios_e_unitario(self):
        self.assertEqual([], oeba_sort([])[0])
        self.assertEqual([42], oeba_sort([42])[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
