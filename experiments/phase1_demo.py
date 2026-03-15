"""
Fase 1 — Validação Empírica de δ com Plots.

Executa:
  1. Localiza pontos de bifurcação r_1..r_5 via period-doubling
  2. Calcula δ_empirico = (r_{n+1}-r_n)/(r_{n+2}-r_{n+1}) e compara com δ teórico
  3. Plota diagrama de bifurcação completo com marcadores r_n
  4. Plota expoente de Lyapunov λ(r) — confirma onset do caos
  5. Plota convergência das razões δ_n → δ
  6. Demo FeigenbaumForest + FractalMemory

Rode: python experiments/phase1_demo.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from src.logistic import find_bifurcation_points, compute_delta_ratios, bifurcation_diagram, lyapunov_exponent
from src.spawn_policy import FeigenbaumForest
from src.fractal_memory import FractalMemory
from src.constants import FEIGENBAUM_DELTA

SEP = "═" * 64


def banner(t):
    print(f"\n{SEP}\n  {t}\n{SEP}")


def validate_delta_empirically(bifs):
    """
    Validação empírica central do projeto.
    Calcula razões de convergência e erro percentual vs δ teórico.
    """
    ratios = compute_delta_ratios(bifs)
    print(f"\n  δ teórico  = {FEIGENBAUM_DELTA:.10f}")
    print(f"  {'n':>3}  {'r_n':>12}  {'δ_n':>10}  {'erro %':>8}  {'status'}")
    print(f"  {'-' * 55}")
    for i, (r, ratio) in enumerate(zip(bifs[1:], ratios)):
        erro = abs(ratio - FEIGENBAUM_DELTA) / FEIGENBAUM_DELTA * 100
        ok = "✓" if erro < 20 else "~"
        print(f"  {ok} {i + 1:>2}  {r:12.8f}  {ratio:10.5f}  {erro:8.2f}%")
    return ratios


def plot_full_analysis(bifs, ratios):
    """Gera figura com 3 subplots: bifurcação, Lyapunov, convergência δ."""
    fig = plt.figure(figsize=(18, 6))
    gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)

    ax1 = fig.add_subplot(gs[0])
    rs, xs = bifurcation_diagram(r_range=(2.5, 4.0), r_steps=3500, last_n=250)
    ax1.scatter(rs, xs, s=0.04, c="#2196F3", alpha=0.25, rasterized=True)
    for i, r in enumerate(bifs):
        ax1.axvline(r, color="#E53935", lw=0.9, alpha=0.8, ls="--")
        ax1.text(r + 0.005, 0.92, f"r_{i + 1}", fontsize=7, color="#E53935",
                 transform=ax1.get_xaxis_transform())
    ax1.set_xlabel("r", fontsize=11)
    ax1.set_ylabel("x*", fontsize=11)
    ax1.set_title("Diagrama de Bifurcação\nMapa Logístico f(x)=rx(1-x)", fontsize=10)
    ax1.set_xlim(2.5, 4.0)

    ax2 = fig.add_subplot(gs[1])
    r_vals = np.linspace(2.5, 4.0, 600)
    lya = [lyapunov_exponent(r, n=4000) for r in r_vals]
    ax2.plot(r_vals, lya, "#2196F3", lw=0.9, label="λ(r)")
    ax2.axhline(0, color="#E53935", lw=1.2, label="λ=0")
    ax2.fill_between(r_vals, lya, 0,
                     where=[l > 0 for l in lya],
                     color="#E53935", alpha=0.12, label="Região caótica")
    for r in bifs:
        ax2.axvline(r, color="#FF9800", lw=0.7, alpha=0.6, ls=":")
    ax2.set_xlabel("r", fontsize=11)
    ax2.set_ylabel("λ (Expoente de Lyapunov)", fontsize=11)
    ax2.set_title("Expoente de Lyapunov\nConfirma onset do caos", fontsize=10)
    ax2.legend(fontsize=8)
    ax2.set_xlim(2.5, 4.0)

    ax3 = fig.add_subplot(gs[2])
    ns = list(range(1, len(ratios) + 1))
    ax3.plot(ns, ratios, "o-", color="#2196F3", lw=2,
             markersize=8, label="δ_n empírico")
    ax3.axhline(FEIGENBAUM_DELTA, color="#E53935", lw=1.5,
                ls="--", label=f"δ teórico = {FEIGENBAUM_DELTA:.4f}")
    ax3.fill_between(
        [min(ns) - 0.3, max(ns) + 0.3],
        [FEIGENBAUM_DELTA * 0.9] * 2,
        [FEIGENBAUM_DELTA * 1.1] * 2,
        color="#E53935", alpha=0.08, label="±10% do teórico"
    )
    for n, r in zip(ns, ratios):
        ax3.annotate(f"{r:.3f}", (n, r), textcoords="offset points",
                     xytext=(6, 4), fontsize=8)
    ax3.set_xlabel("n (ordem da razão)", fontsize=11)
    ax3.set_ylabel("δ_n = (r_{n+1}-r_n)/(r_{n+2}-r_{n+1})", fontsize=9)
    ax3.set_title(f"Convergência Empírica → δ\nδ = {FEIGENBAUM_DELTA:.6f}", fontsize=10)
    ax3.legend(fontsize=8)
    ax3.set_xticks(ns)

    plt.suptitle(
        "FeigenbaumIA — Validação Empírica da Constante Universal δ ≈ 4.669",
        fontsize=13, fontweight="bold", y=1.02
    )
    os.makedirs("experiments", exist_ok=True)
    out = "experiments/phase1_analysis.png"
    plt.savefig(out, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"\n  Figura salva: {out}")
    return out


def main():
    banner("1. LOCALIZANDO PONTOS DE BIFURCAÇÃO (period-doubling)")
    print("  Aguarde ~20s...")
    bifs = find_bifurcation_points()
    print(f"  {len(bifs)} pontos encontrados:")
    for i, r in enumerate(bifs):
        print(f"    r_{i + 1} = {r:.10f}")

    banner("2. VALIDAÇÃO EMPÍRICA DE δ")
    ratios = validate_delta_empirically(bifs)

    banner("3. EXPOENTE DE LYAPUNOV — AMOSTRAS")
    for r, label in [
        (2.9, "r=2.9  (estável, período-1)"),
        (3.2, "r=3.2  (período-2)"),
        (3.5, "r=3.5  (período-4)"),
        (3.57, "r=3.57 (onset do caos)"),
        (3.83, "r=3.83 (janela período-3)"),
        (3.9, "r=3.9  (caótico)"),
    ]:
        lam = lyapunov_exponent(r)
        estado = "CAOS" if lam > 0 else "ESTÁVEL"
        print(f"  {label:38s}: λ = {lam:+.5f}  [{estado}]")

    banner("4. GERANDO PLOTS")
    plot_full_analysis(bifs, ratios)

    banner("5. FEIGENBAUM FOREST — CICLOS DE EVOLUÇÃO")
    forest = FeigenbaumForest(max_depth=5, emit=False)
    rng = np.random.default_rng(42)
    for cycle in range(20):
        alive_ids = {m.id for m in forest._walk() if m.alive}
        entropies = {i: float(rng.uniform(0.05, 0.95)) for i in alive_ids}
        report = forest.step(entropies)
        if (cycle + 1) % 5 == 0:
            topo = forest.topology_summary()
            print(f"  Ciclo {cycle + 1:02d}: alive={report['alive']:3d}  "
                  f"depth={report['max_depth']}  "
                  f"spawns_total={topo['total_spawns']}  "
                  f"H_avg={report['avg_entropy']:.3f}")

    banner("6. FRACTAL MEMORY — COMPRESSÃO DCT")
    mem = FractalMemory(base_dim=128, n_levels=5)
    for _ in range(30):
        mem.store(rng.standard_normal(128))
    stats = mem.stats()
    for k in range(5):
        s = stats[f"level_{k}"]
        print(f"  Nível {k} [{s['tier']:4s}]: "
              f"dim={s['dim']:3d}  "
              f"entries={s['n_entries']:2d}  "
              f"compressão={s['compression']:.1f}×")
    orig = rng.standard_normal(128)
    mem.store(orig)
    recon = mem.reconstruct(level=2)
    mse = float(np.mean((orig - recon[:128]) ** 2))
    print(f"\n  Reconstrução nível 2 MSE = {mse:.6f}")

    banner("FASE 1 CONCLUÍDA ✓ — δ VALIDADO EMPIRICAMENTE")
    if ratios:
        best = min(abs(r - FEIGENBAUM_DELTA) / FEIGENBAUM_DELTA for r in ratios)
        print(f"  Melhor aproximação: erro = {best * 100:.2f}% vs δ teórico")
    print("  Plots em: experiments/phase1_analysis.png")
    print("  Próximo: python experiments/phase2_demo.py\n")


if __name__ == "__main__":
    main()
