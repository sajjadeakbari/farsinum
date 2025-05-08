# farsinum/seo_analyzer.py

import re
from typing import List, Dict, Optional, Any, Tuple
from collections import Counter
from .text_normalizer import persian_text_normalizer # برای پیش‌پردازش متن
from .text_analyzer import count_words, count_sentences # برای معیارهای خوانایی

# برای استخراج تگ‌های عنوان و توضیحات از HTML (در صورت نیاز)
# فعلا از آن استفاده نمی‌کنیم و روی تحلیل متن خام تمرکز داریم.
# from bs4 import BeautifulSoup # اگر بخواهیم HTML را تجزیه کنیم

# مقادیر پیشنهادی برای سئو (اینها فقط پیشنهاد هستند و باید با تحقیق بیشتر تنظیم شوند)
RECOMMENDED_MIN_WORD_COUNT = 300
RECOMMENDED_KEYWORD_DENSITY_MIN = 0.01  # 1%
RECOMMENDED_KEYWORD_DENSITY_MAX = 0.03  # 3%
RECOMMENDED_AVG_SENTENCE_LENGTH_MAX = 25 # کلمه در جمله

class SEOResult:
    """کلاسی برای نگهداری نتایج تحلیل سئو."""
    def __init__(self, check_name: str, passed: bool, message: str, value: Any = None, details: Optional[Dict] = None):
        self.check_name = check_name
        self.passed = passed # آیا این بررسی با موفقیت انجام شده (معیار را برآورده کرده)؟
        self.message = message # پیامی برای کاربر
        self.value = value     # مقدار محاسبه شده (مثلاً تعداد کلمات)
        self.details = details or {} # جزئیات بیشتر در صورت نیاز

    def __repr__(self) -> str:
        return f"SEOResult(check='{self.check_name}', passed={self.passed}, message='{self.message}', value={self.value})"

    def to_dict(self) -> Dict:
        return {
            "check_name": self.check_name,
            "passed": self.passed,
            "message": self.message,
            "value": self.value,
            "details": self.details
        }

def _preprocess_text_for_seo(text: str, normalize: bool = True) -> str:
    """پیش‌پردازش متن برای تحلیل سئو (نرمال‌سازی و تبدیل به حروف کوچک)."""
    if normalize:
        text = persian_text_normalizer(text)
    return text.lower() # برای شمارش کلمات کلیدی بدون حساسیت به بزرگی و کوچکی (در فارسی کمتر مهم است)

def check_text_length(text: str, min_word_count: int = RECOMMENDED_MIN_WORD_COUNT) -> SEOResult:
    """
    طول متن (تعداد کلمات) را بررسی می‌کند.
    """
    word_count = count_words(text) # از ماژول text_analyzer خودمان استفاده می‌کنیم
    passed = word_count >= min_word_count
    message = (
        f"تعداد کلمات متن {word_count} است. "
        f"{'این تعداد مناسب به نظر می‌رسد.' if passed else f'توصیه می‌شود متن حداقل {min_word_count} کلمه داشته باشد.'}"
    )
    return SEOResult("Text Length", passed, message, value=word_count, details={"min_recommended": min_word_count})

def check_keyword_density(
    text: str,
    keyword: str,
    normalize_text_and_keyword: bool = True,
    min_density: float = RECOMMENDED_KEYWORD_DENSITY_MIN,
    max_density: float = RECOMMENDED_KEYWORD_DENSITY_MAX
) -> SEOResult:
    """
    چگالی یک کلمه کلیدی خاص را در متن بررسی می‌کند.
    """
    if not keyword.strip():
        return SEOResult("Keyword Density", False, "کلمه کلیدی ارائه نشده است.", value=0, details={"keyword": keyword})

    processed_text = _preprocess_text_for_seo(text, normalize_text_and_keyword)
    processed_keyword = _preprocess_text_for_seo(keyword, normalize_text_and_keyword).strip()

    words = processed_text.split()
    total_words = len([word for word in words if word]) # شمارش دقیق کلمات پس از split

    if total_words == 0:
        return SEOResult("Keyword Density", False, "متن خالی است یا کلمه‌ای ندارد.", value=0,
                         details={"keyword": processed_keyword, "occurrences": 0, "total_words": 0})

    keyword_occurrences = words.count(processed_keyword)
    density = keyword_occurrences / total_words if total_words > 0 else 0

    passed = min_density <= density <= max_density
    message = (
        f"کلمه کلیدی '{processed_keyword}' {keyword_occurrences} بار در متن تکرار شده است. "
        f"چگالی: {density:.2%}. "
    )
    if passed:
        message += "چگالی کلمه کلیدی در محدوده مناسب قرار دارد."
    elif density < min_density:
        message += f"چگالی کمتر از حد توصیه شده ({min_density:.1%}) است. ممکن است نیاز به تکرار بیشتر کلمه کلیدی باشد."
    else: # density > max_density
        message += f"چگالی بیشتر از حد توصیه شده ({max_density:.1%}) است. این ممکن است به عنوان Keyword Stuffing تلقی شود."

    return SEOResult(
        "Keyword Density",
        passed,
        message,
        value=density,
        details={
            "keyword": processed_keyword,
            "occurrences": keyword_occurrences,
            "total_words": total_words,
            "min_recommended_density": min_density,
            "max_recommended_density": max_density
        }
    )

