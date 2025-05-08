# farsinum/date_converter.py

import datetime
import jdatetime
from typing import Union, Optional, Tuple
from .numeral_converter import to_persian_numerals # برای نمایش تاریخ با ارقام فارسی

# فرمت‌های رایج برای ورودی و خروجی
DEFAULT_GREGORIAN_FORMAT = "%Y-%m-%d"
DEFAULT_JALALI_FORMAT = "%Y/%m/%d" # فرمت رایج فارسی
COMMON_JALALI_FORMAT_WITH_DAY_NAME = "%A %d %B %Y" # شنبه ۱ فروردین ۱۴۰۳

def _parse_gregorian_date(date_input: Union[str, datetime.date, datetime.datetime]) -> datetime.date:
    """
    ورودی تاریخ میلادی را تجزیه کرده و به شیء datetime.date تبدیل می‌کند.
    """
    if isinstance(date_input, datetime.datetime):
        return date_input.date()
    if isinstance(date_input, datetime.date):
        return date_input
    if isinstance(date_input, str):
        # تلاش برای تجزیه با فرمت‌های رایج
        formats_to_try = [
            DEFAULT_GREGORIAN_FORMAT,
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y%m%d"
        ]
        for fmt in formats_to_try:
            try:
                return datetime.datetime.strptime(date_input, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"فرمت تاریخ میلادی '{date_input}' قابل تشخیص نیست. از فرمت YYYY-MM-DD استفاده کنید.")
    raise TypeError("ورودی تاریخ میلادی باید رشته، datetime.date یا datetime.datetime باشد.")

def gregorian_to_jalali(
    g_date: Union[str, datetime.date, datetime.datetime],
    output_format: Optional[str] = DEFAULT_JALALI_FORMAT,
    use_persian_numerals: bool = True,
    locale: str = "fa_IR" # برای نام ماه‌ها و روزهای فارسی
) -> str:
    """
    تاریخ میلادی را به تاریخ شمسی (جلالی) تبدیل می‌کند.

    Args:
        g_date: تاریخ میلادی به صورت رشته (مثلاً "2023-03-21") یا شیء datetime.date/datetime.datetime.
        output_format: فرمت رشته خروجی شمسی (مانند "%Y/%m/%d").
                       اگر None باشد، یک تاپل (سال، ماه، روز) شمسی برمی‌گرداند.
        use_persian_numerals: اگر True باشد، اعداد در خروجی به فارسی تبدیل می‌شوند.
        locale: لوکیل برای نام ماه‌ها و روزهای هفته (پیش‌فرض 'fa_IR').

    Returns:
        رشته تاریخ شمسی فرمت شده یا تاپل (سال، ماه، روز) شمسی.

    Example:
        >>> gregorian_to_jalali("2023-03-21")
        '۱۴۰۲/۰۱/۰۱'
        >>> gregorian_to_jalali(datetime.date(2023, 10, 8), output_format="%d %B %Y")
        '۱۶ مهر ۱۴۰۲'
        >>> gregorian_to_jalali("2023-12-25", use_persian_numerals=False)
        '1402/10/04'
        >>> gregorian_to_jalali("2024-02-29", output_format=None)
        (1402, 12, 10)
    """
    parsed_g_date = _parse_gregorian_date(g_date)
    j_date_obj = jdatetime.date.fromgregorian(date=parsed_g_date)

    if output_format is None:
        return j_date_obj.year, j_date_obj.month, j_date_obj.day

    # تنظیم لوکیل برای jdatetime (اگر لازم باشد و jdatetime از آن پشتیبانی کند)
    # jdatetime به طور پیش‌فرض از نام‌های فارسی برای ماه‌ها و روزها استفاده می‌کند.
    # آرگومان locale بیشتر برای سازگاری با strftime استاندارد است.
    # jdatetime.set_locale(locale) # ممکن است در نسخه‌های جدیدتر نیازی نباشد یا روش دیگری داشته باشد

    # jdatetime.date.strftime از لوکیل سیستم برای نام ماه‌ها و روزها استفاده می‌کند
    # برای اطمینان از فارسی بودن، می‌توانیم خودمان یک نگاشت داشته باشیم یا از فرمت‌های عددی استفاده کنیم
    # و سپس با to_persian_numerals اعداد را فارسی کنیم.
    # اما strftime خود jdatetime معمولا فارسی است.
    
    formatted_jalali_date = j_date_obj.strftime(output_format, locale=locale)

    if use_persian_numerals:
        return to_persian_numerals(formatted_jalali_date)
    return formatted_jalali_date


