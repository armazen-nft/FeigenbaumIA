"""
FeigenbaumMLP — rede neural com topologia dinâmica guiada por δ.

Diferença fundamental de uma MLP convencional:
  - MLP convencional: topologia FIXA, definida antes do treino
  - FeigenbaumMLP: topologia VIVA, evolui durante o treino via policy_step()

Regras de evolução:
  1. Filhos herdam pesos do pai divididos por δ (não são inicializados aleatoriamente)
  2. policy_step() é chamado uma vez por epoch, após o forward pass
  3. Camadas mortas permanecem no ModuleList mas são ignoradas no forward
  4. Auditoria Enochian completa de cada evento
"""

from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F
from .constants import FEIGENBAUM_DELTA, SPAWN_THRESHOLD, PRUNE_THRESHOLD
from .enochian  import EnochianEmitter


class FeigenbaumLayer(nn.Module):
    """
    Camada linear com entropia monitorada.
    A entropia é calculada como Shannon normalizada das ativações médias.
    """

    def __init__(self, in_features: int, out_features: int,
                 layer_id: int, depth: int = 0):
        super().__init__()
        self.layer_id = layer_id
        self.depth = depth
        self.alive = True
        self.age = 0
        self.spawn_count = 0
        self.linear = nn.Linear(in_features, out_features)
        self._entropy: float = 0.5

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self.alive:
            return x
        self.age += 1
        out = F.relu(self.linear(x))
        with torch.no_grad():
            avg = out.mean(0)
            p = F.softmax(avg, dim=0)
            raw_h = -(p * (p + 1e-9).log()).sum().item()
            max_h = torch.log(torch.tensor(float(avg.shape[0]))).item()
            self._entropy = float(raw_h / (max_h + 1e-9))
        return out

    @property
    def entropy(self) -> float:
        return self._entropy


class FeigenbaumMLP(nn.Module):
    """
    MLP com política de crescimento Feigenbaum.

    Uso típico:
        model = FeigenbaumMLP(input_dim=784, hidden_dim=128, output_dim=10)
        for epoch in range(epochs):
            for xb, yb in loader:
                loss = criterion(model(xb), yb)
                loss.backward(); opt.step(); opt.zero_grad()
            report = model.policy_step()
    """

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int,
                 max_hidden_layers: int = 12, min_hidden_layers: int = 1,
                 emit: bool = True, context: str = "FeigenbaumMLP"):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.max_hidden_layers = max_hidden_layers
        self.min_hidden_layers = min_hidden_layers
        self.emitter = EnochianEmitter(log=emit, context=context)
        self._layer_id_counter = 0
        self._epoch = 0

        self.input_layer = FeigenbaumLayer(input_dim, hidden_dim, self._next_id(), depth=0)
        self.hidden_layers: nn.ModuleList = nn.ModuleList([
            FeigenbaumLayer(hidden_dim, hidden_dim, self._next_id(), depth=1)
        ])
        self.output_layer = nn.Linear(hidden_dim, output_dim)

        self.emitter.identity(0, 0, 0.5)
        self.emitter.spawn(self.hidden_layers[0].layer_id, 1, 0.5)

    def _next_id(self) -> int:
        self._layer_id_counter += 1
        return self._layer_id_counter

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.input_layer(x)
        for layer in self.hidden_layers:
            if layer.alive:
                x = layer(x)
        return self.output_layer(x)

    def policy_step(self) -> dict:
        """Aplica política Feigenbaum. Chamar uma vez por epoch."""
        self._epoch += 1
        spawned, pruned = [], []

        for layer in list(self.hidden_layers):
            if not layer.alive:
                continue
            self.emitter.measure(layer.layer_id, layer.depth, layer.entropy)
            alive_count = sum(1 for l in self.hidden_layers if l.alive)

            if layer.entropy < PRUNE_THRESHOLD and alive_count > self.min_hidden_layers:
                layer.alive = False
                pruned.append(layer.layer_id)
                self.emitter.prune(layer.layer_id, layer.depth, layer.entropy)

            elif layer.entropy > SPAWN_THRESHOLD and alive_count < self.max_hidden_layers:
                new_layer = FeigenbaumLayer(
                    self.hidden_dim, self.hidden_dim,
                    self._next_id(), depth=layer.depth + 1,
                )
                with torch.no_grad():
                    new_layer.linear.weight.data = (
                        layer.linear.weight.data.clone() / FEIGENBAUM_DELTA
                    )
                    new_layer.linear.bias.data = (
                        layer.linear.bias.data.clone() / FEIGENBAUM_DELTA
                    )
                self.hidden_layers.append(new_layer)
                layer.spawn_count += 1
                spawned.append(new_layer.layer_id)
                self.emitter.spawn(
                    new_layer.layer_id, new_layer.depth,
                    layer.entropy / FEIGENBAUM_DELTA, parent_id=layer.layer_id,
                )
                self.emitter.connect(
                    layer.layer_id, new_layer.layer_id,
                    layer.depth, layer.entropy,
                )

        alive_count = sum(1 for l in self.hidden_layers if l.alive)
        avg_h = sum(l.entropy for l in self.hidden_layers if l.alive) / max(1, alive_count)
        self.emitter.audit(0, 0, avg_h)

        return {
            "epoch": self._epoch,
            "alive_layers": alive_count,
            "total_layers": len(self.hidden_layers),
            "spawned": spawned,
            "pruned": pruned,
            "avg_entropy": avg_h,
            "token_stats": self.emitter.stats(),
        }

    def topology_info(self) -> dict:
        alive = [l for l in self.hidden_layers if l.alive]
        return {
            "alive_layers": len(alive),
            "total_layers": len(self.hidden_layers),
            "depths": [l.depth for l in alive],
            "entropies": [round(l.entropy, 4) for l in alive],
            "total_params": sum(p.numel() for p in self.parameters()),
            "epoch": self._epoch,
        }
