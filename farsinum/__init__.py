# farsinum/__init__.py

"""
Farsinum: یک کتابخانه پایتون برای کار با اعداد، ارقام و متن فارسی.
شامل توابعی برای تبدیل اعداد، تبدیل عدد به حروف، نرمال‌سازی متن فارسی و تحلیل ساده متن.
"""

__version__ = "0.2.0" # افزایش نسخه

from .numeral_converter import to_persian_numerals, to_english_numerals
from .number_to_words import number_to_persian_words
from .text_normalizer import (
    persian_text_normalizer,
    normalize_characters,
    cleanup_spacing,
    standardize_quotes,
    standardize_ellipsis,
    add_zwnj_to_common_suffixes,
    ZWNJ
)
from .text_analyzer import count_words, count_sentences, count_paragraphs


# توابعی که می‌خواهیم با from farsinum import * در دسترس باشند
__all__ = [
    # Numeral Converter
    "to_persian_numerals",
    "to_english_numerals",
    # Number to Words
    "number_to_persian_words",
    # Text Normalizer
    "persian_text_normalizer",
    "normalize_characters",
    "cleanup_spacing",
    "standardize_quotes",
    "standardize_ellipsis",
    "add_zwnj_to_common_suffixes",
    "ZWNJ",
    # Text Analyzer
    "count_words",
    "count_sentences",
    "count_paragraphs",
    # Version
    "__version__"
]
