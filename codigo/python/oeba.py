"""
OEBA — Ordenação por Extremos Bidirecionais Adaptativa

Algoritmo autoral (adaptação estrutural profunda de Selection Min-Max + Insertion).

Raciocínio projetual:
1. Em cada passo, localiza mínimo e máximo no intervalo ativo [L, R] em uma varredura.
2. Fixa o mínimo em A[L] e o máximo em A[R], encolhendo o intervalo.
3. Se todos os elementos do intervalo forem iguais, encerra (já ordenado).
4. Twist autoral: mede a fração de inversões adjacentes no miolo.
   Se a desordem for <= tau OU o miolo tiver tamanho <= kappa, finaliza com Insertion Sort.
"""

from typing import Any, List, Tuple

# Parâmetros de projeto (justificados empiricamente no relatório)
DEFAULT_TAU = 0.15
DEFAULT_KAPPA = 16


def oeba_sort(
    arr: List[Any],
    tau: float = DEFAULT_TAU,
    kappa: int = DEFAULT_KAPPA,
) -> Tuple[List[Any], int, int]:
    """
    Ordenação por Extremos Bidirecionais Adaptativa (OEBA).

    Retorna:
        (lista_ordenada, comparacoes, movimentacoes)
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a, 0, 0

    comps = 0
    moves = 0
    left = 0
    right = n - 1

    def insertion_range(lo: int, hi: int) -> None:
        nonlocal comps, moves
        for i in range(lo + 1, hi + 1):
            key = a[i]
            moves += 1
            j = i - 1
            while j >= lo:
                comps += 1
                if a[j] > key:
                    a[j + 1] = a[j]
                    moves += 1
                    j -= 1
                else:
                    break
            a[j + 1] = key
            moves += 1

    while left < right:
        size = right - left + 1
        if size <= kappa:
            insertion_range(left, right)
            break

        min_idx = left
        max_idx = left
        for i in range(left + 1, right + 1):
            comps += 1
            if a[i] < a[min_idx]:
                min_idx = i
            comps += 1
            if a[i] > a[max_idx]:
                max_idx = i

        comps += 1
        if a[min_idx] == a[max_idx]:
            # Intervalo homogêneo: já está ordenado.
            break

        # Posiciona extremos nas bordas, tratando colisão de índices.
        if min_idx == right and max_idx == left:
            a[left], a[right] = a[right], a[left]
            moves += 2
        else:
            if min_idx != left:
                a[left], a[min_idx] = a[min_idx], a[left]
                moves += 2
                if max_idx == left:
                    max_idx = min_idx
            if max_idx != right:
                a[right], a[max_idx] = a[max_idx], a[right]
                moves += 2

        left += 1
        right -= 1

        if left >= right:
            break

        # Mede desordem adjacente no miolo remanescente.
        adjacent_pairs = right - left
        if adjacent_pairs <= 0:
            break

        inversions = 0
        for i in range(left, right):
            comps += 1
            if a[i] > a[i + 1]:
                inversions += 1

        disorder = inversions / adjacent_pairs
        if disorder <= tau:
            insertion_range(left, right)
            break

    return a, comps, moves
