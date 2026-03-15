"""Testes — FeigenbaumForest spawn/prune."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.constants import PRUNE_THRESHOLD, SPAWN_THRESHOLD
from src.spawn_policy import FeigenbaumForest


def test_forest_initializes():
    forest = FeigenbaumForest(max_depth=3, emit=False)
    assert len(forest.roots) == 1


def test_spawn_on_high_entropy():
    forest = FeigenbaumForest(max_depth=2, emit=False)
    root = forest.roots[0]
    report = forest.step({root.id: SPAWN_THRESHOLD + 0.1})
    assert len(report["spawned"]) >= 1


def test_prune_on_low_entropy():
    forest = FeigenbaumForest(max_depth=2, emit=False)
    root = forest.roots[0]
    report = forest.step({root.id: PRUNE_THRESHOLD - 0.05})
    assert root.id in report["pruned"]
