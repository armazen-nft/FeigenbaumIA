"""
Memória fractal — compressão automática de estados internos.

Armazena estados em níveis de resolução decrescente (por δ).
O nível 0 é full-res. Cada nível subsequente é comprimido por fator δ.
"""

from __future__ import annotations

from typing import List

import numpy as np

from .constants import FEIGENBAUM_DELTA


class FractalMemory:
    """
    Estrutura de memória multi-resolução.
    Nível k armazena vetores comprimidos por δ^k.
    """

    def __init__(self, base_dim: int = 64, n_levels: int = 4):
        self.base_dim = base_dim
        self.n_levels = n_levels
        self.levels: List[List[np.ndarray]] = [[] for _ in range(n_levels)]

    def _dim_at_level(self, k: int) -> int:
        return max(1, int(self.base_dim / (FEIGENBAUM_DELTA**k)))

    def store(self, vector: np.ndarray) -> None:
        """Armazena vetor full-res e versões comprimidas em cada nível."""
        v = vector.flatten()[: self.base_dim]
        if len(v) < self.base_dim:
            v = np.pad(v, (0, self.base_dim - len(v)))
        self.levels[0].append(v.copy())
        for k in range(1, self.n_levels):
            dim = self._dim_at_level(k)
            compressed = v[:dim]
            self.levels[k].append(compressed)

    def retrieve(self, level: int = 0, last_n: int = 10) -> List[np.ndarray]:
        """Recupera últimos n vetores do nível especificado."""
        return self.levels[level][-last_n:]

    def stats(self) -> dict:
        sizes = {f"level_{k}": len(self.levels[k]) for k in range(self.n_levels)}
        dims = {f"dim_{k}": self._dim_at_level(k) for k in range(self.n_levels)}
        return {**sizes, **dims, "compression_ratio": FEIGENBAUM_DELTA}
