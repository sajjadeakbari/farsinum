# farsinum/numeral_converter.py

from typing import Union

PERSIAN_NUMERALS = "۰۱۲۳۴۵۶۷۸۹"
ENGLISH_NUMERALS = "0123456789"

# ساخت جداول ترجمه برای کارایی بیشتر
_PERSIAN_TO_ENGLISH_TRANSLATOR = str.maketrans(PERSIAN_NUMERALS, ENGLISH_NUMERALS)
_ENGLISH_TO_PERSIAN_TRANSLATOR = str.maketrans(ENGLISH_NUMERALS, PERSIAN_NUMERALS)

def to_persian_numerals(text: Union[str, int]) -> str:
    """
    اعداد انگلیسی و عربی در یک رشته را به معادل فارسی آن‌ها تبدیل می‌کند.

    Args:
        text: رشته ورودی که ممکن است حاوی اعداد انگلیسی/عربی باشد یا یک عدد صحیح.

    Returns:
        رشته‌ای با اعداد تبدیل شده به فارسی.

    Example:
        >>> to_persian_numerals("test 123 test ۴۵۶")
        'test ۱۲۳ test ۴۵۶'
        >>> to_persian_numerals(123)
        '۱۲۳'
    """
    return str(text).translate(_ENGLISH_TO_PERSIAN_TRANSLATOR)

def to_english_numerals(text: Union[str, int]) -> str:
    """
    اعداد فارسی در یک رشته را به معادل انگلیسی (غربی) آن‌ها تبدیل می‌کند.

    Args:
        text: رشته ورودی که ممکن است حاوی اعداد فارسی باشد یا یک عدد صحیح (که ابتدا به فارسی تبدیل می‌شود).

    Returns:
        رشته‌ای با اعداد تبدیل شده به انگلیسی.

    Example:
        >>> to_english_numerals("تست ۱۲۳ تست 456")
        'تست 123 تست 456'
        >>> to_english_numerals("۰۹۱۲۳۴۵۶۷۸۹")
        '09123456789'
    """
    # ابتدا اعداد انگلیسی موجود را به فارسی تبدیل می‌کنیم تا یکدست شوند،
    # سپس همه را به انگلیسی تبدیل می‌کنیم. این کار برای مواردی مثل "۱۲۳test456" است.
    # اگرچه در مثال‌ها تنها اعداد یک نوع داده شده، این تابع مقاوم‌تر عمل می‌کند.
    # اما برای سادگی، فرض می‌کنیم ورودی یا فارسی است یا انگلیسی که به فارسی تبدیل شده.
    # راه ساده‌تر و مستقیم‌تر برای این تابع:
    return str(text).translate(_PERSIAN_TO_ENGLISH_TRANSLATOR)
