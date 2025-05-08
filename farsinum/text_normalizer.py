# farsinum/text_normalizer.py

import re
import unicodedata

# نگاشت برای کاراکترهای رایج عربی/فارسی
_CHARACTER_MAP = {
    'ك': 'ک',  # Arabic Kaf to Persian Keheh
    'ي': 'ی',  # Arabic Yeh to Persian Yeh
    'ئ': 'ی',  # Arabic Yeh Hamza Above to Persian Yeh (برای یکسان سازی بیشتر، اگرچه ئ کاربرد خاص خود را دارد)
              # می‌توان این مورد را اختیاری کرد یا با دقت بیشتری اعمال نمود. فعلا برای سادگی.
    'أ': 'ا',  # Arabic Alef with Hamza Above to Persian Alef
    'إ': 'ا',  # Arabic Alef with Hamza Below to Persian Alef
    'ٱ': 'ا',  # Arabic Alef with Wasla Above to Persian Alef
    'آ': 'آ',  # Arabic Alef with Madda Above to Persian Alef with Madda
    'ة': 'ه',  # Arabic Teh Marbuta to Persian Heh
    'ء': '',   # Arabic Hamza (معمولا به تنهایی نیاز به جایگزینی یا حذف دارد، بسته به زمینه)
              # فعلا حذف می‌کنیم، ممکن است نیاز به بررسی بیشتر داشته باشد.
    # ارقام عربی شرقی (که گاهی با فارسی اشتباه گرفته می‌شوند)
    '١': '۱',
    '٢': '۲',
    '٣': '۳',
    '٤': '۴',
    '٥': '۵',
    '٦': '۶',
    '٧': '۷',
    '٨': '۸',
    '٩': '۹',
    '٠': '۰',
}
_CHARACTER_TRANSLATOR = str.maketrans(_CHARACTER_MAP)

# کاراکتر نیم‌فاصله
ZWNJ = '\u200c'

def normalize_characters(text: str) -> str:
    """
    نرمال‌سازی کاراکترهای عربی رایج به معادل فارسی آن‌ها.
    همچنین ارقام عربی شرقی را به فارسی تبدیل می‌کند.
    """
    text = text.translate(_CHARACTER_TRANSLATOR)
    # استفاده از NFKC برای یکسان‌سازی بیشتر کاراکترهای ترکیبی و سازگار با کامپوزرها
    # این ممکن است برخی کاراکترهای فارسی خاص مانند تشدید را تغییر دهد، باید با دقت استفاده شود.
    # فعلا برای یکسان‌سازی کلی کاراکترها مناسب است.
    text = unicodedata.normalize('NFKC', text)
    return text

def cleanup_spacing(text: str) -> str:
    """
    پاک‌سازی فاصله‌گذاری‌های اشتباه:
    - حذف فضاهای اضافی متعدد.
    - حذف فضاهای ابتدایی و انتهایی خطوط و کل متن.
    - تبدیل چندین خط خالی به یک خط خالی.
    - اطمینان از وجود یک فاصله بعد از علائم نگارشی مانند نقطه، ویرگول و ...
      (اگر بعدشان حرف باشد).
    """
    # حذف فضاهای ابتدایی و انتهایی
    text = text.strip()
    # جایگزینی چندین فاصله با یک فاصله
    text = re.sub(r'[ \t]+', ' ', text)
    # حذف فاصله‌های قبل از علائم نگارشی خاص
    text = re.sub(r'\s+([؟!?٪ maxit؛،.:])', r'\1', text)
    # اطمینان از یک فاصله بعد از علائم نگارشی (اگر حرفی بعدش باشد)
    text = re.sub(r'([؟!?٪ maxit؛،.:])(?=[^\s\d؟!?٪ maxit؛،.:])', r'\1 ', text) # \d برای جلوگیری از فاصله در اعداد اعشاری
    # حذف فضاهای اضافی در خطوط خالی
    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    # تبدیل چندین خط خالی به یک خط خالی
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # اطمینان از اینکه ZWNJ با فاصله احاطه نشده باشد
    text = re.sub(rf'\s*{ZWNJ}\s*', ZWNJ, text)
    # حذف ZWNJ های متعدد پشت سر هم
    text = re.sub(rf'{ZWNJ}+', ZWNJ, text)
    return text.strip() # حذف فضای احتمالی ایجاد شده در انتهای متن