def _parse_jalali_date_str(j_date_str: str) -> Tuple[int, int, int]:
    """
    رشته تاریخ شمسی را تجزیه کرده و به (سال، ماه، روز) تبدیل می‌کند.
    اعداد فارسی و انگلیسی را پشتیبانی می‌کند.
    """
    from .numeral_converter import to_english_numerals # وارد کردن در صورت نیاز
    
    j_date_str_en_numerals = to_english_numerals(j_date_str)

    formats_to_try = [
        DEFAULT_JALALI_FORMAT, # %Y/%m/%d
        "%Y-%m-%d",
        # فرمت‌های دیگر را می‌توان اضافه کرد
    ]
    # تلاش برای جدا کردن با جداکننده‌های رایج
    parts = []
    if '/' in j_date_str_en_numerals:
        parts = j_date_str_en_numerals.split('/')
    elif '-' in j_date_str_en_numerals:
        parts = j_date_str_en_numerals.split('-')
    
    if len(parts) == 3:
        try:
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            # اعتبارسنجی اولیه مقادیر (jdatetime خودش اعتبارسنجی دقیق‌تر را انجام می‌دهد)
            if not (1000 <= year <= 1500 and 1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError("مقادیر تاریخ شمسی نامعتبر است.")
            return year, month, day
        except ValueError:
            pass # ادامه به تلاش با strptime

    # اگر جداکننده‌ها کار نکردند یا فرمت متفاوت بود، از strptime کتابخانه jdatetime استفاده می‌کنیم
    # این بخش نیاز به jdatetime.datetime.strptime دارد که تاریخ شمسی را تجزیه کند.
    # اما jdatetime.datetime.strptime مستقیماً رشته را به شیء jdatetime.datetime تبدیل می‌کند.
    # ما فقط به سال، ماه، روز نیاز داریم.
    # فعلا روی فرمت‌های ساده با جداکننده تمرکز می‌کنیم.
    # برای پشتیبانی کامل از strptime برای شمسی، باید jdatetime.datetime.strptime را استفاده کرد.
    
    raise ValueError(f"فرمت تاریخ شمسی '{j_date_str}' قابل تشخیص نیست. از فرمت YYYY/MM/DD یا YYYY-MM-DD با اعداد فارسی یا انگلیسی استفاده کنید.")


def jalali_to_gregorian(
    j_date: Union[str, Tuple[int, int, int], jdatetime.date, jdatetime.datetime],
    output_format: Optional[str] = DEFAULT_GREGORIAN_FORMAT
) -> Union[str, datetime.date]:
    """
    تاریخ شمسی (جلالی) را به تاریخ میلادی تبدیل می‌کند.

    Args:
        j_date: تاریخ شمسی به صورت:
                - رشته (مانند "۱۴۰۲/۰۱/۰۱" یا "1402-01-01")
                - تاپل (سال، ماه، روز) مانند (1402, 1, 1)
                - شیء jdatetime.date یا jdatetime.datetime
        output_format: فرمت رشته خروجی میلادی (مانند "%Y-%m-%d").
                       اگر None باشد، شیء datetime.date برمی‌گرداند.

    Returns:
        رشته تاریخ میلادی فرمت شده یا شیء datetime.date.

    Example:
        >>> jalali_to_gregorian("۱۴۰۲/۰۱/۰۱")
        '2023-03-21'
        >>> jalali_to_gregorian((1402, 7, 16))
        '2023-10-08'
        >>> jalali_to_gregorian(jdatetime.date(1402, 10, 4), output_format=None)
        datetime.date(2023, 12, 25)
        >>> jalali_to_gregorian("1402-12-10") # سال کبیسه شمسی
        '2024-02-29'
    """
    j_date_obj: jdatetime.date
    if isinstance(j_date, (jdatetime.date, jdatetime.datetime)):
        if isinstance(j_date, jdatetime.datetime):
            j_date_obj = j_date.date()
        else:
            j_date_obj = j_date # type: ignore
    elif isinstance(j_date, tuple) and len(j_date) == 3:
        try:
            j_date_obj = jdatetime.date(j_date[0], j_date[1], j_date[2])
        except ValueError as e: # برای خطاهای مربوط به تاریخ نامعتبر شمسی
            raise ValueError(f"تاریخ شمسی ورودی نامعتبر است: {e}")
    elif isinstance(j_date, str):
        year, month, day = _parse_jalali_date_str(j_date)
        try:
            j_date_obj = jdatetime.date(year, month, day)
        except ValueError as e:
            raise ValueError(f"تاریخ شمسی ورودی نامعتبر است: {e}")
    else:
        raise TypeError("ورودی تاریخ شمسی باید رشته، تاپل (سال، ماه، روز)، jdatetime.date یا jdatetime.datetime باشد.")

    g_date_obj = j_date_obj.togregorian()

    if output_format is None:
        return g_date_obj
    
    return g_date_obj.strftime(output_format)

def today_jalali(
    output_format: Optional[str] = DEFAULT_JALALI_FORMAT,
    use_persian_numerals: bool = True,
    locale: str = "fa_IR"
) -> str:
    """
    تاریخ امروز را به صورت شمسی برمی‌گرداند.

    Args:
        output_format: فرمت رشته خروجی شمسی.
        use_persian_numerals: اگر True باشد، اعداد در خروجی به فارسی تبدیل می‌شوند.
        locale: لوکیل برای نام ماه‌ها و روزهای هفته.

    Returns:
        رشته تاریخ شمسی امروز.

    Example:
        >>> # فرض کنید امروز ۱۶ مهر ۱۴۰۲ است (۲۰۲۳/۱۰/۰۸)
        >>> # today_jalali()
        '۱۴۰۲/۰۷/۱۶'
        >>> # today_jalali(output_format=COMMON_JALALI_FORMAT_WITH_DAY_NAME)
        'یکشنبه ۱۶ مهر ۱۴۰۲'
    """
    now_gregorian = datetime.date.today()
    return gregorian_to_jalali(now_gregorian, output_format, use_persian_numerals, locale)
