# Phase: 4 | Module: RecreateV2 | Author: FeigenbaumIA-Stack
"""Reconstrói artefatos mínimos da Fase 2/3 e valida pré-condições de release."""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_PATHS = [
    Path("src/enochian.py"),
    Path("src/feigenbaum_mlp.py"),
    Path("src/melissa_bridge.py"),
    Path("src/poe_interface.py"),
    Path("MANIFESTO.md"),
    Path("experiments/phase2_demo.py"),
    Path("experiments/phase3_demo.py"),
]


def validate_token(token: str) -> bool:
    """Valida formato básico de token de automação do GitHub."""
    return token.startswith("ghp_") and len(token) >= 8


def main(argv: list[str]) -> int:
    """Executa validações locais para reconstrução da release v2."""
    if len(argv) < 2:
        print("Uso: python recreate_v2.py ghp_TOKEN")
        return 1

    token = argv[1].strip()
    if not validate_token(token):
        print("Token inválido: use um token no formato ghp_***")
        return 2

    missing = [str(path) for path in REQUIRED_PATHS if not path.exists()]
    if missing:
        print("Arquivos ausentes:")
        for path in missing:
            print(f" - {path}")
        return 3

    tracked_files = [p for p in Path(".").rglob("*") if p.is_file() and ".git" not in p.parts]
    print(f"Token aceito (formato): {token[:7]}***")
    print(f"Arquivos verificados: {len(REQUIRED_PATHS)}")
    print(f"Arquivos totais no workspace: {len(tracked_files)}")
    print("recreate_v2: validação local concluída.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
