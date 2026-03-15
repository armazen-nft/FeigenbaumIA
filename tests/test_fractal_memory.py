"""Testes — FractalMemory."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.constants import FEIGENBAUM_DELTA
from src.fractal_memory import FractalMemory


def test_target_dim_progressive_compression():
    mem = FractalMemory(base_dim=128, n_levels=4)
    dims = [mem._target_dim(k) for k in range(4)]
    assert dims[0] == 128
    assert dims[1] == max(1, int(round(128 / FEIGENBAUM_DELTA)))
    assert dims[0] > dims[1] > dims[2] >= dims[3]


def test_push_and_retrieve_per_level():
    mem = FractalMemory(base_dim=32, n_levels=3)
    v = np.arange(32, dtype=np.float32)
    mem.push(v)
    for level in range(3):
        values = mem.retrieve(level)
        assert len(values) == 1
        assert values[0].shape[0] == mem._target_dim(level)
