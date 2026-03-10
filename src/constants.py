"""
Constantes universais do projeto.
δ (delta) de Feigenbaum: razão de convergência das bifurcações logísticas.
α (alpha) de Feigenbaum: razão de escala do eixo do atrator.
"""

FEIGENBAUM_DELTA = 4.669201609102990671853203821578  # δ
FEIGENBAUM_ALPHA = 2.502907875095892822283902873218  # α

# Limites do mapa logístico
R_ONSET = 3.0
R_CHAOS = 3.56995
R_MAX = 4.0

# Política de spawn/prune
SPAWN_THRESHOLD = 0.85
PRUNE_THRESHOLD = 0.15
