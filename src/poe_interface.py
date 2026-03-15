# Phase: 3 | Module: PoEInterface | Author: FeigenbaumIA-Stack
"""Interface mínima para envio de eventos FeigenbaumIA ao ecossistema PoE."""

from __future__ import annotations

from dataclasses import dataclass

from .enochian import EnochianToken


@dataclass
class PoEMessage:
    """Envelope compatível com transporte assíncrono de eventos."""

    topic: str
    payload: str


class PoEInterface:
    """Adaptador simples para serialização de tokens Enochian para PoE."""

    def __init__(self, topic_prefix: str = "poe.feigenbaum") -> None:
        self.topic_prefix = topic_prefix

    def to_message(self, token: EnochianToken) -> PoEMessage:
        """Converte token em mensagem pronta para transporte externo."""
        topic = f"{self.topic_prefix}.{token.glyph.value.lower()}"
        return PoEMessage(topic=topic, payload=token.to_json())
