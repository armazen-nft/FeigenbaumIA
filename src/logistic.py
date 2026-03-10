"""
Mapa logístico hierárquico — Capítulo 1 do FeigenbaumIA.

Demonstra empiricamente a convergência das razões de bifurcação
para δ ≈ 4.669, validando a hipótese central do projeto.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np


def logistic(r: float, x: float) -> float:
    """f(x) = r * x * (1 - x)."""
    return r * x * (1.0 - x)


def iterate(r: float, x0: float = 0.5, n: int = 1000, warmup: int = 500) -> np.ndarray:
    """Itera o mapa logístico e retorna os últimos (n - warmup) valores."""
    x = x0
    trajectory = []
    for i in range(n):
        x = logistic(r, x)
        if i >= warmup:
            trajectory.append(x)
    return np.array(trajectory)


def find_bifurcation_points(
    r_start: float = 2.5,
    r_end: float = 3.57,
    steps: int = 100_000,
    tol: float = 1e-6,
) -> List[float]:
    """
    Localiza os primeiros 5 pontos de bifurcação r_n onde o período dobra.
    Retorna lista de r_n ordenada.
    """
    bifurcations = []
    prev_period = 1
    r_vals = np.linspace(r_start, r_end, steps)

    for r in r_vals:
        pts = np.unique(np.round(iterate(r, n=2000, warmup=1800), decimals=6))
        period = len(pts)
        if period > prev_period and period <= 32:
            # confirma com segunda rodada
            pts2 = np.unique(np.round(iterate(r, x0=0.3, n=2000, warmup=1800), decimals=6))
            if len(pts2) == period:
                bifurcations.append(r)
                prev_period = period
                if len(bifurcations) >= 5:
                    break

    return bifurcations


def compute_delta_ratios(bifurcations: List[float]) -> List[float]:
    """
    Calcula as razões (r_{n+1} - r_n) / (r_{n+2} - r_{n+1}).
    Devem convergir para δ ≈ 4.669.
    """
    ratios = []
    for i in range(len(bifurcations) - 2):
        num = bifurcations[i + 1] - bifurcations[i]
        den = bifurcations[i + 2] - bifurcations[i + 1]
        if abs(den) > 1e-12:
            ratios.append(num / den)
    return ratios


def bifurcation_diagram(
    r_range: Tuple[float, float] = (2.5, 4.0),
    steps: int = 3000,
    last_n: int = 200,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Retorna (r_values, x_values) para plotar o diagrama de bifurcação.
    """
    r_vals = np.linspace(*r_range, steps)
    rs, xs = [], []
    for r in r_vals:
        pts = iterate(r, n=last_n + 500, warmup=500)
        rs.extend([r] * len(pts))
        xs.extend(pts.tolist())
    return np.array(rs), np.array(xs)
