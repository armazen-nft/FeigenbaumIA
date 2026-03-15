"""Fase 3 — Pipeline: FeigenbaumForest → FractalMemory → MelissaBridge → PoE."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.fractal_memory import FractalMemory
from src.melissa_bridge import MelissaBridge
from src.poe_interface import PoEInterface
from src.spawn_policy import FeigenbaumForest


def _walk(mod):
    stack = [mod]
    while stack:
        node = stack.pop()
        yield node
        stack.extend(node.children)


def main(cycles: int = 10) -> None:
    rng = np.random.default_rng(0)
    forest = FeigenbaumForest(max_depth=3, emit=False)
    memory = FractalMemory(base_dim=128, n_levels=3)
    bridge = MelissaBridge(memory, output_dir="./melissa_output", mode="local")
    poe = PoEInterface()

    for cycle in range(1, cycles + 1):
        nodes = list(_walk(forest.roots[0]))
        alive_nodes = [n for n in nodes if n.alive]
        entropies = {m.id: float(rng.uniform(0.05, 0.95)) for m in alive_nodes}
        report = forest.step(entropies)

        for m in alive_nodes:
            memory.push(rng.standard_normal(128).astype(np.float32))

        avg_entropy = float(np.mean(list(entropies.values()))) if entropies else 0.0
        poe.register_cycle(alive_layers=len(alive_nodes), avg_entropy=avg_entropy, module_id=0)

        if cycle % 5 == 0:
            summary = bridge.flush(module_id=0, tag=f"forest_cycle{cycle}")
            print(f"Ciclo {cycle}: flush tiers={list(summary.keys())} spawned={len(report['spawned'])}")

    print("Status bridge:", bridge.status())
    print("Stats PoE:", poe.stats())


if __name__ == "__main__":
    main()
