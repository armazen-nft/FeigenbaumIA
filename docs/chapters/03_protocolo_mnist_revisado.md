# Capítulo 3 — Protocolo Experimental Revisado: MNIST (v2.0)

**Objetivo principal:** Verificar empiricamente se a razão de bifurcações observada em módulos MLP converge para δ ≈ 4.669.

## 3.1 Arquitetura

- Dataset: MNIST (60k train / 10k test)
- Módulo base: FeigenbaumModule (1 camada linear + sigmoid → mapa logístico)
- Hierarquia: inicia com 1 módulo, spawn até máximo 8 níveis
- Loss: CrossEntropy + regularização de divergência

## 3.2 Como medir δ (definição rigorosa)

```python
x_series = []  # coleta em cada forward
for batch in loader:
    h = module(x)
    x_log = r * norm(h) * (1 - norm(h))
    x_series.append(x_log.mean().item())

# Após 500 passos:
attractor = x_series[-200:]
period = len(set(round(v, 6) for v in attractor))
# Compara com período anterior → calcula razão
ratio = (r_current - r_prev) / (r_next - r_current)
```

## 3.3 Baselines (claros e reproduzíveis)

- MLP fixo (mesmo total de parâmetros)
- Lottery Ticket Hypothesis (pruning estático)
- Dynamic Sparse Training (DST)

## 3.4 Procedimento passo a passo

1. Treinar por 50 épocas com Adam (lr=0.001)
2. A cada 5 épocas: calcular razão δ por módulo
3. Registrar: acurácia, pico GPU (GB), FLOPs (torch.profiler), erro |δ_obs - 4.669|
4. Repetir 10 seeds diferentes

## 3.5 Métricas principais

- Erro médio na estimativa de δ (< 0.05 = sucesso)
- Redução de memória/FLOPs vs. baseline
- Acurácia final (esperado > 98 %)

Notebook de referência: notebooks/02_mnist_validation.ipynb (próximo commit)
Próximo passo: rodar o experimento completo e publicar resultados em arXiv/NeurIPS 2026.
