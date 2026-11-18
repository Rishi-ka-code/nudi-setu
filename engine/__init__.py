# -*- coding: utf-8 -*-
"""
Kannada Dialect to Textbook Kannada Conversion Engine
"""

from .dialect_detector import DialectDetector
from .morph_analyzer import MorphAnalyzer
from .normalizer import DialectNormalizer

__all__ = ["DialectDetector", "MorphAnalyzer", "DialectNormalizer"]

