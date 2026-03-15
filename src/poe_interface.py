"""Interface mínima para coleta de métricas PoE durante os demos."""

from __future__ import annotations


class PoEInterface:
    def __init__(self) -> None:
        self.cycles = 0
        self.total_layers = 0
        self.total_entropy = 0.0

    def register_cycle(self, alive_layers: int, avg_entropy: float) -> None:
        self.cycles += 1
        self.total_layers += int(alive_layers)
        self.total_entropy += float(avg_entropy)

    def stats(self) -> dict:
        if self.cycles == 0:
            return {"cycles": 0, "avg_layers": 0.0, "avg_entropy": 0.0}
        return {
            "cycles": self.cycles,
            "avg_layers": self.total_layers / self.cycles,
            "avg_entropy": self.total_entropy / self.cycles,
        }
