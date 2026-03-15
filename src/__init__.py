"""Pacote principal da FeigenbaumIA."""

from .constants import FEIGENBAUM_ALPHA, FEIGENBAUM_DELTA
from .enochian import EnochianEmitter, EnochianToken, GlyphType
from .feigenbaum_mlp import FeignbaumLayer, FeignbaumMLP
from .fractal_memory import FractalMemory
from .logistic import logistic_sequence, logistic_step
from .melissa_bridge import MelissaBridge
from .poe_interface import PoEInterface
from .spawn_policy import FeigenbaumForest, Module

__all__ = [
    "FEIGENBAUM_DELTA",
    "FEIGENBAUM_ALPHA",
    "logistic_step",
    "logistic_sequence",
    "FeigenbaumForest",
    "Module",
    "FractalMemory",
    "EnochianEmitter",
    "EnochianToken",
    "GlyphType",
    "FeignbaumMLP",
    "FeignbaumLayer",
    "MelissaBridge",
    "PoEInterface",
]
