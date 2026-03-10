"""Testes básicos — mapa logístico e política de spawn."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from src.constants import FEIGENBAUM_DELTA
from src.logistic import compute_delta_ratios, find_bifurcation_points
from src.spawn_policy import FeigenbaumForest


def test_bifurcation_ratios():
    bifs = find_bifurcation_points()
    assert len(bifs) >= 3, "Menos de 3 bifurcações encontradas"
    ratios = compute_delta_ratios(bifs)
    for ratio in ratios:
        assert abs(ratio - FEIGENBAUM_DELTA) / FEIGENBAUM_DELTA < 0.15, (
            f"Razão {ratio:.4f} muito distante de δ={FEIGENBAUM_DELTA:.4f}"
        )


def test_forest_grows():
    forest = FeigenbaumForest(max_depth=3)
    rng = np.random.default_rng(0)
    for _ in range(5):
        entropies = {i: float(rng.uniform(0.8, 1.0)) for i in range(forest._id_counter)}
        forest.step(entropies)
    assert forest._id_counter > 1, "Nenhum módulo foi spawnado"


if __name__ == "__main__":
    test_bifurcation_ratios()
    test_forest_grows()
    print("Todos os testes passaram.")
