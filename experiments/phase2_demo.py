"""
Fase 2 — FeigenbaumMLP com Topologia Dinâmica + Plots de Evolução.

Compara:
  A) FeigenbaumMLP — topologia evolui durante treino via δ
  B) MLP Estática  — arquitetura fixa equivalente

Plots gerados:
  - Evolução de camadas vivas por epoch
  - Entropia média por epoch
  - Árvore de tokens Enochian emitidos
  - Accuracy comparativa

Rode: python experiments/phase2_demo.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.feigenbaum_mlp import FeigenbaumMLP
from src.poe_interface import PoEInterface

SEP = "═" * 64


def banner(t):
    print(f"\n{SEP}\n  {t}\n{SEP}")


def synthetic_dataset(n=3000, d=128, n_classes=6, seed=42):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d)).astype(np.float32)
    centers = rng.standard_normal((n_classes, d)).astype(np.float32) * 2
    y = np.argmin(np.linalg.norm(X[:, None] - centers[None], axis=2), axis=1).astype(np.int64)
    split = int(n * 0.8)
    return (
        TensorDataset(torch.from_numpy(X[:split]), torch.from_numpy(y[:split])),
        TensorDataset(torch.from_numpy(X[split:]), torch.from_numpy(y[split:])),
    )


def train_epoch(model, loader, optimizer, criterion):
    model.train()
    total = 0.0
    for xb, yb in loader:
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        optimizer.step()
        total += loss.item()
    return total / len(loader)


def evaluate(model, loader):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for xb, yb in loader:
            correct += (model(xb).argmax(1) == yb).sum().item()
            total += len(yb)
    return correct / total


def plot_evolution(history_f, history_s, epochs):
    """Gera figura com 4 subplots de evolução."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    ep = list(range(1, epochs + 1))

    ax = axes[0, 0]
    ax.plot(ep, history_f["acc"], "b-o", ms=4, label="FeigenbaumMLP")
    ax.plot(ep, history_s["acc"], "r--s", ms=4, label="MLP Estática")
    ax.set_title("Accuracy por Epoch")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(ep, history_f["layers"], "g-o", ms=4, label="Camadas vivas")
    ax.fill_between(ep, history_f["layers"], alpha=0.15, color="green")
    ax.set_title("Camadas Vivas — FeigenbaumMLP")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("N camadas")
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(ep, history_f["entropy"], "m-o", ms=4, label="H média")
    ax.axhline(0.82, color="red", ls="--", lw=1, label="θ_spawn=0.82")
    ax.axhline(0.12, color="blue", ls="--", lw=1, label="θ_prune=0.12")
    ax.set_title("Entropia Média das Camadas")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Entropia")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1)

    ax = axes[1, 1]
    token_counts = history_f["token_by_glyph"]
    glyphs = list(token_counts.keys())
    counts = list(token_counts.values())
    colors = plt.cm.Set3(np.linspace(0, 1, len(glyphs)))
    bars = ax.bar(glyphs, counts, color=colors, edgecolor="gray", lw=0.5)
    ax.set_title("Ledger Enochian — Tokens por Tipo")
    ax.set_xlabel("Glifo")
    ax.set_ylabel("Total emitido")
    ax.tick_params(axis="x", rotation=45)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(count), ha="center", fontsize=8)

    plt.suptitle(
        "FeigenbaumMLP — Evolução da Topologia Dinâmica via δ ≈ 4.669",
        fontsize=13, fontweight="bold"
    )
    plt.tight_layout()
    os.makedirs("experiments", exist_ok=True)
    out = "experiments/phase2_evolution.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n  Figura salva: {out}")


def run(epochs=30):
    train_ds, val_ds = synthetic_dataset()
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=64)
    criterion = nn.CrossEntropyLoss()
    poe = PoEInterface()

    history_f = {"acc": [], "layers": [], "entropy": [], "token_by_glyph": {}}
    history_s = {"acc": []}

    banner("A) FEIGENBAUM MLP — TOPOLOGIA DINÂMICA")
    model_f = FeigenbaumMLP(
        input_dim=128, hidden_dim=128, output_dim=6,
        max_hidden_layers=10, emit=False
    )
    opt_f = optim.Adam(model_f.parameters(), lr=3e-4, weight_decay=1e-5)

    for epoch in range(epochs):
        loss = train_epoch(model_f, train_loader, opt_f, criterion)
        report = model_f.policy_step()
        acc = evaluate(model_f, val_loader)
        poe.register_cycle(report["alive_layers"], report["avg_entropy"])

        history_f["acc"].append(acc)
        history_f["layers"].append(report["alive_layers"])
        history_f["entropy"].append(report["avg_entropy"])

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  Epoch {epoch + 1:02d}: loss={loss:.4f}  acc={acc:.3f}  "
                  f"layers={report['alive_layers']}  "
                  f"↑{len(report['spawned'])} ↓{len(report['pruned'])}  "
                  f"H={report['avg_entropy']:.3f}")

    history_f["token_by_glyph"] = model_f.emitter.stats()["by_glyph"]
    acc_f = evaluate(model_f, val_loader)
    topo_f = model_f.topology_info()

    banner("B) MLP ESTÁTICA — TOPOLOGIA FIXA (3 camadas)")
    model_s = nn.Sequential(
        nn.Linear(128, 128), nn.ReLU(),
        nn.Linear(128, 128), nn.ReLU(),
        nn.Linear(128, 128), nn.ReLU(),
        nn.Linear(128, 6),
    )
    opt_s = optim.Adam(model_s.parameters(), lr=3e-4, weight_decay=1e-5)

    for epoch in range(epochs):
        train_epoch(model_s, train_loader, opt_s, criterion)
        acc = evaluate(model_s, val_loader)
        history_s["acc"].append(acc)
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  Epoch {epoch + 1:02d}: acc={acc:.3f}  layers=3 (fixo)")

    acc_s = evaluate(model_s, val_loader)
    params_s = sum(p.numel() for p in model_s.parameters())

    banner("COMPARATIVO FINAL")
    print(f"\n  {'Modelo':<22} {'Acc':>6}  {'Params':>8}  {'Layers':>7}  {'Tokens':>8}")
    print(f"  {'-' * 60}")
    print(f"  {'FeigenbaumMLP':<22} {acc_f:6.3f}  "
          f"{topo_f['total_params']:8d}  "
          f"{topo_f['alive_layers']:7d}  "
          f"{model_f.emitter.stats()['total_tokens']:8d}")
    print(f"  {'MLP Estática':<22} {acc_s:6.3f}  "
          f"{params_s:8d}  {'3':>7}  {'0':>8}")

    banner("GERANDO PLOTS DE EVOLUÇÃO")
    plot_evolution(history_f, history_s, epochs)

    banner("POE INTERFACE — SUMÁRIO")
    for k, v in poe.stats().items():
        print(f"  {k}: {v}")

    print("\n  ✓ Fase 2 concluída.")
    print("  Plots: experiments/phase2_evolution.png")
    print("  Próximo: python experiments/phase3_demo.py\n")


if __name__ == "__main__":
    run()