def check_headings_simple(text: str) -> SEOResult:
    """
    بررسی ساده برای وجود الگوهای شبیه به عنوان (H1, H2 و ...).
    این تابع خطوطی که با # شروع می‌شوند (مارک‌داون) یا خطوط کوتاه تک کلمه‌ای یا دو کلمه‌ای
    که در یک پاراگراف جدا هستند را به عنوان عنوان شناسایی می‌کند.
    این یک روش بسیار ابتدایی است.
    """
    lines = text.splitlines()
    headings_found: Dict[str, int] = {"H1 (Markdown)": 0, "H2 (Markdown)": 0, "H3+ (Markdown)": 0, "Short Line Heading": 0}
    
    h1_exists = False

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue

        # بررسی عناوین مارک‌داون
        if stripped_line.startswith("# "):
            headings_found["H1 (Markdown)"] += 1
            h1_exists = True
        elif stripped_line.startswith("## "):
            headings_found["H2 (Markdown)"] += 1
        elif stripped_line.startswith("###") or stripped_line.startswith("####") or \
             stripped_line.startswith("#####") or stripped_line.startswith("######"):
            headings_found["H3+ (Markdown)"] += 1
        
        # بررسی خطوط کوتاه (به عنوان یک معیار ساده برای عنوان در متن عادی)
        # اگر خط کوتاه باشد (مثلا کمتر از 5 کلمه) و پاراگراف خودش باشد (اطرافش خالی باشد یا نبوده باشد)
        # این بخش نیاز به تعریف دقیق‌تری از "پاراگراف جدا" دارد.
        # فعلا فقط خطوطی که کلمات کمی دارند را شمارش می‌کنیم.
        elif len(stripped_line.split()) <= 4 and len(stripped_line.split()) > 0:
             # این شرط برای جلوگیری از شمارش لیست‌ها یا موارد مشابه است
             if not re.match(r"^\s*[-*+]|\d+\.", stripped_line):
                headings_found["Short Line Heading"] += 1


    total_headings = sum(headings_found.values())
    passed = total_headings > 0 and h1_exists # حداقل یک H1 (مارک‌داون) و چند عنوان دیگر
    
    message = f"تعداد کل عناوین شناسایی شده (به روش ساده): {total_headings}. "
    if not h1_exists and headings_found["H1 (Markdown)"] == 0 :
        message += "به نظر می‌رسد عنوان اصلی (H1 با #) وجود ندارد یا شناسایی نشده. "
    if total_headings == 0:
        message += "هیچ عنوانی (مانند # H1, ## H2 یا خطوط کوتاه) شناسایی نشد. استفاده از عناوین به ساختار متن کمک می‌کند."
    elif passed:
        message += "استفاده از عناوین مناسب به نظر می‌رسد."
    else:
        message += "توصیه می‌شود از عناوین (به خصوص H1 برای عنوان اصلی و H2, H3 برای بخش‌ها) استفاده کنید."

    return SEOResult("Headings Usage", passed, message, value=total_headings, details=headings_found)


def check_readability_simple(text: str, max_avg_sentence_len: int = RECOMMENDED_AVG_SENTENCE_LENGTH_MAX) -> SEOResult:
    """
    بررسی ساده خوانایی متن بر اساس میانگین طول جمله.
    """
    num_words = count_words(text)
    num_sentences = count_sentences(text)

    if num_sentences == 0:
        return SEOResult("Readability (Avg Sentence Length)", False, "جمله‌ای برای تحلیل خوانایی یافت نشد.", value=0)

    avg_sentence_length = num_words / num_sentences
    passed = avg_sentence_length <= max_avg_sentence_len
    
    message = (
        f"میانگین طول جملات: {avg_sentence_length:.1f} کلمه در هر جمله. "
        f"{'این مقدار برای خوانایی مناسب به نظر می‌رسد.' if passed else f'جملات ممکن است کمی طولانی باشند (توصیه شده: حداکثر {max_avg_sentence_len} کلمه). کوتاه کردن جملات به خوانایی کمک می‌کند.'}"
    )
    return SEOResult(
        "Readability (Avg Sentence Length)",
        passed,
        message,
        value=avg_sentence_length,
        details={"total_words": num_words, "total_sentences": num_sentences, "max_recommended_avg_len": max_avg_sentence_len}
    )

