# Phase: 2 | Module: Demo | Author: FeigenbaumIA-Stack
"""
Fase 2 — Demo: FeignbaumMLP em dataset sintético.

Compara FeignbaumMLP (topologia dinâmica) vs MLP estática equivalente.
Métricas: accuracy, n_params, n_alive_layers, tokens emitidos.

Rode: python experiments/phase2_demo.py
"""

from __future__ import annotations

import importlib.util
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def ensure_phase2_dependencies() -> None:
    """Valida dependências opcionais da demo antes dos imports pesados."""
    missing = [
        dep
        for dep in ("numpy", "torch")
        if importlib.util.find_spec(dep) is None
    ]
    if missing:
        deps = ", ".join(missing)
        raise SystemExit(
            "Dependências ausentes para phase2_demo.py: "
            f"{deps}. Instale requirements.txt para executar o benchmark."
        )


ensure_phase2_dependencies()

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from src.feigenbaum_mlp import FeignbaumMLP


def make_dataset(n: int = 2000, d: int = 64, classes: int = 4) -> tuple[TensorDataset, TensorDataset]:
    """Cria dataset sintético com split treino/validação."""
    rng = np.random.default_rng(42)
    x = rng.standard_normal((n, d)).astype(np.float32)
    y = rng.integers(0, classes, n).astype(np.int64)
    split = int(n * 0.8)
    return (
        TensorDataset(torch.from_numpy(x[:split]), torch.from_numpy(y[:split])),
        TensorDataset(torch.from_numpy(x[split:]), torch.from_numpy(y[split:])),
    )


def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
) -> float:
    """Treina modelo por uma época."""
    model.train()
    total_loss = 0.0
    for xb, yb in loader:
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        optimizer.step()
        total_loss += float(loss.item())
    return total_loss / max(1, len(loader))


def evaluate(model: nn.Module, loader: DataLoader) -> float:
    """Calcula acurácia de classificação."""
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for xb, yb in loader:
            preds = model(xb).argmax(1)
            correct += int((preds == yb).sum().item())
            total += len(yb)
    return correct / max(1, total)


def run(epochs: int = 20) -> None:
    """Executa benchmark comparativo da fase 2."""
    train_ds, val_ds = make_dataset()
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=64)

    print("\n" + "═" * 60)
    print("  FASE 2 — FeignbaumMLP vs MLP Estática")
    print("═" * 60)

    print("\n▶ FeignbaumMLP (topologia dinâmica)")
    model_f = FeignbaumMLP(input_dim=64, hidden_dim=64, output_dim=4, emit=False)
    opt_f = optim.Adam(model_f.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        loss = train_epoch(model_f, train_loader, opt_f, criterion)
        report = model_f.policy_step()
        if (epoch + 1) % 5 == 0:
            acc = evaluate(model_f, val_loader)
            print(
                f"  Epoch {epoch + 1:02d}: loss={loss:.4f} acc={acc:.3f} "
                f"layers={report['alive_layers']} "
                f"spawned={len(report['spawned'])} "
                f"pruned={len(report['pruned'])}"
            )

    acc_f = evaluate(model_f, val_loader)
    tokens_f = model_f.emitter.stats()

    print("\n▶ MLP Estática (topologia fixa)")
    model_s = nn.Sequential(
        nn.Linear(64, 64),
        nn.ReLU(),
        nn.Linear(64, 64),
        nn.ReLU(),
        nn.Linear(64, 4),
    )
    opt_s = optim.Adam(model_s.parameters(), lr=1e-3)

    for _ in range(epochs):
        train_epoch(model_s, train_loader, opt_s, criterion)

    acc_s = evaluate(model_s, val_loader)

    print("\n" + "═" * 60)
    print("  RESULTADO COMPARATIVO")
    print("═" * 60)
    print(f"  FeignbaumMLP  acc={acc_f:.3f}  tokens_emitidos={tokens_f['total_tokens']}")
    print(f"  MLP Estática  acc={acc_s:.3f}  tokens_emitidos=0")
    print("\n  Ledger Enochian (últimos 5 tokens):")
    lines = model_f.emitter.export_ledger().strip().split("\n")
    for line in lines[-5:]:
        print(f"    {line[:80]}...")
    print("\n  ✓ Fase 2 concluída. Próximo: Fase 3 — Ponte MelissaCore.\n")


if __name__ == "__main__":
    run()
