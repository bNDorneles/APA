"""
Framework de Benchmarking e Comparação de Algoritmos de Ordenação.
Gera tabelas estatísticas em Markdown e gráficos comparativos PNG.
"""

import argparse
from collections import defaultdict
import os
import random
import time
from typing import Callable, Dict, List, Tuple

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from authorial import dpes_sort
from classical import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from oeba import oeba_sort


def generate_dataset(n: int, distribution: str) -> List[int]:
    if distribution == "random":
        return [random.randint(0, 10 * n) for _ in range(n)]
    elif distribution == "sorted":
        return list(range(n))
    elif distribution == "reverse":
        return list(range(n, 0, -1))
    elif distribution == "duplicates":
        return [random.choice([1, 2, 3, 5, 8]) for _ in range(n)]
    elif distribution == "almost_sorted":
        arr = list(range(n))
        swaps = max(1, n // 20)
        for _ in range(swaps):
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    else:
        raise ValueError(f"Distribuição desconhecida: {distribution}")


def run_benchmark(
    algorithms: Dict[str, Callable[[List], Tuple[List, int, int]]],
    sizes: List[int],
    distributions: List[str],
    trials: int = 3,
) -> Dict[str, Dict[str, Dict[int, Dict[str, float]]]]:
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    for dist in distributions:
        print(f"\n[Benchmark] distribuição: [{dist.upper()}]")
        for size in sizes:
            print(f"  -> N = {size}...")
            datasets = [generate_dataset(size, dist) for _ in range(trials)]

            for name, fn in algorithms.items():
                if (
                    size > 1500
                    and name in ("Bubble Sort", "Selection Sort", "Insertion Sort", "OEBA (Autoral)")
                    and dist in ("random", "reverse")
                ):
                    continue

                times = []
                comps = []
                moves = []

                for data in datasets:
                    data_copy = list(data)
                    start = time.perf_counter()
                    res, c, m = fn(data_copy)
                    elapsed_ms = (time.perf_counter() - start) * 1000.0
                    assert res == sorted(data), f"Erro de ordenação em {name}!"
                    times.append(elapsed_ms)
                    comps.append(c)
                    moves.append(m)

                results[dist][name][size] = {
                    "time_ms": sum(times) / len(times),
                    "comps": sum(comps) / len(comps),
                    "moves": sum(moves) / len(moves),
                }

    return results


def print_markdown_summary(results: dict, sizes: List[int]):
    for dist, algs in results.items():
        print(f"\n### Resultados: Distribuição `{dist}` (Tempo em ms)")
        header = "| Algoritmo | " + " | ".join(f"N={s}" for s in sizes) + " |"
        sep = "| :--- | " + " | ".join(":---:" for _ in sizes) + " |"
        print(header)
        print(sep)
        for alg_name, size_data in algs.items():
            row = [alg_name]
            for s in sizes:
                if s in size_data:
                    row.append(f"{size_data[s]['time_ms']:.3f} ms")
                else:
                    row.append("-")
            print("| " + " | ".join(row) + " |")


def save_markdown_tables(results: dict, sizes: List[int], output_path: str):
    lines = ["# Tabelas de benchmark (TP1 - OEBA)", ""]
    for dist, algs in results.items():
        lines.append(f"## {dist}")
        lines.append("")
        lines.append("### Tempo (ms)")
        lines.append("| Algoritmo | " + " | ".join(f"N={s}" for s in sizes) + " |")
        lines.append("| :--- | " + " | ".join(":---:" for _ in sizes) + " |")
        for alg_name, size_data in algs.items():
            row = [alg_name]
            for s in sizes:
                row.append(f"{size_data[s]['time_ms']:.3f}" if s in size_data else "-")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")
        lines.append("### Comparações")
        lines.append("| Algoritmo | " + " | ".join(f"N={s}" for s in sizes) + " |")
        lines.append("| :--- | " + " | ".join(":---:" for _ in sizes) + " |")
        for alg_name, size_data in algs.items():
            row = [alg_name]
            for s in sizes:
                row.append(f"{size_data[s]['comps']:.0f}" if s in size_data else "-")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Tabelas salvas em: {output_path}")


def plot_benchmark_results(results: dict, output_path: str = "benchmark_results.png"):
    if not HAS_MATPLOTLIB:
        print("matplotlib não instalado; pulando gráfico.")
        return

    distributions = list(results.keys())
    fig, axes = plt.subplots(len(distributions), 2, figsize=(14, 4 * len(distributions)))
    if len(distributions) == 1:
        axes = [axes]

    for idx, dist in enumerate(distributions):
        ax_time = axes[idx][0]
        ax_comps = axes[idx][1]
        for alg_name, size_map in results[dist].items():
            sizes = sorted(size_map.keys())
            times = [size_map[s]["time_ms"] for s in sizes]
            comps = [size_map[s]["comps"] for s in sizes]
            ax_time.plot(sizes, times, marker="o", label=alg_name)
            ax_comps.plot(sizes, comps, marker="s", label=alg_name)

        ax_time.set_title(f"Tempo (ms) - [{dist}]")
        ax_time.set_xlabel("N")
        ax_time.set_ylabel("ms")
        ax_time.grid(True, linestyle="--", alpha=0.6)
        ax_time.legend(fontsize=7)

        ax_comps.set_title(f"Comparações - [{dist}]")
        ax_comps.set_xlabel("N")
        ax_comps.set_ylabel("comps")
        ax_comps.grid(True, linestyle="--", alpha=0.6)
        ax_comps.legend(fontsize=7)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=150)
    print(f"Gráfico salvo em: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Benchmark TP1 APA")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--plot", type=str, default="../images/benchmark_results.png")
    parser.add_argument(
        "--tables",
        type=str,
        default="../relatorio/benchmark_tabelas.md",
        help="Caminho para salvar tabelas Markdown",
    )
    args = parser.parse_args()

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "OEBA (Autoral)": oeba_sort,
        "DPES (Referência)": dpes_sort,
    }

    sizes = [10, 50, 100, 250, 500, 1000]
    distributions = ["random", "sorted", "reverse", "duplicates", "almost_sorted"]

    random.seed(42)
    results = run_benchmark(algorithms, sizes, distributions, trials=args.trials)
    print_markdown_summary(results, sizes)
    save_markdown_tables(results, sizes, args.tables)
    plot_benchmark_results(results, args.plot)


if __name__ == "__main__":
    main()