# --- توابع مربوط به HTML (فعلا کامنت شده، در صورت نیاز می‌توان فعال کرد) ---
# def check_html_title_tag(html_content: str) -> SEOResult:
#     """بررسی وجود و طول تگ <title> در HTML."""
#     try:
#         soup = BeautifulSoup(html_content, 'html.parser')
#         title_tag = soup.find('title')
#         if title_tag and title_tag.string:
#             title_text = title_tag.string.strip()
#             # طول پیشنهادی برای تگ عنوان بین 50 تا 60 کاراکتر است
#             passed = 10 < len(title_text) < 70 # یک محدوده بازتر برای سادگی
#             message = f"تگ <title> پیدا شد: '{title_text}' (طول: {len(title_text)} کاراکتر). "
#             message += "طول مناسب به نظر می‌رسد." if passed else "طول تگ عنوان ممکن است خیلی کوتاه یا خیلی بلند باشد."
#             return SEOResult("HTML Title Tag", passed, message, value=title_text)
#         else:
#             return SEOResult("HTML Title Tag", False, "تگ <title> در HTML پیدا نشد یا خالی است.", value=None)
#     except Exception as e:
#         return SEOResult("HTML Title Tag", False, f"خطا در تجزیه HTML: {e}", value=None)

# def check_html_meta_description(html_content: str) -> SEOResult:
#     """بررسی وجود و طول تگ <meta name="description"> در HTML."""
#     try:
#         soup = BeautifulSoup(html_content, 'html.parser')
#         meta_tag = soup.find('meta', attrs={'name': 'description'})
#         if meta_tag and meta_tag.get('content'):
#             desc_text = meta_tag['content'].strip()
#             # طول پیشنهادی برای توضیحات متا بین 120 تا 158 کاراکتر است
#             passed = 50 < len(desc_text) < 170 # یک محدوده بازتر
#             message = f"تگ <meta name=\"description\"> پیدا شد: '{desc_text[:60]}...' (طول: {len(desc_text)} کاراکتر). "
#             message += "طول مناسب به نظر می‌رسد." if passed else "طول توضیحات متا ممکن است خیلی کوتاه یا خیلی بلند باشد."
#             return SEOResult("HTML Meta Description", passed, message, value=desc_text)
#         else:
#             return SEOResult("HTML Meta Description", False, "تگ <meta name=\"description\"> در HTML پیدا نشد یا محتوای آن خالی است.", value=None)
#     except Exception as e:
#         return SEOResult("HTML Meta Description", False, f"خطا در تجزیه HTML: {e}", value=None)

def run_seo_checklist_on_text(text: str, keyword: Optional[str] = None) -> List[SEOResult]:
    """
    مجموعه‌ای از بررسی‌های سئو را روی متن خام اجرا می‌کند.
    """
    results: List[SEOResult] = []

    results.append(check_text_length(text))
    if keyword:
        results.append(check_keyword_density(text, keyword))
    else:
        results.append(SEOResult("Keyword Density", False, "کلمه کلیدی برای بررسی چگالی ارائه نشده است.", value=0))
        
    results.append(check_headings_simple(text))
    results.append(check_readability_simple(text))
    
    return results

# def run_seo_checklist_on_html(html_content: str, keyword: Optional[str] = None) -> List[SEOResult]:
#     """
#     مجموعه‌ای از بررسی‌های سئو را روی محتوای HTML اجرا می‌کند.
#     شامل بررسی‌های متنی و بررسی‌های مخصوص HTML.
#     """
#     results: List[SEOResult] = []
#     try:
#         soup = BeautifulSoup(html_content, 'html.parser')
#         # استخراج متن اصلی از HTML برای تحلیل‌های متنی
#         # این روش ساده است و ممکن است متن‌های ناخواسته (منو، فوتر) را هم شامل شود.
#         # برای دقت بیشتر، باید تگ‌های اصلی محتوا (مانند <article>, <main>) انتخاب شوند.
#         body_tag = soup.find('body')
#         text_content = body_tag.get_text(separator=' ', strip=True) if body_tag else ""
#     except Exception:
#         text_content = "" # اگر HTML قابل تجزیه نباشد، متن خالی در نظر می‌گیریم

#     if not text_content and html_content: # اگر استخراج متن از body ناموفق بود ولی html_content وجود داشت
#         text_content = html_content # بازگشت به خود html_content برای تحلیل‌های متنی (به عنوان آخرین راه حل)


#     results.append(check_html_title_tag(html_content))
#     results.append(check_html_meta_description(html_content))
    
#     results.extend(run_seo_checklist_on_text(text_content, keyword))
    
#     return results
