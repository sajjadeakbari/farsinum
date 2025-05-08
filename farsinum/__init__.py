# farsinum/__init__.py

"""
Farsinum: کتابخانه جامع پایتون برای کار با زبان و داده‌های فارسی.
شامل تبدیل اعداد، عدد به حروف، نرمال‌سازی متن، تحلیل متن، تبدیل تاریخ و تحلیل احساسات ساده.
"""

__version__ = "0.4.0" # افزایش نسخه

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
from .date_converter import (
    gregorian_to_jalali,
    jalali_to_gregorian,
    today_jalali,
    DEFAULT_GREGORIAN_FORMAT,
    DEFAULT_JALALI_FORMAT,
    COMMON_JALALI_FORMAT_WITH_DAY_NAME
)
from .sentiment_analyzer import ( # اضافه کردن ماژول جدید
    analyze_sentiment_simple,
    SentimentLabel, # اگر کاربران بخواهند از این تایپ استفاده کنند
    SentimentScore
)
from .sentiment_analyzer import (
    analyze_sentiment_simple,
    SentimentLabel,
    SentimentScore
)
from .seo_analyzer import ( # اضافه کردن ماژول جدید
    SEOResult,
    check_text_length,
    check_keyword_density,
    check_headings_simple,
    check_readability_simple,
    run_seo_checklist_on_text,
    # RECOMMENDED_MIN_WORD_COUNT, # اینها معمولا به عنوان ثابت در __all__ نمی‌آیند
    # RECOMMENDED_KEYWORD_DENSITY_MIN,
    # RECOMMENDED_KEYWORD_DENSITY_MAX,
    # RECOMMENDED_AVG_SENTENCE_LENGTH_MAX
)

# توابعی که می‌خواهیم با from farsinum import * در دسترس باشند
__all__ = [
    # Numeral Converter
    "to_persian_numerals", "to_english_numerals",
    # Number to Words
    "number_to_persian_words",
    # Text Normalizer
    "persian_text_normalizer", "normalize_characters", "cleanup_spacing",
    "standardize_quotes", "standardize_ellipsis", "add_zwnj_to_common_suffixes", "ZWNJ",
    # Text Analyzer
    "count_words", "count_sentences", "count_paragraphs",
    # Date Converter
    "gregorian_to_jalali", "jalali_to_gregorian", "today_jalali",
    "DEFAULT_GREGORIAN_FORMAT", "DEFAULT_JALALI_FORMAT", "COMMON_JALALI_FORMAT_WITH_DAY_NAME",
    # Sentiment Analyzer
    "analyze_sentiment_simple", "SentimentLabel", "SentimentScore",
    # Version
    "__version__"
]
