# Phase: 3 | Module: Demo | Author: FeigenbaumIA-Stack
"""Demonstra integração FractalMemory -> MelissaBridge -> PoEInterface."""

from __future__ import annotations

import numpy as np

from src.enochian import EnochianToken, GlyphType
from src.fractal_memory import FractalMemory
from src.melissa_bridge import MelissaBridge
from src.poe_interface import PoEInterface


def run_demo() -> None:
    """Executa fluxo mínimo da fase 3 em modo local."""
    memory = FractalMemory(base_dim=32, levels=3)
    vec = np.random.rand(32).astype(np.float32)
    memory.store(vec)

    bridge = MelissaBridge(memory=memory, output_dir="./melissa_bridge_output")
    summary = bridge.flush(module_id=42, tag="phase3")

    token = EnochianToken(glyph=GlyphType.CEPH, module_id=42, depth=0, entropy=0.42)
    envelope = PoEInterface().to_message(token)

    print("phase3_demo summary:", summary)
    print("phase3_demo message topic:", envelope.topic)


if __name__ == "__main__":
    run_demo()
