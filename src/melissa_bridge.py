# Phase: 3 | Module: MelissaBridge | Author: FeigenbaumIA-Stack
"""
Ponte entre FeigenbaumIA e MelissaCore.

FractalMemory (FeigenbaumIA) → MelissaCore Hot/Warm/Cold

Protocolo:
  - Nível 0 (full-res)  → HOT  (acesso imediato, sem compressão)
  - Nível 1 (dim/δ)     → WARM (compressão leve, acesso rápido)
  - Nível 2+ (dim/δ^k)  → COLD (compressão máxima, acesso lento)

Todos os estados são serializados com tokens Enochian antes de enviar.
Interface é agnóstica ao transporte: local (arquivo), socket, ou HTTP.

MelissaCore repo: https://github.com/armazen-nft/melissa-core
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal, Optional

import numpy as np

from .enochian import EnochianEmitter, EnochianToken, GlyphType
from .fractal_memory import FractalMemory

MemoryTier = Literal["HOT", "WARM", "COLD"]


class MelissaBridge:
    """Exporta estados da FractalMemory para o formato esperado pelo MelissaCore."""

    TIER_MAP = {0: "HOT", 1: "WARM"}

    def __init__(
        self,
        memory: FractalMemory,
        output_dir: str = "./melissa_bridge_output",
        emitter: Optional[EnochianEmitter] = None,
        mode: str = "local",
    ) -> None:
        """Inicializa ponte e estrutura de diretórios por tier."""
        self.memory = memory
        self.output_dir = Path(output_dir)
        self.emitter = emitter or EnochianEmitter(log=False)
        self.mode = mode
        self._setup_dirs()

    def _setup_dirs(self) -> None:
        """Cria diretórios HOT/WARM/COLD caso não existam."""
        for tier in ["HOT", "WARM", "COLD"]:
            (self.output_dir / tier).mkdir(parents=True, exist_ok=True)

    def _tier(self, level: int) -> MemoryTier:
        """Mapeia nível da memória para tier MelissaCore."""
        return self.TIER_MAP.get(level, "COLD")

    def flush(self, module_id: int = 0, tag: str = "state") -> dict:
        """Exporta todos os níveis da FractalMemory para pastas Hot/Warm/Cold."""
        summary = {}
        for level in range(self.memory.n_levels):
            tier = self._tier(level)
            vectors = self.memory.retrieve(level=level)
            if not vectors:
                continue

            payload = {
                "module_id": module_id,
                "level": level,
                "tier": tier,
                "n_vectors": len(vectors),
                "dim": int(vectors[0].shape[0]),
                "vectors": [v.tolist() for v in vectors],
                "enochian_token": self.emitter.emit(
                    EnochianToken(
                        glyph=GlyphType.DRUX,
                        module_id=module_id,
                        depth=level,
                        entropy=float(np.mean([np.std(v) for v in vectors])),
                        context=f"MelissaBridge:{tier}",
                    )
                ).to_enochian_sequence(),
            }

            fname = self.output_dir / tier / f"{tag}_level{level}.json"
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

            summary[tier] = {"file": str(fname), "n_vectors": len(vectors)}

        return summary

    def status(self) -> dict:
        """Retorna contagem de arquivos exportados por tier."""
        counts = {}
        for tier in ["HOT", "WARM", "COLD"]:
            files = list((self.output_dir / tier).glob("*.json"))
            counts[tier] = len(files)
        return counts
