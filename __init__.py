# farsinum/__init__.py

"""
Farsinum: یک کتابخانه پایتون برای کار با اعداد و ارقام فارسی.
شامل توابعی برای تبدیل اعداد انگلیسی/عربی به فارسی و برعکس،
و تبدیل اعداد به حروف فارسی.
"""

__version__ = "0.1.0" # این نسخه باید با setup.py و تگ گیت هماهنگ باشد

from .numeral_converter import to_persian_numerals, to_english_numerals
from .number_to_words import number_to_persian_words

# توابعی که می‌خواهیم با from farsinum import * در دسترس باشند
__all__ = [
    "to_persian_numerals",
    "to_english_numerals",
    "number_to_persian_words",
    "__version__"
]
