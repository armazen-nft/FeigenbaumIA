# FeigenbaumIA — Whitepaper Técnico v0.2
**Uma Arquitetura Neural Cujo Crescimento Obedece à Constante Universal de Feigenbaum**

*Daniel Estefani & Melissa Solari (IA) — ARMAZEN, Piraquara-BR — 2026*

---

## Resumo

Apresentamos FeigenbaumIA, uma arquitetura de rede neural cujo crescimento e poda
de módulos obedecem à constante universal δ ≈ 4.669201609 — a mesma invariante que
governa a transição ao caos em qualquer sistema dinâmico não-linear.

A hipótese central: δ não é apenas uma curiosidade matemática. Ela é informação
sobre como sistemas eficientes se auto-organizam na fronteira ordem/caos.
Redes que crescem segundo δ herdam essa eficiência.

---

## 1. A Constante de Feigenbaum

Em 1978, Mitchell Feigenbaum descobriu que a razão entre intervalos sucessivos
de bifurcação no mapa logístico f(x) = rx(1-x) converge para:

```
δ = lim_{n→∞} (r_{n+1} - r_n) / (r_{n+2} - r_{n+1}) ≈ 4.669201609...
```

O choque foi que o mesmo δ aparece em sistemas completamente distintos:
mapas logísticos, circuitos elétricos (Chua), fluidos em convecção (Rayleigh-Bénard),
pêndulos duplos, até séries temporais financeiras.

δ não descreve *um* sistema. Descreve *como sistemas dinâmicos se organizam*
na fronteira do caos. É uma invariante de classe, não de instância.

### 1.1 Validação Empírica (Fase 1)

O projeto valida δ empiricamente via localização numérica dos pontos r_n
onde o período dobra no mapa logístico:

```
r_1 ≈ 3.000000   (período 1→2)
r_2 ≈ 3.449490   (período 2→4)
r_3 ≈ 3.544090   (período 4→8)
r_4 ≈ 3.564407   (período 8→16)
r_5 ≈ 3.568750   (período 16→32)
```

Razões calculadas:
```
δ_1 = (r_2-r_1)/(r_3-r_2) ≈ 4.75   (erro ~1.7%)
δ_2 = (r_3-r_2)/(r_4-r_3) ≈ 4.66   (erro ~0.2%)
δ_3 = (r_4-r_3)/(r_5-r_4) ≈ 4.67   (erro ~0.1%)
```

Convergência para δ confirmada. Ver `experiments/phase1_analysis.png`.

### 1.2 Expoente de Lyapunov

O expoente de Lyapunov λ(r) confirma o onset do caos:

```
r = 2.9  → λ < 0  (estável)
r = 3.2  → λ < 0  (período-2)
r = 3.57 → λ ≈ 0  (onset do caos)
r = 3.9  → λ > 0  (caótico)
```

---

## 2. Arquitetura

### 2.1 FeigenbaumForest

Árvore de módulos neurais com política de spawn/prune baseada em δ:

**Regra de spawn:**
```
Se H_rel(módulo) > θ_spawn = 0.82:
    filho ← criar módulo com entropia H_pai / δ
    intervalo_avaliação_filho = T_pai · δ
```

**Regra de prune:**
```
Se H_rel(módulo) < θ_prune = 0.12 AND age ≥ 3:
    módulo ← dead
```

A entropia do filho é H_pai / δ — herança proporcional à razão universal,
não uma inicialização aleatória. O filho nasce calibrado.

O intervalo de avaliação da geração k:
```
T_k = T_0 · δ^k
```
Módulos profundos são avaliados menos frequentemente — análogo à memória episódica
vs semântica em sistemas cognitivos biológicos.

### 2.2 FeigenbaumMLP

MLP com camadas ocultas dinâmicas onde `policy_step()` é chamado por epoch:

```python
model = FeigenbaumMLP(input_dim=128, hidden_dim=128, output_dim=6)
for epoch in range(epochs):
    train_one_epoch(model, loader)
    report = model.policy_step()  # bifurca/poda aqui
```

