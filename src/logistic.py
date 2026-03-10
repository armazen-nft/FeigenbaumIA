# Phase: 1 | Module: Logistic | Author: FeigenbaumIA-Stack
"""Implementações utilitárias do mapa logístico."""

from __future__ import annotations

from typing import List


def logistic_step(x: float, r: float) -> float:
    """Executa um único passo do mapa logístico x_{n+1}=r*x_n*(1-x_n)."""
    return r * x * (1.0 - x)


def logistic_sequence(x0: float, r: float, n: int) -> List[float]:
    """Gera sequência logística de tamanho ``n`` a partir de ``x0``."""
    values: List[float] = [x0]
    for _ in range(max(0, n - 1)):
        values.append(logistic_step(values[-1], r))
    return values
