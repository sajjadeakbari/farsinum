# farsinum/__init__.py

"""
Farsinum: یک کتابخانه پایتون برای کار با اعداد، ارقام، متن و تاریخ فارسی.
شامل توابعی برای تبدیل اعداد، تبدیل عدد به حروف، نرمال‌سازی متن فارسی،
تحلیل ساده متن و تبدیل تاریخ میلادی/شمسی.
"""

__version__ = "0.3.0" # افزایش نسخه

from .numeral_converter import to_persian_numerals, to_english_numerals
from .number_to_words import number_to_persian_words
from .text_normalizer import (
    persian_text_normalizer,
    # ... (بقیه import های text_normalizer)
    ZWNJ
)
from .text_analyzer import count_words, count_sentences, count_paragraphs
from .date_converter import ( # اضافه کردن ماژول جدید
    gregorian_to_jalali,
    jalali_to_gregorian,
    today_jalali,
    DEFAULT_GREGORIAN_FORMAT,
    DEFAULT_JALALI_FORMAT,
    COMMON_JALALI_FORMAT_WITH_DAY_NAME
)


# توابعی که می‌خواهیم با from farsinum import * در دسترس باشند
__all__ = [
    # Numeral Converter
    "to_persian_numerals",
    "to_english_numerals",
    # Number to Words
    "number_to_persian_words",
    # Text Normalizer
    "persian_text_normalizer",
    "normalize_characters", # اگر می‌خواهید اینها هم مستقیما قابل import باشند
    "cleanup_spacing",
    "standardize_quotes",
    "standardize_ellipsis",
    "add_zwnj_to_common_suffixes",
    "ZWNJ",
    # Text Analyzer
    "count_words",
    "count_sentences",
    "count_paragraphs",
    # Date Converter
    "gregorian_to_jalali",
    "jalali_to_gregorian",
    "today_jalali",
    "DEFAULT_GREGORIAN_FORMAT",
    "DEFAULT_JALALI_FORMAT",
    "COMMON_JALALI_FORMAT_WITH_DAY_NAME",
    # Version
    "__version__"
]
