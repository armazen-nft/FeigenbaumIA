# Phase: 1 | Module: Tests | Author: FeigenbaumIA-Stack
"""Teste de sanidade para o mapa logístico."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.logistic import logistic_sequence, logistic_step


def test_logistic_step_bounds() -> None:
    """Valida que um passo permanece em [0, 1] para caso padrão."""
    x1 = logistic_step(0.5, 3.9)
    assert 0.0 <= x1 <= 1.0


def test_logistic_sequence_length() -> None:
    """Valida tamanho da sequência gerada."""
    seq = logistic_sequence(0.5, 3.9, 25)
    assert len(seq) == 25


if __name__ == "__main__":
    test_logistic_step_bounds()
    test_logistic_sequence_length()
    print("test_logistic.py: OK")
