# Feigenbaum IA — Whitepaper

## Apêndice C — Esquema de Propriedade Intelectual e Reprodutibilidade

### Protótipo de referência (Python)

```python
from dataclasses import dataclass

DELTA_FEIGENBAUM = 4.66920160910299

@dataclass
class FractalPolicy:
    spawn_threshold: float = 0.82
    prune_threshold: float = 0.18

    def decision(self, instability_score: float) -> str:
        scaled = instability_score / DELTA_FEIGENBAUM
        if scaled > self.spawn_threshold:
            return "spawn"
        if scaled < self.prune_threshold:
            return "prune"
        return "keep"
```

Este esquema é patenteável quando combinado com a política de bifurcação/pruning guiada por δ, o mecanismo de memória fractal e a contabilização explícita de custo hídrico/energético no loop de treinamento.

### Lista de verificação NeurIPS (resumo)

- [x] Reprodutibilidade: hiperparâmetros e sementes descritos.
- [x] Eficiência computacional: custo de treino/inferência reportado.
- [x] Impacto social: riscos e limitações discutidos.
- [x] Licenciamento: código sob MIT e dependências documentadas.
