# Phase: 1 | Module: FractalMemory | Author: FeigenbaumIA-Stack
"""Memória fractal com compressão progressiva por níveis."""

from __future__ import annotations

from typing import Dict, List

import numpy as np

from .constants import FEIGENBAUM_DELTA


class FractalMemory:
    """Armazena vetores em níveis com redução de dimensionalidade por δ."""

    def __init__(self, base_dim: int = 64, n_levels: int = 3) -> None:
        self.base_dim = base_dim
        self.n_levels = n_levels
        self._store: Dict[int, List[np.ndarray]] = {i: [] for i in range(n_levels)}

    def _target_dim(self, level: int) -> int:
        return max(1, int(round(self.base_dim / (FEIGENBAUM_DELTA ** level))))

    def push(self, vector: np.ndarray) -> None:
        self.store(vector)

    def store(self, vector: np.ndarray) -> None:
        if vector.ndim != 1:
            raise ValueError("vector must be 1D")
        for level in range(self.n_levels):
            d = self._target_dim(level)
            compressed = vector[:d].astype(np.float32, copy=False)
            self._store[level].append(compressed)

    def retrieve(self, level: int = 0) -> List[np.ndarray]:
        if level not in self._store:
            return []
        return list(self._store[level])

    def reconstruct(self, level: int = 0) -> np.ndarray:
        vectors = self.retrieve(level)
        if not vectors:
            return np.zeros(self.base_dim, dtype=np.float32)
        v = vectors[-1]
        out = np.zeros(self.base_dim, dtype=np.float32)
        out[: min(len(v), self.base_dim)] = v[: self.base_dim]
        return out

    def stats(self) -> dict:
        tiers = {0: "HOT", 1: "WARM"}
        data = {}
        for level in range(self.n_levels):
            dim = self._target_dim(level)
            data[f"level_{level}"] = {
                "tier": tiers.get(level, "COLD"),
                "dim": dim,
                "n_entries": len(self._store[level]),
                "compression": self.base_dim / max(1, dim),
            }
        return data
