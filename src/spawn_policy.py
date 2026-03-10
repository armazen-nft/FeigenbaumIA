# Phase: 2 | Module: SpawnPolicy | Author: FeigenbaumIA-Stack
"""Política de bifurcação e poda de módulos em floresta fractal."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .constants import FEIGENBAUM_DELTA, PRUNE_THRESHOLD, SPAWN_THRESHOLD
from .enochian import EnochianEmitter, GlyphType


@dataclass
class Module:
    """Representa módulo cognitivo individual na floresta."""

    id: int
    depth: int
    entropy: float = 0.5
    alive: bool = True
    children: List["Module"] = field(default_factory=list)

    def should_spawn(self) -> bool:
        """Indica se módulo deve bifurcar."""
        return self.entropy > SPAWN_THRESHOLD

    def should_prune(self) -> bool:
        """Indica se módulo deve ser podado."""
        return self.entropy < PRUNE_THRESHOLD


class FeigenbaumForest:
    """Gerencia dinâmica de módulos baseada em entropia e δ."""

    def __init__(self, max_depth: int = 5, emit: bool = True) -> None:
        """Inicializa floresta com módulo raiz."""
        self.max_depth = max_depth
        self._id_counter = 0
        self.emitter = EnochianEmitter(log=emit)
        root = self._new_module(depth=0)
        self.emitter.identity(root.id, root.depth, root.entropy)
        self.roots: List[Module] = [root]

    def _new_module(self, depth: int, entropy: float = 0.5) -> Module:
        """Cria novo módulo com identificador incremental."""
        self._id_counter += 1
        return Module(id=self._id_counter, depth=depth, entropy=entropy)

    def step(self, entropies: Dict[int, float]) -> dict:
        """Processa um ciclo da floresta com atualização de entropias."""
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
                spawned.append(child.id)
                self.emitter.spawn(child.id, child.depth, child.entropy, parent_id=mod.id)
                self.emitter.connect(mod.id, child.id, mod.depth, mod.entropy)
            for c in mod.children:
                _process(c)

        for root in self.roots:
            _process(root)

        return {"spawned": spawned, "pruned": pruned, "stats": self.emitter.stats()}
