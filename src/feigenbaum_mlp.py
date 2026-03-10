# Phase: 2 | Module: FeignbaumMLP | Author: FeigenbaumIA-Stack
"""
MLP com política de crescimento Feigenbaum.

A topologia não é fixa. A cada epoch de avaliação, camadas ocultas
bifurcam (spawn) ou são podadas segundo entropia relativa e δ.

Benchmark alvo: MNIST ou dataset sintético.
Comparar contra MLP estática de mesma capacidade inicial.
"""

from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from .constants import FEIGENBAUM_DELTA, PRUNE_THRESHOLD, SPAWN_THRESHOLD
from .enochian import EnochianEmitter, GlyphType


class FeignbaumLayer(nn.Module):
    """Camada linear com entropia monitorada e flag de vida."""

    def __init__(self, in_features: int, out_features: int, layer_id: int) -> None:
        """Inicializa camada linear monitorada."""
        super().__init__()
        self.layer_id = layer_id
        self.alive = True
        self.linear = nn.Linear(in_features, out_features)
        self._entropy: float = 0.5

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Executa forward da camada e atualiza entropia empírica."""
        if not self.alive:
            return x
        out = F.relu(self.linear(x))
        p = F.softmax(out.detach().mean(0), dim=0)
        h = -(p * (p + 1e-9).log()).sum().item()
        self._entropy = min(1.0, h / (out.shape[-1] + 1e-9) * 2)
        return out

    @property
    def entropy(self) -> float:
        """Entropia recente da camada."""
        return self._entropy


class FeignbaumMLP(nn.Module):
    """MLP cuja topologia evolui segundo a política Feigenbaum."""

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        max_hidden_layers: int = 8,
        emit: bool = True,
    ) -> None:
        """Inicializa rede dinâmica com uma camada oculta inicial."""
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.max_hidden_layers = max_hidden_layers
        self.emitter = EnochianEmitter(log=emit)
        self._layer_id_counter = 0

        self.input_layer = FeignbaumLayer(input_dim, hidden_dim, self._next_id())
        self.hidden_layers: nn.ModuleList = nn.ModuleList(
            [FeignbaumLayer(hidden_dim, hidden_dim, self._next_id())]
        )
        self.output_layer = nn.Linear(hidden_dim, output_dim)

        self.emitter.identity(0, 0, 0.5)

    def _next_id(self) -> int:
        """Gera próximo identificador de camada."""
        self._layer_id_counter += 1
        return self._layer_id_counter

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Executa forward completo da rede."""
        x = self.input_layer(x)
        for layer in self.hidden_layers:
            if layer.alive:
                x = layer(x)
        return self.output_layer(x)

    def policy_step(self) -> dict:
        """Aplica política Feigenbaum de spawn/prune nas camadas ocultas."""
        spawned, pruned = [], []
        layers_to_check = list(self.hidden_layers)

        for layer in layers_to_check:
            if not layer.alive:
                continue
            self.emitter.measure(layer.layer_id, 0, layer.entropy)

            if layer.entropy < PRUNE_THRESHOLD:
                layer.alive = False
                pruned.append(layer.layer_id)
                self.emitter.prune(layer.layer_id, 0, layer.entropy)
            elif (
                layer.entropy > SPAWN_THRESHOLD
                and len(self.hidden_layers) < self.max_hidden_layers
            ):
                new_layer = FeignbaumLayer(
                    self.hidden_dim, self.hidden_dim, self._next_id()
                )
                with torch.no_grad():
                    new_layer.linear.weight.data = (
                        layer.linear.weight.data / FEIGENBAUM_DELTA
                    )
                    new_layer.linear.bias.data = (
                        layer.linear.bias.data / FEIGENBAUM_DELTA
                    )
                self.hidden_layers.append(new_layer)
                spawned.append(new_layer.layer_id)
                self.emitter.spawn(
                    new_layer.layer_id,
                    len(self.hidden_layers),
                    layer.entropy,
                    parent_id=layer.layer_id,
                )

        alive_count = sum(1 for l in self.hidden_layers if l.alive)
        avg_entropy = sum(l.entropy for l in self.hidden_layers) / max(1, alive_count)
        self.emitter.audit(0, 0, avg_entropy)

        return {
            "alive_layers": alive_count,
            "spawned": spawned,
            "pruned": pruned,
            "token_ledger": self.emitter.stats(),
        }
