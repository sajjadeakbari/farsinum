# Farsinum (کتابخانه پایتون)

[![PyPI version](https://badge.fury.io/py/farsinum.svg)](https://badge.fury.io/py/farsinum)

<!-- بعد از انتشار در PyPI، لینک بالا فعال می‌شود -->
<!-- می‌توانید بج‌ها و اطلاعات بیشتری اضافه کنید -->

یک کتابخانه پایتون  و کارآمد برای کار با اعداد و ارقام فارسی.

این پکیج شامل توابع زیر است:
*   تبدیل اعداد انگلیسی (یا عربی) به معادل فارسی آن‌ها در یک رشته.
*   تبدیل اعداد فارسی به معادل انگلیسی (غربی) آن‌ها در یک رشته.
*   تبدیل اعداد صحیح به حروف فارسی.

## نصب

می‌توانید `farsinum` را با استفاده از pip نصب کنید:


```bash
pip install farsinum
```




## نرمال‌سازی متن فارسی

پکیج `farsinum` شامل توابعی برای پاک‌سازی و استانداردسازی متن‌های فارسی است.


```python
from farsinum import persian_text_normalizer, ZWNJ

dirty_text = '  اين يك متن نمونه با كاراكترهاي عربي (ك، ي) و اعداد ١٢٣ و فاصله هاي اضافي است... كتاب ها "عالي" اند!  '
normalized_text = persian_text_normalizer(dirty_text)
print(normalized_text)
```

# خروجی تقریبی (بسته به جزئیات پیاده‌سازی):
# این یک متن نمونه با کاراکترهای عربی (ک، ی) و اعداد ۱۲۳ و فاصله های اضافی است… کتاب‌ها «عالی» اند!



توابع جزئی‌تر نیز در دسترس هستند:
* `normalize_characters(text)`
* `cleanup_spacing(text)`
* `standardize_quotes(text)`
* `standardize_ellipsis(text)`
* `add_zwnj_to_common_suffixes(text)`
* `ZWNJ` (کاراکتر نیم‌فاصله)



و برای تحلیل متن:

## تحلیل ساده متن فارسی

توابعی برای شمارش کلمات، جملات و پاراگراف‌ها:


```python
from farsinum import count_words, count_sentences, count_paragraphs

text = """این پاراگراف اول است. شامل دو جمله می‌باشد!
گاهی اوقات جملات طولانی هستند؟

این پاراگراف دوم است.
فقط یک جمله دارد.
"""

print(f"تعداد کلمات: {count_words(text)}")
print(f"تعداد جملات: {count_sentences(text)}")
print(f"تعداد پاراگراف‌ها: {count_paragraphs(text)}")

# خروجی:
# تعداد کلمات: 22 (یا نزدیک به این، بسته به نحوه شمارش کلمات با علائم)
# تعداد جملات: 4
# تعداد پاراگراف‌ها: 2

## تبدیل تاریخ میلادی و شمسی

`farsinum` امکان تبدیل بین تاریخ‌های میلادی و شمسی (جلالی) را با استفاده از کتابخانه `jdatetime` فراهم می‌کند و رابط کاربری ساده‌ای برای فرمت‌های رایج ارائه می‌دهد.

```python
import datetime
from farsinum import gregorian_to_jalali, jalali_to_gregorian, today_jalali

# تبدیل میلادی به شمسی
g_date_str = "2023-10-08"
jalali_date_str = gregorian_to_jalali(g_date_str)
print(f"{g_date_str} میلادی برابر است با {jalali_date_str} شمسی")
# خروجی: 2023-10-08 میلادی برابر است با ۱۴۰۲/۰۷/۱۶ شمسی

dt_obj = datetime.date(2024, 2, 29) # سال کبیسه میلادی
jalali_formatted = gregorian_to_jalali(dt_obj, output_format="%A %d %B %Y", use_persian_numerals=True)
print(f"تاریخ {dt_obj} به شمسی: {jalali_formatted}")
# خروجی: تاریخ 2024-02-29 به شمسی: پنجشنبه ۱۰ اسفند ۱۴۰۲ (بسته به لوکیل)

# تبدیل شمسی به میلادی
j_date_str = "۱۴۰۲/۰۱/۰۱"
gregorian_date_str = jalali_to_gregorian(j_date_str)
print(f"{j_date_str} شمسی برابر است با {gregorian_date_str} میلادی")
# خروجی: ۱۴۰۲/۰۱/۰۱ شمسی برابر است با 2023-03-21 میلادی

gregorian_date_obj = jalali_to_gregorian((1402, 12, 29), output_format=None) # آخرین روز سال ۱۴۰۲ (غیر کبیسه)
print(f"آخرین روز ۱۴۰۲ به میلادی: {gregorian_date_obj}")
# خروجی: آخرین روز ۱۴۰۲ به میلادی: 2024-03-19

# تاریخ امروز به شمسی
print(f"امروز به شمسی: {today_jalali()}")
print(f"امروز (با فرمت کامل): {today_jalali(output_format='%A، %d %B %Y')}")

## تحلیل اولیه سئو متن فارسی

`farsinum` ابزارهای ساده‌ای برای بررسی برخی جنبه‌های اولیه سئو محتوای متنی فارسی ارائه می‌دهد.

```python
from farsinum import run_seo_checklist_on_text, SEOResult

my_article_text = """
# عنوان اصلی مقاله من
این یک مقاله نمونه درباره بهینه‌سازی برای موتورهای جستجو است.
در این مقاله، به بررسی نکات کلیدی سئو می‌پردازیم. سئو برای موفقیت آنلاین حیاتی است.
متن باید به اندازه کافی طولانی باشد و کلمات کلیدی مناسبی داشته باشد.
کلمه کلیدی اصلی ما "سئو" است.

## نکات مهم در سئو محتوا
- تحقیق کلمات کلیدی
- تولید محتوای با کیفیت (سئو داخلی)
- لینک‌سازی (سئو خارجی)

سئو یک دانش در حال تغییر است.
"""

keyword_to_check = "سئو"
seo_results = run_seo_checklist_on_text(my_article_text, keyword=keyword_to_check)

print(f"نتایج بررسی سئو برای کلمه کلیدی '{keyword_to_check}':")
for result in seo_results:
    print(f"  - بررسی: {result.check_name}")
    print(f"    وضعیت: {'موفق' if result.passed else 'نیاز به بهبود'}")
    print(f"    پیام: {result.message}")
    print(f"    مقدار: {result.value}")
    if result.details:
        print(f"    جزئیات: {result.details}")
    print("-" * 20)

# مثال خروجی (مقادیر و پیام‌ها ممکن است متفاوت باشند):
# نتایج بررسی سئو برای کلمه کلیدی 'سئو':
#   - بررسی: Text Length
#     وضعیت: نیاز به بهبود
#     پیام: تعداد کلمات متن 50 است. توصیه می‌شود متن حداقل 300 کلمه داشته باشد.
#     مقدار: 50
#     جزئیات: {'min_recommended': 300}
# --------------------
#   - بررسی: Keyword Density
#     وضعیت: نیاز به بهبود  (یا موفق، بسته به چگالی واقعی و تنظیمات)
#     پیام: کلمه کلیدی 'سئو' 4 بار در متن تکرار شده است. چگالی: 8.00%. چگالی بیشتر از حد توصیه شده (3.0%) است...
#     مقدار: 0.08
#     جزئیات: {'keyword': 'سئو', 'occurrences': 4, 'total_words': 50, ...}
# --------------------
#   - بررسی: Headings Usage
#     وضعیت: موفق
#     پیام: تعداد کل عناوین شناسایی شده (به روش ساده): 2. استفاده از عناوین مناسب به نظر می‌رسد.
#     مقدار: 2
#     جزئیات: {'H1 (Markdown)': 1, 'H2 (Markdown)': 1, ...}
# --------------------
#   - بررسی: Readability (Avg Sentence Length)
#     وضعیت: موفق
#     پیام: میانگین طول جملات: 10.0 کلمه در هر جمله. این مقدار برای خوانایی مناسب به نظر می‌رسد.
#     مقدار: 10.0
#     جزئیات: {'total_words': 50, 'total_sentences': 5, ...}
# --------------------



