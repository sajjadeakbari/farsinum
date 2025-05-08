# farsinum/longtail_keyword_generator.py

from typing import List, Set, Optional, Union, Iterable
import itertools # برای تولید ترکیبات
from .text_normalizer import persian_text_normalizer # برای یکسان‌سازی ورودی‌ها

# لیست‌های پیش‌فرض برای تولید کلمات کلیدی طولانی
# این لیست‌ها می‌توانند بسیار گسترده‌تر باشند و از فایل خوانده شوند.

# کلمات پرسشی رایج
QUESTION_PREFIXES: List[str] = [
    "چگونه", "چطور", "چرا", "چیست", "کدام", "کجا", "بهترین", "ارزانترین", "سریعترین",
    "آموزش", "راهنمای", "روش", "نحوه", "قیمت", "خرید", "فروش", "دانلود",
    "برای", "در مورد", "درباره"
]

# عبارات یا کلمات تکمیلی که می‌توانند به انتهای کلمه کلیدی اضافه شوند
COMMON_SUFFIXES: List[str] = [
    "چیست", "کجاست", "آنلاین", "رایگان", "با قیمت مناسب", "در تهران", "در ایران",
    "برای مبتدیان", "پیشرفته", "جدید", "۲۰۲۴", "۱۴۰۳", # سال‌ها
    "تصویری", "ویدئویی", "مقاله", "پادکست"
]

# کلماتی که می‌توانند بین کلمات کلیدی اصلی و کلمات پرسشی/تکمیلی قرار بگیرند
CONNECTING_WORDS: List[str] = ["برای", "در", "از", "با", "و"]


def _normalize_keywords(keywords: Union[str, Iterable[str]]) -> List[str]:
    """کلمات کلیدی ورودی را نرمال‌سازی و به لیست تبدیل می‌کند."""
    if isinstance(keywords, str):
        # اگر یک رشته با کلمات جدا شده با ویرگول یا فاصله باشد
        # ابتدا با ویرگول جدا می‌کنیم، سپس با فاصله
        processed_keywords = []
        for part in keywords.split(','):
            processed_keywords.extend(part.strip().split())
        
        # حذف رشته‌های خالی که ممکن است ایجاد شده باشند
        normalized = [persian_text_normalizer(kw.strip()) for kw in processed_keywords if kw.strip()]

    elif isinstance(keywords, Iterable):
        normalized = [persian_text_normalizer(str(kw).strip()) for kw in keywords if str(kw).strip()]
    else:
        raise TypeError("ورودی keywords باید رشته یا مجموعه‌ای از رشته‌ها باشد.")
    
    return list(set(normalized)) # حذف موارد تکراری پس از نرمال‌سازی


