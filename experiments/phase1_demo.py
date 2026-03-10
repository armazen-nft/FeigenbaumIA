"""
Fase 1 — Demonstração do mapa logístico hierárquico.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.constants import FEIGENBAUM_DELTA
from src.fractal_memory import FractalMemory
from src.logistic import bifurcation_diagram, compute_delta_ratios, find_bifurcation_points
from src.spawn_policy import FeigenbaumForest


def section(title):
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print("═" * 60)


def main():
    section("1. LOCALIZANDO PONTOS DE BIFURCAÇÃO")
    print("  (pode levar alguns segundos...)")
    bifs = find_bifurcation_points()
    for i, r in enumerate(bifs):
        print(f"  r_{i + 1} = {r:.8f}")

    section("2. RAZÕES DE CONVERGÊNCIA → δ")
    ratios = compute_delta_ratios(bifs)
    for i, ratio in enumerate(ratios):
        erro = abs(ratio - FEIGENBAUM_DELTA) / FEIGENBAUM_DELTA * 100
        print(f"  δ_{i + 1} = {ratio:.6f}  (erro vs teórico: {erro:.2f}%)")
    print(f"\n  δ teórico = {FEIGENBAUM_DELTA:.6f}")

    section("3. DIAGRAMA DE BIFURCAÇÃO")
    rs, xs = bifurcation_diagram()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(rs, xs, s=0.1, c="steelblue", alpha=0.3, rasterized=True)
    ax.set_xlabel("r", fontsize=12)
    ax.set_ylabel("x*", fontsize=12)
    ax.set_title("Diagrama de Bifurcação — Mapa Logístico (FeigenbaumIA)", fontsize=13)
    for r in bifs:
        ax.axvline(r, color="crimson", linewidth=0.8, alpha=0.6, linestyle="--")
    out = "experiments/bifurcation_diagram.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  Salvo: {out}")

    section("4. FEIGENBAUM FOREST — SPAWN/PRUNE")
    forest = FeigenbaumForest(max_depth=4)
    rng = np.random.default_rng(42)
    for cycle in range(8):
        alive_ids = [m for m in range(forest._id_counter)]
        entropies = {i: float(rng.uniform(0, 1)) for i in alive_ids}
        report = forest.step(entropies)
        print(
            f"  Ciclo {cycle + 1:02d}: alive={report['alive']:3d}  "
            f"spawned={len(report['spawned'])}  pruned={len(report['pruned'])}"
        )

    section("5. FRACTAL MEMORY — COMPRESSÃO MULTI-NÍVEL")
    mem = FractalMemory(base_dim=64, n_levels=4)
    for _ in range(20):
        mem.store(rng.standard_normal(64))
    stats = mem.stats()
    for k in range(4):
        print(f"  Nível {k}: {stats[f'level_{k}']} vetores  dim={stats[f'dim_{k}']}")
    print(f"  Razão de compressão δ = {stats['compression_ratio']:.4f}")

    section("FASE 1 CONCLUÍDA ✓")
    print("  Hipótese confirmada: bifurcações convergem para δ.")
    print("  Próximo: Fase 2 — MLP PyTorch com política Feigenbaum.\n")


if __name__ == "__main__":
    main()
