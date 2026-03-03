import matplotlib.pyplot as plt
import numpy as np

DELTA = 4.66920160910299067185320382
R_STAR = 3.569945671
DELTA0 = 0.1
N_LEVELS = 8
X0 = 0.5
TRANSIENT = 200
ATTRACTOR_POINTS = 8


def run_hierarchical_logistic():
    r_values = [R_STAR - DELTA0 * (DELTA ** -n) for n in range(N_LEVELS)]
    x_values = [X0]
    attractor_history = []

    for r in r_values:
        x = x_values[-1]
        # descarta transiente
        for _ in range(TRANSIENT):
            x = r * x * (1 - x)
        # coleta attractor
        attractor = []
        for _ in range(ATTRACTOR_POINTS):
            x = r * x * (1 - x)
            attractor.append(x)
        x_values.extend(attractor)
        attractor_history.append((r, attractor))

    # Plot profissional
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(x_values)), x_values, "o-", markersize=4, label="Trajetória hierárquica")
    plt.title("Mapa Logístico Hierárquico — Bifurcações seguindo δ de Feigenbaum")
    plt.xlabel("Passo (nível + attractor points)")
    plt.ylabel("Estado x")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("feigenbaum_bifurcation.png", dpi=300)
    plt.show()

    return attractor_history


if __name__ == "__main__":
    run_hierarchical_logistic()
    print("✅ Protótipo executado! Gráfico salvo como feigenbaum_bifurcation.png")
