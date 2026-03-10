# Arquitetura FeigenbaumIA

## Princípio Central

A constante de Feigenbaum δ ≈ 4.669 é universal: ela aparece na transição ao caos
em sistemas dinâmicos completamente distintos. Este projeto usa δ como **lei de
crescimento e poda** de módulos neurais — não como metáfora, mas como política real.

## Camadas

```text
┌─────────────────────────────────────────────────┐
│  FeigenbaumForest (spawn_policy.py)             │
│  Gerencia árvore de módulos via entropia relativa│
├─────────────────────────────────────────────────┤
│  MLP Feigenbaum (Fase 2 — PyTorch)              │
│  Rede neural cujos nós bifurcam/podão via δ     │
├─────────────────────────────────────────────────┤
│  FractalMemory (fractal_memory.py)              │
│  Estados internos comprimidos em níveis δ^k     │
├─────────────────────────────────────────────────┤
│  MelissaCore Hot/Warm/Cold (Fase 3 — integração)│
│  Persistência de longo prazo dos estados        │
└─────────────────────────────────────────────────┘
```

## Fases

| Fase | Conteúdo | Status |
|------|----------|--------|
| 0 | Fundação — estrutura do repo | ✅ |
| 1 | Protótipo matemático puro (logístico + Forest + FractalMemory) | ✅ |
| 2 | MLP PyTorch com política Feigenbaum | 🔲 |
| 3 | Memória fractal DCT + integração MelissaCore | 🔲 |
| 4 | Benchmarks vs baseline MLP estática | 🔲 |
