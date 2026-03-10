"""
Política de spawn/prune de módulos neurais baseada em δ.

A cada ciclo de avaliação, calcula a entropia relativa de cada módulo.
Se H_rel > SPAWN_THRESHOLD → bifurca (cria filho).
Se H_rel < PRUNE_THRESHOLD → poda (remove módulo).
O intervalo de avaliação escala por δ a cada geração.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .constants import FEIGENBAUM_DELTA, PRUNE_THRESHOLD, SPAWN_THRESHOLD


@dataclass
class Module:
    id: int
    depth: int
    entropy: float = 0.5
    alive: bool = True
    children: List["Module"] = field(default_factory=list)
    eval_interval: int = 10

    def relative_entropy(self) -> float:
        """Normaliza entropia para [0, 1]."""
        return max(0.0, min(1.0, self.entropy))

    def should_spawn(self) -> bool:
        return self.alive and self.relative_entropy() > SPAWN_THRESHOLD

    def should_prune(self) -> bool:
        return self.alive and self.relative_entropy() < PRUNE_THRESHOLD


class FeigenbaumForest:
    """
    Floresta de módulos com política de crescimento controlada por δ.
    O intervalo de avaliação de cada geração = intervalo_pai * δ.
    """

    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth
        self._id_counter = 0
        self.roots: List[Module] = [self._new_module(depth=0)]

    def _new_module(self, depth: int, entropy: float = 0.5) -> Module:
        module = Module(
            id=self._id_counter,
            depth=depth,
            entropy=entropy,
            eval_interval=max(1, int(10 * (FEIGENBAUM_DELTA**depth))),
        )
        self._id_counter += 1
        return module

    def step(self, entropies: dict[int, float]) -> dict:
        """
        Atualiza entropias, aplica spawn/prune.
        entropies: {module_id: novo_valor_entropia}
        Retorna relatório do ciclo.
        """
        spawned, pruned = [], []

        def _process(mod: Module):
            if mod.id in entropies:
                mod.entropy = entropies[mod.id]
            if not mod.alive:
                return
            if mod.should_prune():
                mod.alive = False
                pruned.append(mod.id)
                return
            if mod.should_spawn() and mod.depth < self.max_depth:
                child_entropy = mod.entropy / FEIGENBAUM_DELTA
                child = self._new_module(depth=mod.depth + 1, entropy=child_entropy)
                mod.children.append(child)
                spawned.append(child.id)
            for child in mod.children:
                _process(child)

        for root in self.roots:
            _process(root)

        return {
            "total_modules": self._id_counter,
            "alive": self._count_alive(),
            "spawned": spawned,
            "pruned": pruned,
        }

    def _count_alive(self) -> int:
        count = 0

        def _walk(mod: Module):
            nonlocal count
            if mod.alive:
                count += 1
            for child in mod.children:
                _walk(child)

        for root in self.roots:
            _walk(root)
        return count
