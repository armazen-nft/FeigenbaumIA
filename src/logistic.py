# Phase: 1 | Module: Logistic | Author: FeigenbaumIA-Stack
"""Implementações utilitárias do mapa logístico."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np


def logistic_step(x: float, r: float) -> float:
    """Executa um único passo do mapa logístico x_{n+1}=r*x_n*(1-x_n)."""
    return r * x * (1.0 - x)


def logistic_sequence(x0: float, r: float, n: int) -> List[float]:
    """Gera sequência logística de tamanho ``n`` a partir de ``x0``."""
    values: List[float] = [x0]
    for _ in range(max(0, n - 1)):
        values.append(logistic_step(values[-1], r))
    return values


def iterate(r: float, x0: float = 0.5, n: int = 1000, discard: int = 100) -> np.ndarray:
    """Itera o mapa logístico e retorna apenas a cauda após transiente."""
    x = x0
    out = []
    for i in range(n):
        x = logistic_step(x, r)
        if i >= discard:
            out.append(x)
    return np.array(out, dtype=np.float64)


def lyapunov_exponent(r: float, x0: float = 0.5, n: int = 2000, discard: int = 200) -> float:
    """Calcula expoente de Lyapunov para parâmetro ``r``."""
    x = x0
    acc = 0.0
    count = 0
    for i in range(n):
        x = logistic_step(x, r)
        deriv = abs(r * (1.0 - 2.0 * x)) + 1e-12
        if i >= discard:
            acc += np.log(deriv)
            count += 1
    return float(acc / max(1, count))


def bifurcation_diagram(r_range: Tuple[float, float] = (2.5, 4.0), r_steps: int = 2000, last_n: int = 100):
    """Retorna pontos (r, x*) para plot de bifurcação."""
    rs = np.linspace(r_range[0], r_range[1], r_steps)
    out_r = []
    out_x = []
    for r in rs:
        xs = iterate(r, n=1200, discard=1200 - last_n)
        out_r.extend([r] * len(xs))
        out_x.extend(xs.tolist())
    return np.array(out_r), np.array(out_x)


def find_bifurcation_points() -> List[float]:
    """Retorna aproximações conhecidas dos primeiros pontos de bifurcação."""
    return [3.0, 3.449489743, 3.544090359, 3.564407266, 3.5687594]


def compute_delta_ratios(bifs: List[float]) -> List[float]:
    """Calcula razões δ_n usando sequência de pontos de bifurcação."""
    ratios: List[float] = []
    for i in range(len(bifs) - 2):
        num = bifs[i + 1] - bifs[i]
        den = bifs[i + 2] - bifs[i + 1]
        if den != 0:
            ratios.append(num / den)
    return ratios
