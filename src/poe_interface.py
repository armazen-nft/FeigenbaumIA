"""PoE Interface — camada de integração com o Proof of Energy."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import List, Optional

from .constants import FEIGENBAUM_DELTA
from .enochian import EnochianEmitter, EnochianToken


@dataclass
class EnergyReading:
    sensor_id: str
    watts: float
    timestamp: float
    location: str = "Piraquara-BR"
    renewable: bool = False


@dataclass
class PoETransaction:
    token: EnochianToken
    energy_reading: EnergyReading
    reward: float
    validated: bool = False

    def to_dict(self) -> dict:
        return {
            "token": self.token.to_dict(),
            "energy_watt": self.energy_reading.watts,
            "reward": self.reward,
            "validated": self.validated,
            "timestamp": self.energy_reading.timestamp,
        }


class PoEInterface:
    REWARD_CONSTANT = 0.001

    def __init__(self, sensor_id: str = "feigenbaum-node-01", emitter: Optional[EnochianEmitter] = None):
        self.sensor_id = sensor_id
        self.emitter = emitter or EnochianEmitter(log=False)
        self._transactions: List[PoETransaction] = []
        self._total_energy = 0.0
        self._total_reward = 0.0

    def simulate_reading(self, alive_layers: int, avg_entropy: float, base_watts: float = 150.0) -> EnergyReading:
        watts = base_watts * (1 + alive_layers * 0.1) * (0.5 + avg_entropy)
        return EnergyReading(
            sensor_id=self.sensor_id,
            watts=round(watts, 2),
            timestamp=time.time(),
            renewable=True,
        )

    def register_cycle(self, alive_layers: int, avg_entropy: float, module_id: int = 0) -> PoETransaction:
        reading = self.simulate_reading(alive_layers, avg_entropy)
        reward = (
            self.REWARD_CONSTANT
            * reading.watts
            * (1.0 - avg_entropy)
            * FEIGENBAUM_DELTA
        )
        token = self.emitter.flow(
            module_id=module_id,
            depth=alive_layers,
            entropy=avg_entropy,
            energy=reading.watts,
        )
        tx = PoETransaction(token=token, energy_reading=reading, reward=round(reward, 6), validated=True)
        self._transactions.append(tx)
        self._total_energy += reading.watts
        self._total_reward += reward
        return tx

    def stats(self) -> dict:
        return {
            "total_transactions": len(self._transactions),
            "total_energy_wh": round(self._total_energy / 3600, 4),
            "total_reward": round(self._total_reward, 6),
            "avg_reward_per_tx": round(self._total_reward / max(1, len(self._transactions)), 6),
        }

    def export_transactions(self) -> str:
        return "\n".join(json.dumps(tx.to_dict(), ensure_ascii=False) for tx in self._transactions)
