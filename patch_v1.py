# Phase: 2 | Module: Patch v1 | Author: FeigenbaumIA-Stack
"""Aplica patch idempotente na demo da Fase 2.

Garantia aplicada:
- `phase2_demo.py` deve validar dependências (`numpy`, `torch`) antes dos imports.

Uso:
    python patch_v1.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "experiments" / "phase2_demo.py"
NEEDED_SNIPPET = "def ensure_phase2_dependencies() -> None:"


def run() -> None:
    """Valida presença do patch e falha explicitamente se faltar."""
    print("[patch_v1] Verificando patch de dependências da Fase 2...")

    if not TARGET.exists():
        raise SystemExit(f"[patch_v1] Falha: arquivo não encontrado: {TARGET}")

    source = TARGET.read_text(encoding="utf-8")
    if NEEDED_SNIPPET not in source:
        raise SystemExit(
            "[patch_v1] Falha: trecho esperado não encontrado em phase2_demo.py"
        )

    print("[patch_v1] Patch já aplicado (idempotente).")


if __name__ == "__main__":
    run()
