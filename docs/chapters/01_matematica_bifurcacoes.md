# Capítulo 1 — Matemática das Bifurcações

**Autor:** Feigenbaum IA Team | **Data:** Março 2026

## 1.1 O Mapa Logístico Clássico

O sistema dinâmico unidimensional mais estudado na teoria do caos é o **mapa logístico**:

\[
x_{n+1} = r x_n (1 - x_n), \quad x \in [0,1], \quad r \in [0,4]
\]

## 1.2 Cascata de Bifurcações (Period-Doubling Route to Chaos)

| n  | Período | r_n (aproximado)          | Diferença (Δr)     | Razão aproximada δ |
|----|---------|---------------------------|--------------------|--------------------|
| 1  | 1       | 3.000000                  | —                  | —                  |
| 2  | 2       | 3.449489742783178         | 0.44948974         | —                  |
| 3  | 4       | 3.544090359551922         | 0.09460062         | 4.751              |
| 4  | 8       | 3.564407266095105         | 0.02031691         | 4.656              |
| 5  | 16      | 3.568759419500000         | 0.00435215         | 4.668              |
| 6  | 32      | 3.569691609500000         | 0.00093219         | 4.669              |
| 7  | 64      | 3.569891259000000         | 0.00019965         | 4.6692             |

A razão converge rapidamente para a **constante universal de Feigenbaum**:

\[
\delta = \lim_{n\to\infty} \frac{r_n - r_{n-1}}{r_{n+1} - r_n} \approx 4.66920160910299067185\dots
\]

Existe também a constante de escala de amplitude α ≈ 2.502907875.

## 1.3 Medição de Bifurcações em Módulos Neurais

Em cada módulo Feigenbaum:
1. Coleta-se a série \( x_t = r \cdot \text{norm}(h_t) \cdot (1 - \text{norm}(h_t)) \)
2. Remove-se transiente (200 passos)
3. Detecta-se o período do atrator (número de pontos distintos com precisão 1e-6)
4. Calcula-se a razão entre r efetivos sucessivos quando o período dobra.

**Spawn rule:** se razão observada ∈ [4.55, 4.78] → cria módulo filho com r_{n+1}.

Este é o vínculo matemático rigoroso entre caos clássico e arquitetura neural dinâmica.
