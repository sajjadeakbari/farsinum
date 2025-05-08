# farsinum/text_analyzer.py

import re
from typing import List

# برای سادگی، از کاراکترهای پایانی جمله استاندارد استفاده می‌کنیم.
# برای دقت بیشتر، می‌توان موارد استثنا (مانند Ph.D.) را در نظر گرفت.
_SENTENCE_TERMINATORS = r"[.!?؟]+" # یک یا چند پایانه جمله
_PARAGRAPH_SEPARATOR = r"\n\s*\n" # دو یا چند خط جدید، با فضای خالی احتمالی بینشان

def count_words(text: str) -> int:
    """
    تعداد کلمات در متن را شمارش می‌کند.
    کلمات با فاصله از هم جدا می‌شوند. علائم نگارشی چسبیده به کلمات جزئی از کلمه حساب نمی‌شوند
    (پس از جداسازی با فاصله، رشته‌های خالی فیلتر می‌شوند).
    """
    if not isinstance(text, str):
        raise TypeError("ورودی باید از نوع رشته باشد.")
    if not text.strip():
        return 0
    
    # حذف علائم نگارشی که ممکن است به کلمات چسبیده باشند برای شمارش دقیق‌تر "کلمه"
    # این یک راه ساده است، برای دقت بیشتر باید لیست کامل‌تری از علائم داشت
    # و یا از روش‌های توکن‌سازی پیشرفته‌تری استفاده کرد.
    # فعلا بر اساس جداسازی با فاصله و فیلتر کردن رشته‌های خالی عمل می‌کنیم.
    # یک راه بهتر: حذف علائم نگارشی و سپس split
    # text_without_punctuation = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE) # حذف هرچیزی جز حروف، اعداد و فاصله
    # words = text_without_punctuation.split()
    
    # روش فعلی: split بر اساس فاصله و سپس فیلتر
    words = re.split(r'\s+', text.strip()) # تقسیم بر اساس یک یا چند فاصله
    return len([word for word in words if word]) # فیلتر کردن رشته‌های خالی احتمالی

def count_sentences(text: str) -> int:
    """
    تعداد جملات در متن را شمارش می‌کند.
    جملات با کاراکترهای پایانی استاندارد (. ! ؟) از هم جدا می‌شوند.
    """
    if not isinstance(text, str):
        raise TypeError("ورودی باید از نوع رشته باشد.")
    if not text.strip():
        return 0
    
    # تقسیم متن بر اساس پایان‌دهنده‌های جمله
    # و فیلتر کردن رشته‌های خالی که ممکن است در اثر چند پایان‌دهنده پشت سر هم ایجاد شوند.
    sentences = re.split(_SENTENCE_TERMINATORS, text)
    # اگر متنی با نقطه تمام نشود، آخرین بخش هم یک جمله حساب می‌شود (اگر خالی نباشد).
    # re.split اگر با جداکننده تمام شود، یک رشته خالی در انتها ایجاد می‌کند.
    # مثال: "سلام. خوبی؟" -> ["سلام", " خوبی", ""]
    # "سلام" -> ["سلام"]
    
    count = 0
    for s in sentences:
        if s.strip(): # اگر بخشی از متن (پس از جداسازی) محتوا داشته باشد
            count += 1
    return count if count > 0 else (1 if text.strip() else 0) # اگر هیچ جداکننده‌ای نبود ولی متن وجود داشت، یک جمله است

def count_paragraphs(text: str) -> int:
    """
    تعداد پاراگراف‌ها در متن را شمارش می‌کند.
    پاراگراف‌ها با یک یا چند خط خالی از هم جدا می‌شوند.
    """
    if not isinstance(text, str):
        raise TypeError("ورودی باید از نوع رشته باشد.")
    if not text.strip():
        return 0
        
    # پاراگراف‌ها با دو یا چند خط جدید از هم جدا می‌شوند
    paragraphs = re.split(_PARAGRAPH_SEPARATOR, text.strip())
    # فیلتر کردن پاراگراف‌های خالی که ممکن است در اثر جداکننده‌های متعدد ایجاد شوند
    count = len([p for p in paragraphs if p.strip()])
    return count if count > 0 else (1 if text.strip() else 0)
