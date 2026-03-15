# Phase: 3 | Module: Tests | Author: FeigenbaumIA-Stack
"""Testes da integração básica da Fase 3."""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.enochian import EnochianToken, GlyphType
from src.poe_interface import PoEInterface


def test_poe_interface_serialization() -> None:
    """Valida serialização de token para envelope PoE."""
    token = EnochianToken(glyph=GlyphType.PA, module_id=1, depth=0, entropy=0.1)
    msg = PoEInterface().to_message(token)

    assert msg.topic.startswith("poe.feigenbaum")
    payload = json.loads(msg.payload)
    assert payload["glyph"] == GlyphType.PA.value
