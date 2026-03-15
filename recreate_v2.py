#!/usr/bin/env python3
"""FeigenbaumIA — recreate_v2.py
Uso: python recreate_v2.py <GITHUB_TOKEN>

Sincroniza os arquivos deste repositório para `armazen-nft/FeigenbaumIA` via API GitHub.
"""

from __future__ import annotations

import base64
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = "armazen-nft/FeigenbaumIA"
BRANCH = "main"
API = "https://api.github.com"

PATHS = [
    "requirements.txt",
    "setup.py",
    ".github/workflows/ci.yml",
    "README.md",
    "PAPER.md",
    "MANIFESTO.md",
    "docs/ARCHITECTURE.md",
    "src/__init__.py",
    "src/constants.py",
    "src/logistic.py",
    "src/spawn_policy.py",
    "src/fractal_memory.py",
    "src/enochian.py",
    "src/feigenbaum_mlp.py",
    "src/melissa_bridge.py",
    "src/poe_interface.py",
    "experiments/phase1_demo.py",
    "experiments/phase2_demo.py",
    "experiments/phase3_demo.py",
    "tests/__init__.py",
    "tests/test_logistic.py",
    "tests/test_enochian.py",
    "tests/test_fractal_memory.py",
    "tests/test_spawn_policy.py",
]


def gh(token: str, method: str, path: str, body: dict | None = None):
    req = urllib.request.Request(f"{API}{path}", method=method)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github.v3+json")
    data = json.dumps(body).encode() if body else None
    try:
        with urllib.request.urlopen(req, data=data) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code}: {exc.read().decode()[:200]}")
        return None


def get_sha(token: str, path: str) -> str | None:
    result = gh(token, "GET", f"/repos/{REPO}/contents/{path}")
    return result.get("sha") if result else None


def push_file(token: str, path: str) -> None:
    content = Path(path).read_text(encoding="utf-8")
    body = {
        "message": f"feat: FeigenbaumIA v2 — {path}",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": BRANCH,
    }
    sha = get_sha(token, path)
    if sha:
        body["sha"] = sha
    ok = gh(token, "PUT", f"/repos/{REPO}/contents/{path}", body)
    print(("✓" if ok else "✗"), path)


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python recreate_v2.py <GITHUB_TOKEN>")
        sys.exit(1)
    token = sys.argv[1].strip()
    if not gh(token, "GET", "/user"):
        print("Token inválido ou sem acesso.")
        sys.exit(1)

    for idx, path in enumerate(PATHS, start=1):
        push_file(token, path)
        if idx % 5 == 0:
            time.sleep(0.4)

    print(f"✅ {len(PATHS)} arquivos enviados para {REPO}.")


if __name__ == "__main__":
    main()