def normalize_line_breaks(text: str) -> str:
    """تبدیل انواع مختلف خط جدید به \\n."""
    return text.replace('\r\n', '\n').replace('\r', '\n')

def standardize_quotes(text: str) -> str:
    """تبدیل گیومه‌های انگلیسی ("") به فارسی («»)."""
    # این یک پیاده‌سازی ساده است و ممکن است برای موارد تودرتو یا پیچیده نیاز به بهبود داشته باشد.
    # تلاش برای جایگزینی "باز" و "بسته" به صورت جداگانه
    # این بخش نیاز به منطق دقیق تری برای تشخیص ابتدا و انتهای نقل قول دارد
    # فعلا یک جایگزینی ساده انجام می‌دهیم:
    text = text.replace('"', '«', 1) # اولین " را با « جایگزین کن
    text = text.replace('"', '»')   # بقیه " ها را با » جایگزین کن
                                      # این روش ساده‌انگارانه است.

    # یک روش بهتر می‌تواند بررسی فضای اطراف " باشد:
    # "abc" -> «abc»
    # text = re.sub(r'(?<!\w)"(.*?)"(?!\w)', r'«\1»', text) # این نیاز به بررسی بیشتر دارد

    # فعلا از روشی استفاده می‌کنیم که به طور متناوب جایگزین می‌کند
    # این روش هم ایده‌آل نیست اگر نقل قول‌های تکی وجود داشته باشد.
    count = 0
    new_text = []
    for char in text:
        if char == '"':
            if count % 2 == 0:
                new_text.append('«')
            else:
                new_text.append('»')
            count += 1
        else:
            new_text.append(char)
    return "".join(new_text)


def standardize_ellipsis(text: str) -> str:
    """تبدیل سه نقطه یا بیشتر (...) به کاراکتر استاندارد سه نقطه (…)."""
    return re.sub(r'\.{3,}', '…', text)

def add_zwnj_to_common_suffixes(text: str) -> str:
    """
    اضافه کردن نیم‌فاصله (ZWNJ) به پسوندهای رایج مانند "ها"، "تر"، "ترین".
    مثال: "کتاب ها" -> "کتاب‌ها", "خوب تر" -> "خوب‌تر"
    """
    # پسوند "ها"
    text = re.sub(r'(\S+)[\s_]ها(\s|\b|$)', rf'\1{ZWNJ}ها\2', text) # \S+ برای کلمات غیرفاصله
    # پسوندهای "تر" و "ترین"
    text = re.sub(r'(\S+)[\s_](تر|ترین)(\s|\b|$)', rf'\1{ZWNJ}\2\3', text)
    # پیشوندهای "می" و "نمی" (ساده شده)
    # این بخش بسیار پیچیده است و نیاز به لیست افعال و بررسی دقیق دارد.
    # فعلا یک تلاش ساده برای "می " و "نمی " که بعدشان فعل می‌آید.
    # مثال: "می رود" -> "می‌رود"
    # این regex ممکن است false positive زیادی داشته باشد.
    # text = re.sub(r'\b(می|نمی)[\s_]+(?!و|که|یا|اما|اگر|چون|تا|نه|بلکه)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+)\b', rf'\1{ZWNJ}\2', text)
    # برای پیشوندهای می/نمی، بهتر است از یک لیست افعال استفاده شود یا فعلا صرف نظر شود.
    return text

def persian_text_normalizer(text: str) -> str:
    """
    نرمال‌ساز جامع متن فارسی.
    شامل نرمال‌سازی کاراکترها، پاک‌سازی فاصله‌ها، استانداردسازی علائم نگارشی،
    و اضافه کردن نیم‌فاصله به موارد رایج.
    """
    if not isinstance(text, str):
        raise TypeError("ورودی باید از نوع رشته باشد.")

    text = normalize_line_breaks(text)
    text = normalize_characters(text) # اول نرمال‌سازی کاراکترها
    text = cleanup_spacing(text)
    text = standardize_quotes(text) # گیومه‌ها
    text = standardize_ellipsis(text) # سه نقطه
    text = add_zwnj_to_common_suffixes(text) # نیم‌فاصله برای پسوندها

    # پاک‌سازی نهایی فاصله‌ها پس از همه تغییرات
    text = cleanup_spacing(text)
    return text
