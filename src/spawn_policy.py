# Phase: 2 | Module: SpawnPolicy | Author: FeigenbaumIA-Stack
"""Política de bifurcação e poda de módulos em floresta fractal."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .constants import FEIGENBAUM_DELTA, PRUNE_THRESHOLD, SPAWN_THRESHOLD
from .enochian import EnochianEmitter


@dataclass
class Module:
    """Representa módulo cognitivo individual na floresta."""

    id: int
    depth: int
    entropy: float = 0.5
    alive: bool = True
    children: List["Module"] = field(default_factory=list)
    spawns: int = 0

    def should_spawn(self) -> bool:
        return self.entropy > SPAWN_THRESHOLD

    def should_prune(self) -> bool:
        return self.entropy < PRUNE_THRESHOLD


class FeigenbaumForest:
    """Gerencia dinâmica de módulos baseada em entropia e δ."""

    def __init__(self, max_depth: int = 5, emit: bool = True) -> None:
        self.max_depth = max_depth
        self._id_counter = 0
        self.emitter = EnochianEmitter(log=emit)
        root = self._new_module(depth=0)
        self.emitter.identity(root.id, root.depth, root.entropy)
        self.roots: List[Module] = [root]

    def _new_module(self, depth: int, entropy: float = 0.5) -> Module:
        self._id_counter += 1
        return Module(id=self._id_counter, depth=depth, entropy=entropy)

    def _walk(self) -> List[Module]:
        nodes: List[Module] = []

        def _rec(mod: Module):
            nodes.append(mod)
            for c in mod.children:
                _rec(c)

        for root in self.roots:
            _rec(root)
        return nodes

    def topology_summary(self) -> dict:
        all_nodes = self._walk()
        alive = [m for m in all_nodes if m.alive]
        return {
            "total_modules": len(all_nodes),
            "alive_modules": len(alive),
            "max_depth": max((m.depth for m in alive), default=0),
            "total_spawns": sum(m.spawns for m in all_nodes),
        }

    def step(self, entropies: Dict[int, float]) -> dict:
        spawned: List[int] = []
        pruned: List[int] = []

        def _process(mod: Module) -> None:
            if mod.id in entropies:
                mod.entropy = entropies[mod.id]
                self.emitter.measure(mod.id, mod.depth, mod.entropy)
            if not mod.alive:
                return
            if mod.should_prune():
                mod.alive = False
                pruned.append(mod.id)
                self.emitter.prune(mod.id, mod.depth, mod.entropy)
                return
            if mod.should_spawn() and mod.depth < self.max_depth:
                child_entropy = mod.entropy / FEIGENBAUM_DELTA
                child = self._new_module(depth=mod.depth + 1, entropy=child_entropy)
                mod.children.append(child)
                mod.spawns += 1
                spawned.append(child.id)
                self.emitter.spawn(child.id, child.depth, child.entropy, parent_id=mod.id)
                self.emitter.connect(mod.id, child.id, mod.depth, mod.entropy)
            for c in mod.children:
                _process(c)

        for root in self.roots:
            _process(root)

        alive = [m for m in self._walk() if m.alive]
        return {
            "spawned": spawned,
            "pruned": pruned,
            "alive": len(alive),
            "max_depth": max((m.depth for m in alive), default=0),
            "avg_entropy": sum(m.entropy for m in alive) / max(1, len(alive)),
            "stats": self.emitter.stats(),
        }