def generate_longtail_keywords(
    seed_keywords: Union[str, List[str]],
    question_prefixes: Optional[List[str]] = None,
    common_suffixes: Optional[List[str]] = None,
    max_combinations: int = 2, # حداکثر تعداد کلمات کلیدی اصلی برای ترکیب با هم
    include_original: bool = True,
    min_length: int = 2, # حداقل تعداد کلمات در یک کلمه کلیدی طولانی پیشنهادی
    max_suggestions_per_seed: int = 20 # حداکثر تعداد پیشنهاد برای هر کلمه کلیدی اصلی یا ترکیب
) -> Set[str]:
    """
    کلمات کلیدی طولانی (long-tail) را بر اساس کلمات کلیدی اصلی (seed) تولید می‌کند.

    Args:
        seed_keywords: یک یا چند کلمه کلیدی اصلی، به صورت رشته (جدا شده با کاما یا فاصله) یا لیست.
        question_prefixes: لیست پیشوندهای پرسشی یا عبارات شروع کننده. اگر None باشد، از لیست پیش‌فرض استفاده می‌شود.
        common_suffixes: لیست پسوندهای رایج یا عبارات پایانی. اگر None باشد، از لیست پیش‌فرض استفاده می‌شود.
        max_combinations: حداکثر تعداد کلمات کلیدی اصلی که با هم ترکیب می‌شوند (مثلا اگر 2 باشد،
                          ترکیبات دوتایی از seed_keywords هم در نظر گرفته می‌شوند).
        include_original: آیا خود کلمات کلیدی اصلی هم در خروجی باشند.
        min_length: حداقل تعداد کلمات برای یک پیشنهاد طولانی معتبر.
        max_suggestions_per_seed: محدودیت برای تعداد پیشنهادات تولید شده از هر کلمه/ترکیب اصلی.

    Returns:
        مجموعه‌ای از رشته‌های کلمات کلیدی طولانی پیشنهادی.
    """
    if question_prefixes is None:
        question_prefixes = QUESTION_PREFIXES
    if common_suffixes is None:
        common_suffixes = COMMON_SUFFIXES

    normalized_seeds = _normalize_keywords(seed_keywords)
    if not normalized_seeds:
        return set()

    all_suggestions: Set[str] = set()
    if include_original:
        for seed in normalized_seeds:
            if len(seed.split()) >= min_length:
                all_suggestions.add(seed)

    # ایجاد ترکیبات از کلمات کلیدی اصلی
    seed_combinations: List[List[str]] = []
    for i in range(1, min(max_combinations, len(normalized_seeds)) + 1):
        for combo_tuple in itertools.permutations(normalized_seeds, i): # استفاده از جایگشت برای ترتیب‌های مختلف
            seed_combinations.append(list(combo_tuple))
    
    # اضافه کردن خود کلمات کلیدی اصلی به عنوان "ترکیب" تکی
    if max_combinations == 1 and not seed_combinations: # اگر فقط یک کلمه اصلی بود
         for seed in normalized_seeds:
            seed_combinations.append([seed])


    for current_seed_parts in seed_combinations:
        current_seed_phrase = " ".join(current_seed_parts)
        suggestions_for_current_seed: Set[str] = set()

        # 1. ترکیب با پیشوندهای پرسشی
        for prefix in question_prefixes:
            suggestion = f"{prefix} {current_seed_phrase}"
            if len(suggestion.split()) >= min_length:
                suggestions_for_current_seed.add(suggestion)
        
        # 2. ترکیب با پسوندهای رایج
        for suffix in common_suffixes:
            suggestion = f"{current_seed_phrase} {suffix}"
            if len(suggestion.split()) >= min_length:
                suggestions_for_current_seed.add(suggestion)

        # 3. ترکیب پیشوند + کلمه کلیدی + پسوند (ساده شده)
        # این بخش می‌تواند بسیار گسترده شود، فعلا یک حالت ساده
        # (برای جلوگیری از انفجار ترکیبات، این بخش را محدود می‌کنیم)
        if len(current_seed_parts) == 1: # فقط برای کلمات کلیدی تکی
            limited_prefixes = question_prefixes[:5] # محدود کردن تعداد برای این نوع ترکیب
            limited_suffixes = common_suffixes[:5]
            for prefix in limited_prefixes:
                for suffix in limited_suffixes:
                    # جلوگیری از پسوندهایی که خودشان پرسشی هستند (مانند چیست) بعد از پیشوند پرسشی
                    if suffix.lower() not in ["چیست", "کجاست"] or not any(q in prefix.lower() for q in ["چیست", "چگونه", "کجا"]):
                        suggestion = f"{prefix} {current_seed_phrase} {suffix}"
                        if len(suggestion.split()) >= min_length:
                            suggestions_for_current_seed.add(suggestion)
        
        # اعمال محدودیت تعداد پیشنهادات برای هر کلمه کلیدی اصلی
        if len(suggestions_for_current_seed) > max_suggestions_per_seed:
            # انتخاب تصادفی یا بر اساس اولویت (فعلا ساده‌ترین: برش لیست)
            # برای نتایج پایدارتر، می‌توان sort کرد و سپس برش داد
            # sorted_suggestions = sorted(list(suggestions_for_current_seed))
            # all_suggestions.update(sorted_suggestions[:max_suggestions_per_seed])
            
            # برای اینکه هر بار خروجی یکسان باشد (بدون sort که ممکن است کند باشد)
            # از یک لیست موقت استفاده می‌کنیم و برش می‌دهیم
            temp_list = list(suggestions_for_current_seed)
            all_suggestions.update(temp_list[:max_suggestions_per_seed])
        else:
            all_suggestions.update(suggestions_for_current_seed)

    return all_suggestions
