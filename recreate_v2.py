# Phase: 2 | Module: Recreate v2 | Author: FeigenbaumIA-Stack
"""Reconstrói localmente artefatos mínimos do repositório.

Uso:
    python recreate_v2.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = (
    "README.md",
    "requirements.txt",
    "experiments/phase1_demo.py",
    "experiments/phase2_demo.py",
    "src/feigenbaum_mlp.py",
)


def run() -> None:
    """Valida a estrutura local esperada do workspace."""
    print("[recreate_v2] Validando estrutura do projeto...")

    missing = [rel for rel in REQUIRED_FILES if not (ROOT / rel).exists()]
    if missing:
        print("[recreate_v2] Arquivos ausentes:")
        for rel in missing:
            print(f"  - {rel}")
        raise SystemExit("[recreate_v2] Falha: estrutura incompleta.")

    print("[recreate_v2] Estrutura OK. Nada para recriar.")


if __name__ == "__main__":
    run()
