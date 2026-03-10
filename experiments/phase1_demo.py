# Phase: 1 | Module: Demo | Author: FeigenbaumIA-Stack
"""Demo de fase 1: sequência logística simples."""

from __future__ import annotations

from src.constants import LOGISTIC_R_DEFAULT, LOGISTIC_X0_DEFAULT
from src.logistic import logistic_sequence


def run(n: int = 10) -> None:
    """Executa demo com ``n`` passos e imprime últimos valores."""
    values = logistic_sequence(LOGISTIC_X0_DEFAULT, LOGISTIC_R_DEFAULT, n)
    print("phase1_demo:", [round(v, 6) for v in values[-5:]])


if __name__ == "__main__":
    run()
