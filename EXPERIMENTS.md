# Protocolo Experimental Feigenbaum IA

## Objetivo
Demonstrar empiricamente convergência da razão de bifurcações para δ em módulos MLP dinâmicos.

## Tarefas & Baselines
- MNIST
- CartPole-v1
- Baselines: MLP fixo, Lottery Ticket, Dynamic Sparse Training

## Como medir δ (código esboço)
```python
# dentro do forward loop
x_series.append(logistic_activation(h))
# após 200 passos:
attractor = detect_attractor(x_series)
period = len(set(round(p, 6) for p in attractor))
# comparar com períodos anteriores para calcular razão
```

## Métricas

- `|razão_observada - 4.669| < 0.05`
- Memória GPU, FLOPs, acurácia/reward

Implementar em `notebooks/02_mnist_validation.ipynb` — prioridade máxima.
