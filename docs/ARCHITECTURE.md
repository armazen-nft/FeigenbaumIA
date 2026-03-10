# Architecture

## Fase 1 — Base

- `src/constants.py`: constantes globais.
- `src/logistic.py`: mapa logístico.
- `src/spawn_policy.py`: política de floresta.
- `src/fractal_memory.py`: memória fractal.

## Fase 2 — Módulos Adicionados

### src/enochian.py
EnochianEmitter + GlyphType + EnochianToken.
Cada evento do ciclo de vida de um módulo (spawn, prune, measure, connect)
emite um token serializado como JSON Lines — blockchain-ready.

### src/feigenbaum_mlp.py
FeignbaumMLP: rede PyTorch com camadas ocultas dinâmicas.
Topologia evolui via policy_step() chamado a cada epoch.
Herança de pesos: filho recebe pesos_pai / δ.

### src/melissa_bridge.py
MelissaBridge: exporta FractalMemory para pastas HOT/WARM/COLD.
Interface local no momento; preparada para HTTP/socket na Fase 3.2.

## Grafo de Dependências

```text
constants.py
    ├── logistic.py
    ├── spawn_policy.py ──→ enochian.py
    ├── fractal_memory.py ──→ melissa_bridge.py ──→ [MelissaCore]
    └── feigenbaum_mlp.py ──→ enochian.py
```

## Próxima Fase (3)

- melissa_bridge.py: implementar modo remoto (HTTP para MelissaCore)
- fractal_memory.py: substituir truncation por DCT real
- enochian.py: adicionar submit_to_iotex() para registro blockchain
- experiments/phase3_demo.py: loop completo Feigenbaum → Melissa → PoE
