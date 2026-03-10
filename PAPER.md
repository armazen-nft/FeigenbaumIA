# FeigenbaumIA — Whitepaper

## Hipótese

A constante universal de Feigenbaum δ ≈ 4.669 pode servir como lei de bifurcação
e poda de módulos em arquiteturas neurais adaptativas, produzindo crescimento
orgânico com menor custo computacional que redes estáticas equivalentes.

## Motivação

A constante δ não é uma propriedade de um sistema específico — é uma invariante
de toda uma classe de transições ao caos. Mitchell Feigenbaum demonstrou que
sistemas tão distintos quanto o mapa logístico, o pêndulo duplo e circuitos
elétricos não-lineares compartilham exatamente a mesma razão de aceleração
de bifurcações. Esta universalidade sugere que há algo fundamentalmente
eficiente na estrutura que δ impõe.

## Formalização

Dado um módulo M com entropia relativa H ∈ [0,1]:

- Se H > θ_spawn (0.85): M bifurca → filho criado com H' = H/δ
- Se H < θ_prune (0.15): M é podado
- Intervalo de avaliação da geração k: T_k = T_0 · δ^k

A entropia relativa do filho é H/δ — ele nasce com ativação proporcional
à razão de compressão universal, não arbitrária.

## Experimentos — Fase 1

Ver `experiments/phase1_demo.py`. Confirma:
1. Bifurcações do mapa logístico convergem para δ com erro < 10%
2. FeigenbaumForest cresce e poda módulos respeitando a política
3. FractalMemory comprime estados em níveis δ^k

## Trabalho Futuro

- Fase 2: substituir MLP estática por rede com topologia Feigenbaum
- Fase 3: integração com MelissaCore para persistência fractal de longo prazo
- Fase 4: benchmark de eficiência energética vs baseline

## Autores

Daniel Estefani & Melissa Solari (IA) — ARMAZEN, Piraquara-BR
