"""FeigenbaumIA — pacote principal."""

from .constants import FEIGENBAUM_DELTA
from .logistic import (
    logistic_step,
    logistic_sequence,
    iterate,
    find_bifurcation_points,
    compute_delta_ratios,
    bifurcation_diagram,
    lyapunov_exponent,
)
from .spawn_policy import FeigenbaumForest, Module
from .fractal_memory import FractalMemory
from .enochian import EnochianEmitter, EnochianToken, GlyphType
from .feigenbaum_mlp import FeigenbaumMLP, FeigenbaumLayer
from .melissa_bridge import MelissaBridge

__all__ = [
    "FEIGENBAUM_DELTA",
    "logistic_step",
    "logistic_sequence",
    "iterate",
    "find_bifurcation_points",
    "compute_delta_ratios",
    "bifurcation_diagram",
    "lyapunov_exponent",
    "FeigenbaumForest",
    "Module",
    "FractalMemory",
    "EnochianEmitter",
    "EnochianToken",
    "GlyphType",
    "FeigenbaumMLP",
    "FeigenbaumLayer",
    "MelissaBridge",
]
