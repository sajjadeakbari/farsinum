# farsinum/number_to_words.py

from typing import List

_PERSIAN_ZERO = "صفر"
_PERSIAN_NEGATIVE = "منفی "
_PERSIAN_AND = " و "

_PERSIAN_UNITS: List[str] = [
    "", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"
]
_PERSIAN_TEENS: List[str] = [
    "ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده"
]
_PERSIAN_TENS: List[str] = [
    "", "", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود"
]
_PERSIAN_HUNDREDS: List[str] = [
    "", "یکصد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد"
]
_PERSIAN_SCALE: List[str] = [
    "", "هزار", "میلیون", "میلیارد", "تریلیون", "کوادریلیون" # اضافه کردن مقیاس‌های بیشتر در صورت نیاز
]


def _three_digit_to_persian(n: int) -> str:
    """یک عدد سه رقمی را به حروف فارسی تبدیل می‌کند."""
    if not 0 <= n <= 999:
        raise ValueError("عدد باید بین 0 و 999 باشد.")

    if n == 0:
        return "" # در حالت کلی صفر بخشی از عدد بزرگتر را نمایش نمی‌دهیم

    parts: List[str] = []
    hundred = n // 100
    remainder = n % 100

    if hundred > 0:
        parts.append(_PERSIAN_HUNDREDS[hundred])

    if remainder > 0:
        if remainder < 10:
            parts.append(_PERSIAN_UNITS[remainder])
        elif remainder < 20:
            parts.append(_PERSIAN_TEENS[remainder - 10])
        else:
            ten = remainder // 10
            unit = remainder % 10
            parts.append(_PERSIAN_TENS[ten])
            if unit > 0:
                parts.append(_PERSIAN_UNITS[unit])
    
    return _PERSIAN_AND.join(parts)


def number_to_persian_words(number: int) -> str:
    """
    یک عدد صحیح را به حروف فارسی تبدیل می‌کند.

    Args:
        number: عدد صحیح ورودی.

    Returns:
        رشته حروف فارسی معادل عدد.

    Example:
        >>> number_to_persian_words(0)
        'صفر'
        >>> number_to_persian_words(128)
        'یکصد و بیست و هشت'
        >>> number_to_persian_words(1001)
        'یک هزار و یک'
        >>> number_to_persian_words(25000)
        'بیست و پنج هزار'
        >>> number_to_persian_words(123456789)
        'یکصد و بیست و سه میلیون و چهارصد و پنجاه و شش هزار و هفتصد و هشتاد و نه'
        >>> number_to_persian_words(-42)
        'منفی چهل و دو'
    """
    if not isinstance(number, int):
        raise TypeError("ورودی باید عدد صحیح باشد.")

    if number == 0:
        return _PERSIAN_ZERO

    prefix = ""
    if number < 0:
        prefix = _PERSIAN_NEGATIVE
        number = abs(number)

    if number >= (1000 ** len(_PERSIAN_SCALE)):
        raise ValueError(f"عدد بسیار بزرگ است. حداکثر تا مقیاس {_PERSIAN_SCALE[-1]} پشتیبانی می‌شود.")

    parts: List[str] = []
    scale_index = 0

    while number > 0:
        if number % 1000 != 0:
            chunk_words = _three_digit_to_persian(number % 1000)
            if scale_index > 0: # برای هزار، میلیون و ...
                chunk_words += " " + _PERSIAN_SCALE[scale_index]
            parts.append(chunk_words)
        number //= 1000
        scale_index += 1
    
    # اتصال قطعات با " و "
    result = _PERSIAN_AND.join(reversed(parts))
    
    # پاکسازی " و " های اضافی احتمالی ناشی از منطق ساده شده
    # مثال: "یک هزار و  و یک" -> "یک هزار و یک"
    # این مورد با منطق فعلی _three_digit_to_persian کمتر پیش می آید
    # اما برای اطمینان:
    result = result.replace(f"{_PERSIAN_AND.strip()}  {_PERSIAN_AND.strip()}", _PERSIAN_AND) # " و  و "
    result = result.strip()

    return prefix + result
