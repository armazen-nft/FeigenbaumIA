# Feigenbaum-Inspired Hierarchical Neural Architectures  
**Exploração da Constante Universal de Feigenbaum (δ ≈ 4.669) em Módulos Dinâmicos com Spawn/Prune**

**Versão 2.0 (revisada) — Março 2026**  
**Autor principal:** Daniel Estefani (Armazen NFT)  
**Colaboração IA:** Melissa Solari  
**Repositório:** https://github.com/armazen-nft/FeigenbaumIA  

**Nota de revisão (Mar/2026):** Este documento foi atualizado após revisão técnica externa. Claims quantitativos foram reduzidos a observações preliminares, o vínculo matemático foi explicitado e adicionamos um protocolo experimental reproduzível. O foco agora é demonstrar empiricamente a emergência/convergência de δ nas dinâmicas de spawn/prune.

## Resumo

Propomos investigar arquiteturas neurais hierárquicas nas quais o crescimento e a poda de módulos seguem a lei de escala universal da constante de Feigenbaum δ. Cada módulo é mapeado a um mapa logístico via normalização de ativações, e a política de spawn observa (ou guia) a razão entre “distâncias de bifurcação” nos estados internos.  

O objetivo central é verificar se essa dinâmica produz convergência numérica para δ ≈ 4.669, gerando uma estrutura fractal auto-similar que pode levar a maior eficiência computacional e sustentabilidade.  

Resultados preliminares em simulações puramente logísticas mostram convergência rápida. Experimentos em redes neurais reais (MNIST, CartPole) estão em planejamento (ver seção 5).  

**Palavras-chave:** Teoria do Caos, Constante de Feigenbaum, Arquiteturas Dinâmicas, Pruning Hierárquico, Sustentabilidade em ML.

## Abstract (NeurIPS style)

We investigate hierarchical neural architectures guided by the Feigenbaum constant δ ≈ 4.669201609. By mapping module activations to a logistic map and monitoring period-doubling ratios in hidden states, we explore whether spawn/prune policies can exhibit universal scaling. Preliminary synthetic results show convergence to δ; real-network experiments are outlined. This work contributes an original bridge between chaos theory and dynamic neural architectures.

---

## 1. Introdução e Motivação

Redes neurais modernas crescem de forma super-linear, gerando alto consumo energético e hídrico. Estruturas fractais da natureza, regidas por constantes universais como δ de Feigenbaum, sugerem um caminho alternativo de crescimento orgânico e eficiente.  

**Tese exploratória:** se conseguirmos fazer com que as dinâmicas de ativação de módulos MLP exibam razões de bifurcação convergindo para δ, poderemos construir arquiteturas que crescem de forma previsível em escala e potencialmente mais eficientes.

---

## 2. Fundamentação Matemática e Vínculo com Redes Neurais

### 2.1 Mapa Logístico e δ de Feigenbaum

(Ver Apêndice A para derivação completa e tabela de convergência.)

### 2.2 Mapeamento para Módulos MLP (definição explícita e honesta)

Para cada módulo definimos:
\[
\mathbf{h}_{t+1} = \sigma(W_t \mathbf{h}_t + b_t)
\]
\[
x_{t+1} = r_n \cdot \text{norm}(\mathbf{h}_{t+1}) \cdot (1 - \text{norm}(\mathbf{h}_{t+1}))
\]
onde norm(·) é min-max ou sigmoid normalizado para [0,1], e r_n é o parâmetro efetivo do nível n.

**Como medir bifurcações na rede (ponto chave da revisão):**
- Coleta-se a série temporal de x_t por módulo durante várias forward passes.
- Descarta-se transiente e conta-se o número de pontos distintos no atrator (período).
- Calcula-se a razão entre intervalos de r em que o período dobra.
- Spawn de módulo filho ocorre quando essa razão observada se aproxima de δ ± ε (ε = 0.05 por padrão).
- **Não impomos δ**; observamos se ele emerge naturalmente ou é reforçado pela política.

Essa é a ponte explícita entre caos clássico e deep learning — ainda em investigação.

### 2.3 Inspiração em Carvalho et al. (1999)