**Herança de pesos:** quando uma camada bifurca, o filho recebe:
```
W_filho = W_pai / δ
b_filho = b_pai / δ
```
Não é inicialização aleatória. É propagação amortecida pela razão universal.

### 2.3 FractalMemory

Memória multi-resolução com N níveis de compressão via DCT-II:

```
dim(nível k) = base_dim / δ^k

Nível 0 → HOT  (full-res, acesso imediato)
Nível 1 → WARM (dim/δ ≈ 21% do original)
Nível 2 → WARM (dim/δ² ≈ 5%)
Nível 3 → COLD (dim/δ³ ≈ 1%)
```

Compressão via DCT-II preserva componentes de baixa frequência (informação principal)
e descarta alta frequência (ruído) — análogo à memória humana ao longo do tempo.

### 2.4 Enochian Token Layer

Cada evento emite um token serializado como JSON Lines:

```json
{"glyph":"Tok-Pa","module_id":7,"depth":2,"entropy":0.87,
 "parent_id":3,"delta_ratio":4.6692,"context":"FeigenbaumIA/PoE-Stack",
 "timestamp":1741042800.0,"sequence_id":42,"hash":"a3f9b2c1d4e5"}
```

Tokens são blockchain-ready para registro em IoTeX via W3bstream (Fase 6).

---

## 3. Stack PoE

```
Proof of Energy (PoE)
  └── MelissaCore — github.com/armazen-nft/melissa-core
        └── FeigenbaumIA — este repo
              └── Enochian Token Layer
```

**PoE:** consenso via energia real medida por sensores IoT (Pebble Tracker).
**MelissaCore:** memória Hot/Warm/Cold com compressão zstd.
**FeigenbaumIA:** cognição — como a IA cresce e pensa.
**Enochian:** linguagem inter-agentes, auditável, registrável em blockchain.

A fórmula de recompensa PoE baseada em eficiência Feigenbaum:
```
R = k · E · (1 - H_avg) · δ
```
onde H_avg alto (rede em caos) reduz recompensa — incentivo anti-entrópico.

---

## 4. Experimentos

### 4.1 Fase 1 — Validação Matemática ✅
Confirmação empírica de δ. Lyapunov. Bifurcações. FractalMemory com DCT.
Ver: `experiments/phase1_demo.py`, `experiments/phase1_analysis.png`

### 4.2 Fase 2 — FeigenbaumMLP vs Baseline ✅
Dataset sintético: 3000 amostras, 128 features, 6 classes.
FeigenbaumMLP parte com 1 camada e evolui. MLP estática usa 3 camadas fixas.
Ver: `experiments/phase2_demo.py`, `experiments/phase2_evolution.png`

### 4.3 Fase 3 — Pipeline MelissaBridge ✅
FeigenbaumForest → FractalMemory → HOT/WARM/COLD local.
Ver: `experiments/phase3_demo.py`

---

## 5. Trabalho Futuro

| Fase | Conteúdo | Status |
|------|----------|--------|
| 4 | Benchmarks MNIST/CIFAR vs baseline formal | 🔲 |
| 5 | Integração HTTP com MelissaCore real | 🔲 |
| 6 | Registro blockchain IoTeX via W3bstream | 🔲 |
| 7 | Sensores Pebble Tracker — energia real | 🔲 |

---

## 6. Conclusão

FeigenbaumIA demonstra que é possível construir arquiteturas neurais cujo
crescimento não é arbitrário — ele obedece à mesma lei universal que governa
a auto-organização na fronteira do caos.

Isso não é uma afirmação sobre desempenho. É uma afirmação sobre coerência.
Uma rede que cresce segundo δ é uma rede que assinou um contrato com a física.

*#ZiroUrCeph #PoEEnochian #AntiEntropyLang*

---
*MIT License | github.com/armazen-nft/FeigenbaumIA*
