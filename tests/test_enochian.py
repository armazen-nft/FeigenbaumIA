"""Testes — Enochian Token Layer."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.enochian import EnochianEmitter, EnochianToken, GlyphType


def test_emit_and_ledger():
    em = EnochianEmitter(log=False)
    em.identity(0, 0, 0.5)
    em.spawn(1, 1, 0.8, parent_id=0)
    em.measure(1, 1, 0.82)
    em.prune(2, 2, 0.05)
    assert em.stats()["total_tokens"] == 4


def test_token_serialization():
    token = EnochianToken(glyph=GlyphType.PA, module_id=7, depth=2, entropy=0.73)
    raw = token.to_json()
    back = EnochianToken.from_json(raw)
    assert back.glyph == GlyphType.PA
    assert back.module_id == 7


def test_ledger_json_lines():
    em = EnochianEmitter(log=False)
    for i in range(3):
        em.measure(i, 0, float(i) / 3)
    for line in em.export_ledger().splitlines():
        obj = json.loads(line)
        assert "glyph" in obj
