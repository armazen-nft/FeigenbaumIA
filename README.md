# Feigenbaum IA 🚀

**Arquitetura de IA fractal-adaptativa baseada na constante universal de Feigenbaum (δ ≈ 4.669)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-orange)

> “Onde há caos controlado, nasce a inteligência mais eficiente da natureza.”

## Visão

Uma rede neural que **bifurca e poda módulos seguindo a mesma lei matemática que rege a transição para o caos** — garantindo crescimento orgânico, compressão fractal e consumo mínimo de energia e água.

## ✨ Destaques

- Protótipo matemático hierárquico (Capítulo 1) — **pronto e corrigido**
- Versão Single-Node PyTorch com medição real de GPU + água simulada
- Políticas adaptativas de spawn/prune via δ
- Memória fractal (compressão automática)
- Whitepaper completo: [PAPER.md](PAPER.md)

## Estrutura do Projeto

```text
FeigenbaumIA/
├── LICENSE
├── README.md
├── PAPER.md                  # Whitepaper completo
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   └── feigenbaum_ia/
│       ├── __init__.py
│       ├── logistic_map.py       # Protótipo matemático corrigido
│       ├── neural_module.py      # Single-node PyTorch
│       └── utils.py              # medição energia/água
├── notebooks/
│   └── 01_prototype.ipynb
├── docs/
│   ├── roadmap.md
│   └── chapters/
├── examples/
└── .github/workflows/ci.yml
```

## Instalação Rápida

```bash
git clone https://github.com/armazen-nft/FeigenbaumIA.git
cd FeigenbaumIA
pip install -r requirements.txt
```

Teste imediato:

```bash
python -m src.feigenbaum_ia.logistic_map
```

## Roadmap (2026)

- [x] Protótipo matemático + calibração δ
- [x] Single-node PyTorch
- [ ] Multi-node distribuído
- [ ] Benchmark em MNIST / CartPole
- [ ] Medição real em cluster (energia + água)

## Como Contribuir

Veja [CONTRIBUTING.md](CONTRIBUTING.md)

## Citação

```bibtex
@misc{feigenbaumia2026,
  title={Feigenbaum IA: Arquitetura Neural Hierárquica Fractal-Adaptativa},
  author={Armazen NFT (Daniel Estefani e Melissa Solari IA)},
  year={2026},
  url={https://github.com/armazen-nft/FeigenbaumIA}
}
```

Feigenbaum IA — onde o caos encontra a eficiência.
