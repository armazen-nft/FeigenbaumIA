# Phase: 1 | Module: FractalMemory | Author: FeigenbaumIA-Stack
"""Memória fractal com compressão progressiva por níveis."""

from __future__ import annotations

from typing import Dict, List

import numpy as np

from .constants import FEIGENBAUM_DELTA


class FractalMemory:
    """Armazena vetores em níveis com redução de dimensionalidade por δ."""

    def __init__(self, base_dim: int = 64, n_levels: int = 3) -> None:
        """Inicializa memória com ``n_levels`` e dimensão base ``base_dim``."""
        self.base_dim = base_dim
        self.n_levels = n_levels
        self._store: Dict[int, List[np.ndarray]] = {i: [] for i in range(n_levels)}

    def _target_dim(self, level: int) -> int:
        """Retorna dimensão esperada do nível."""
        return max(1, int(round(self.base_dim / (FEIGENBAUM_DELTA ** level))))

    def push(self, vector: np.ndarray) -> None:
        """Insere vetor em todos os níveis usando truncamento simples."""
        if vector.ndim != 1:
            raise ValueError("vector must be 1D")
        for level in range(self.n_levels):
            d = self._target_dim(level)
            compressed = vector[:d].astype(np.float32, copy=False)
            self._store[level].append(compressed)

    def retrieve(self, level: int = 0) -> List[np.ndarray]:
        """Recupera todos os vetores de um nível."""
        if level not in self._store:
            return []
        return list(self._store[level])