Carvalho, Vilela Mendes & Seixas (Physica D, 1999) propuseram redes de mapas acoplados no ponto de acumulação de Feigenbaum. Usamos essa ideia como inspiração conceitual, mas estendemos para camadas MLP modernas com pesos treináveis. O salto de mapas 1D acoplados para redes profundas é reconhecidamente não-trivial e constitui o principal desafio teórico deste trabalho.

---

## 3. Arquitetura Feigenbaum Module (PyTorch)

(Ver `src/feigenbaum_ia/neural_module.py` no repositório.)

Políticas adaptativas de threshold (divergência, utilidade, entropia) guiam spawn/prune. Módulos inativos são compactados em memória fractal (dicionário recursivo).

---

## 4. Resultados Preliminares

Em simulações puramente logísticas (Capítulo 1 corrigido):
- Convergência da razão para δ com erro < 5 % já no nível 6.
- Gráfico salvo automaticamente em `feigenbaum_bifurcation.png`.

**Não reportamos ainda reduções de memória/FLOPs em tarefas reais** — esses números serão gerados no protocolo experimental abaixo.

---

## 5. Protocolo Experimental Proposto (Foco para NeurIPS 2026)

Para transformar esta proposta em resultado publicável, seguiremos o seguinte protocolo reproduzível:

**Tarefas:**
- MNIST (classificação supervisionada)
- CartPole-v1 (reinforcement learning contínuo)

**Baselines claras:**
- MLP fixo equivalente
- Lottery Ticket Hypothesis (pruning estático)
- Dynamic Sparse Training (DST)

**Medição de δ:**
- Para cada módulo, registrar série temporal de x_t (ativação logisticada).
- Detectar automaticamente dobras de período via análise de atratores.
- Calcular razão sucessiva e verificar convergência para 4.669 ± 0.05.

**Métricas principais:**
- Erro na estimativa de δ
- Pico de memória GPU (torch.cuda.max_memory_allocated)
- FLOPs por época (torch.profiler)
- Acurácia / reward final

**Implementação:** notebook `notebooks/02_mnist_validation.ipynb` (a ser criado).

Esperamos publicar resultados completos até junho 2026.

---

## 6. Limitações e Trabalhos Futuros

- O vínculo entre mapa logístico e dinâmicas de MLP ainda é heurístico; não há prova teórica de universalidade em redes profundas.
- Resultados de eficiência energética são preliminares.
- Criptografia fractal (ver seção 7) é especulativa e requer análise criptográfica formal.

**Aplicações futuras (cautelosas):**
- IA de borda de baixo recurso
- Sistemas multi-agente com comunicação fractal
- Exploração especulativa em criptografia caótica (chaves geradas hierarquicamente), mas sem claims de segurança formal no momento.

---

## 7. Conclusão

A universalidade da constante de Feigenbaum oferece uma lei de escala elegante e independente de implementação. Este trabalho investiga se tal lei pode emergir em arquiteturas neurais dinâmicas. Os primeiros passos matemáticos e de simulação são promissores; o próximo passo crítico é a validação empírica rigorosa em tarefas reais.

Convidamos a comunidade a contribuir com experimentos e análises teóricas.

---

## Referências

- Feigenbaum, M. J. (1978). Quantitative universality... *Journal of Statistical Physics*.
- Carvalho, R., Vilela Mendes, R., Seixas, J. (1999). Feigenbaum networks. *Physica D*.
- (demais referências mantidas)

## Apêndice A — Detalhes Matemáticos da Constante de Feigenbaum

[Conteúdo idêntico ao da versão anterior — tabela de convergência, prova de universalidade, α — mantido integralmente por ser o ponto mais forte.]

## Apêndice B — Aplicações Potenciais em Criptografia Fractal (especulativo)

[Versão curta com disclaimer forte:]  
O mapa logístico é base conhecida de criptografia caótica. Uma extensão hierárquica guiada por δ poderia gerar chaves com estrutura fractal. No entanto, **não fazemos claims de segurança** sem análise formal de entropia, resistência a ataques diferenciais e testes NIST. Esta é uma direção exploratória futura.

---

**Fim da Monografia Revisada v2.0**
