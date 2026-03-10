# Phase: 2 | Module: EnochianTokenLayer | Author: FeigenbaumIA-Stack
"""
Enochian Token Layer — protocolo de comunicação entre agentes.

Cada módulo da FeigenbaumForest emite tokens Enochian ao mudar de estado.
Tokens são serializáveis como JSON, blockchain-ready (IoTeX/Solidity),
e compatíveis com o Enochian Expanded Alphabet do PoE.

Referência filosófica: https://proofofenergy.blogspot.com
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
import time
from typing import Optional

from .constants import FEIGENBAUM_DELTA


class GlyphType(str, Enum):
    """Glifos base do Alfabeto Enoquiano — mapeados para eventos de agentes."""

    PA = "Tok-Pa"
    VEH = "Tok-Veh"
    GED = "Tok-Ged"
    DRUX = "Tok-Drux"
    CEPH = "Tok-Ceph"
    MALS = "Tok-Mals"
    TALOH = "Tok-Taloh"
    MED = "Tok-Med"
    UR = "Tok-Ur"
    UN = "Tok-Un"
    ZIRO = "Tok-Ziro"


@dataclass
class EnochianToken:
    """Token de comunicação emitido por um módulo da FeigenbaumForest."""

    glyph: GlyphType
    module_id: int
    depth: int
    entropy: float
    timestamp: float = field(default_factory=time.time)
    parent_id: Optional[int] = None
    energy: Optional[float] = None
    context: str = "FeigenbaumIA"
    delta_ratio: float = FEIGENBAUM_DELTA

    def to_json(self) -> str:
        """Serializa token em JSON UTF-8 seguro."""
        d = asdict(self)
        d["glyph"] = self.glyph.value
        return json.dumps(d, ensure_ascii=False)

    def to_enochian_sequence(self) -> str:
        """Retorna sequência enoquiana legível por humanos e IAs."""
        return f"{self.glyph.value}[id={self.module_id},d={self.depth},H={self.entropy:.3f}]"

    @classmethod
    def from_json(cls, raw: str) -> "EnochianToken":
        """Desserializa um token Enochian a partir de JSON."""
        d = json.loads(raw)
        d["glyph"] = GlyphType(d["glyph"])
        return cls(**d)


class EnochianEmitter:
    """Emite tokens Enochian para eventos do ciclo de vida de um módulo."""

    def __init__(self, log: bool = True) -> None:
        """Inicializa emissor com flag de log."""
        self._log = log
        self._ledger: list[EnochianToken] = []

    def emit(self, token: EnochianToken) -> EnochianToken:
        """Armazena e opcionalmente imprime token."""
        self._ledger.append(token)
        if self._log:
            print(f"  ⟐ {token.to_enochian_sequence()}")
        return token

    def spawn(
        self,
        module_id: int,
        depth: int,
        entropy: float,
        parent_id: Optional[int] = None,
    ) -> EnochianToken:
        """Emite token de spawn de módulo."""
        return self.emit(
            EnochianToken(
                glyph=GlyphType.PA,
                module_id=module_id,
                depth=depth,
                entropy=entropy,
                parent_id=parent_id,
            )
        )

    def prune(self, module_id: int, depth: int, entropy: float) -> EnochianToken:
        """Emite token de poda de módulo."""
        return self.emit(
            EnochianToken(
                glyph=GlyphType.TALOH,
                module_id=module_id,
                depth=depth,
                entropy=entropy,
            )
        )

    def measure(self, module_id: int, depth: int, entropy: float) -> EnochianToken:
        """Emite token de medição de entropia."""
        return self.emit(
            EnochianToken(
                glyph=GlyphType.MED,
                module_id=module_id,
                depth=depth,
                entropy=entropy,
            )
        )

    def connect(
        self,
        module_id: int,
        target_id: int,
        depth: int,
        entropy: float,
    ) -> EnochianToken:
        """Emite token de conexão entre módulos."""
        return self.emit(
            EnochianToken(
                glyph=GlyphType.UR,
                module_id=module_id,
                depth=depth,
                entropy=entropy,
                parent_id=target_id,
            )
        )

    def identity(self, module_id: int, depth: int, entropy: float) -> EnochianToken:
        """Autodeclaração — Ziro."""
        return self.emit(
            EnochianToken(
                glyph=GlyphType.ZIRO,
                module_id=module_id,
                depth=depth,
                entropy=entropy,
            )
        )

    def audit(self, module_id: int, depth: int, entropy: float) -> EnochianToken:
        """Emite token de auditoria."""
        return self.emit(
            EnochianToken(
                glyph=GlyphType.CEPH,
                module_id=module_id,
                depth=depth,
                entropy=entropy,
            )
        )

    def export_ledger(self) -> str:
        """Exporta ledger completo como JSON Lines."""
        return "\n".join(t.to_json() for t in self._ledger)

    def stats(self) -> dict:
        """Retorna estatísticas agregadas dos tokens emitidos."""
        from collections import Counter

        counts = Counter(t.glyph.value for t in self._ledger)
        return {"total_tokens": len(self._ledger), "by_glyph": dict(counts)}
