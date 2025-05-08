# farsinum/sentiment_analyzer.py

import os
import pkgutil # برای خواندن فایل‌های داده از داخل پکیج
from typing import Set, Dict, Tuple, Literal
from .text_normalizer import persian_text_normalizer # برای نرمال‌سازی متن ورودی

# مسیر فایل‌های واژگان نسبت به این فایل
_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
_POSITIVE_WORDS_FILE = os.path.join(_DATA_PATH, 'positive_words_fa.txt')
_NEGATIVE_WORDS_FILE = os.path.join(_DATA_PATH, 'negative_words_fa.txt')

# استفاده از pkgutil برای خواندن فایل‌ها به روشی که با نصب پکیج هم کار کند
try:
    _positive_lexicon_bytes = pkgutil.get_data('farsinum', 'data/positive_words_fa.txt')
    _negative_lexicon_bytes = pkgutil.get_data('farsinum', 'data/negative_words_fa.txt')

    if _positive_lexicon_bytes is None or _negative_lexicon_bytes is None:
        raise FileNotFoundError("فایل‌های واژگان احساسات یافت نشدند.")

    _POSITIVE_WORDS: Set[str] = set(
        line.strip() for line in _positive_lexicon_bytes.decode('utf-8').splitlines() if line.strip()
    )
    _NEGATIVE_WORDS: Set[str] = set(
        line.strip() for line in _negative_lexicon_bytes.decode('utf-8').splitlines() if line.strip()
    )
except (FileNotFoundError, UnicodeDecodeError, AttributeError) as e:
    # در صورتی که در زمان توسعه فایل‌ها مستقیما خوانده شوند (نه از طریق pkgutil)
    # یا خطایی در خواندن رخ دهد، یک هشدار یا مقدار پیش‌فرض در نظر می‌گیریم.
    # این بخش برای robust بودن بیشتر است.
    print(f"هشدار: خطایی در بارگذاری واژگان احساسات رخ داد: {e}. تحلیل احساسات ممکن است دقیق نباشد.")
    _POSITIVE_WORDS: Set[str] = {"خوب", "عالی", "مثبت"} # مقادیر پیش‌فرض حداقلی
    _NEGATIVE_WORDS: Set[str] = {"بد", "ضعیف", "منفی"}

# کلمات تشدید کننده (intensifiers) و تضعیف کننده (downtoners) می‌توانند اضافه شوند
# مثال: "خیلی خوب" (تشدید مثبت)، "اصلا بد نیست" (تضعیف منفی یا حتی مثبت)
# فعلا برای سادگی از آن‌ها صرف نظر می‌کنیم.

SentimentLabel = Literal["positive", "negative", "neutral"]
SentimentScore = Dict[SentimentLabel, float]


def analyze_sentiment_simple(
    text: str,
    normalize_text: bool = True,
    neutral_threshold: float = 0.1 # آستانه برای خنثی در نظر گرفتن (اختلاف امتیاز مثبت و منفی)
) -> Tuple[SentimentLabel, SentimentScore]:
    """
    تحلیل احساسات ساده متن فارسی بر اساس لیست کلمات مثبت و منفی.

    Args:
        text: متن ورودی برای تحلیل.
        normalize_text: اگر True باشد، متن قبل از تحلیل با persian_text_normalizer نرمال‌سازی می‌شود.
        neutral_threshold: اگر قدر مطلق امتیاز نهایی کمتر از این مقدار باشد، احساس "خنثی" برگردانده می‌شود.
                           مقدار بین 0 و 1. 0 به معنی عدم وجود خنثی (فقط مثبت یا منفی).

    Returns:
        یک تاپل شامل:
        - برچسب احساس کلی (positive, negative, neutral).
        - دیکشنری امتیازات (مثبت، منفی، خنثی) که مجموعشان 1 است.

    Example:
        >>> analyze_sentiment_simple("این فیلم خیلی خوب و عالی بود.")
        ('positive', {'positive': 1.0, 'negative': 0.0, 'neutral': 0.0}) # امتیازات تقریبی
        >>> analyze_sentiment_simple("اصلا از خدمات راضی نبودم، خیلی بد بود.")
        ('negative', {'positive': 0.0, 'negative': 1.0, 'neutral': 0.0})
        >>> analyze_sentiment_simple("این یک کتاب است.")
        ('neutral', {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0})
    """
    if not isinstance(text, str):
        raise TypeError("ورودی باید از نوع رشته باشد.")

    if normalize_text:
        processed_text = persian_text_normalizer(text)
    else:
        processed_text = text
    
    # توکن‌سازی ساده بر اساس فاصله. برای دقت بیشتر می‌توان از توکن‌سازهای پیشرفته‌تر استفاده کرد.
    words = processed_text.lower().split() # تبدیل به حروف کوچک برای یکسان‌سازی (اگرچه در فارسی کمتر کاربرد دارد)

    positive_score = 0
    negative_score = 0

    for word in words:
        if word in _POSITIVE_WORDS:
            positive_score += 1
        elif word in _NEGATIVE_WORDS:
            negative_score += 1
            
    total_sentiment_words = positive_score + negative_score

    if total_sentiment_words == 0: # هیچ کلمه احساسی یافت نشد
        final_label: SentimentLabel = "neutral"
        scores: SentimentScore = {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
        return final_label, scores

    # محاسبه امتیاز نهایی (ساده)
    # می‌توان از روش‌های پیچیده‌تری مانند (pos - neg) / total_words یا (pos - neg) / (pos + neg) استفاده کرد.
    # در اینجا یک امتیاز نسبی بر اساس کلمات احساسی پیدا شده محاسبه می‌کنیم.
    # normalized_positive = positive_score / total_sentiment_words
    # normalized_negative = negative_score / total_sentiment_words
    
    # امتیاز کلی بین -1 (کاملا منفی) و +1 (کاملا مثبت)
    compound_score = (positive_score - negative_score) / total_sentiment_words


    if compound_score > neutral_threshold:
        final_label = "positive"
    elif compound_score < -neutral_threshold:
        final_label = "negative"
    else:
        final_label = "neutral"

    # تخصیص امتیازات نهایی به گونه‌ای که مجموعشان 1 شود (برای نمایش بهتر)
    # این یک روش ساده برای توزیع امتیاز است.
    if final_label == "positive":
        # امتیاز مثبت را بر اساس قدرت مثبت بودن می‌دهیم، بقیه صفر یا نزدیک به صفر
        # این بخش می‌تواند بهبود یابد تا توزیع دقیق‌تری از امتیازات ارائه دهد.
        # برای سادگی، اگر مثبت بود، امتیاز مثبت را 1 و بقیه را 0 می‌گذاریم (در این مدل ساده)
        # اما برای اینکه neutral_threshold معنی داشته باشد، باید امتیازات را دقیق‌تر حساب کنیم.
        p_score = (1 + compound_score) / 2 # مپ کردن compound به [0,1]
        n_score = (1 - compound_score) / 2 # (1-p_score)
        
        # اگر خیلی نزدیک به خنثی نباشد، یکی را غالب می‌کنیم
        if final_label == "positive":
             scores = {"positive": p_score / (p_score + n_score) if (p_score + n_score) > 0 else 0.5, 
                       "negative": n_score / (p_score + n_score) if (p_score + n_score) > 0 else 0.5,
                       "neutral": 0.0}
             # باز نرمال‌سازی برای اینکه positive غالب باشد
             if scores["positive"] > scores["negative"]:
                 scores = {"positive": 1.0, "negative": 0.0, "neutral": 0.0}
             else: # اگر به دلایلی negative بیشتر شد (نباید اتفاق بیفتد با منطق compound)
                 scores = {"positive": 0.0, "negative": 1.0, "neutral": 0.0}


    elif final_label == "negative":
        scores = {"positive": 0.0, "negative": 1.0, "neutral": 0.0}
    else: # neutral
        scores = {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

    # یک روش ساده‌تر برای تخصیص امتیاز نهایی وقتی برچسب مشخص شده:
    if final_label == "positive":
        final_scores: SentimentScore = {"positive": 1.0, "negative": 0.0, "neutral": 0.0}
    elif final_label == "negative":
        final_scores = {"positive": 0.0, "negative": 1.0, "neutral": 0.0}
    else: # neutral
        # برای حالت خنثی، می‌توانیم امتیازات مثبت و منفی را هم برگردانیم اگر نزدیک به هم بودند
        if total_sentiment_words > 0:
             pos_ratio = positive_score / total_sentiment_words
             neg_ratio = negative_score / total_sentiment_words
             neu_ratio = 1.0 - pos_ratio - neg_ratio # ممکن است منفی شود اگر توزیع دقیق نباشد
             # اطمینان از اینکه خنثی منفی نمی‌شود
             if neu_ratio < 0: neu_ratio = 0.0
             # نرمال سازی مجدد
             total_ratio = pos_ratio + neg_ratio + neu_ratio
             if total_ratio > 0:
                 final_scores = {
                     "positive": pos_ratio / total_ratio,
                     "negative": neg_ratio / total_ratio,
                     "neutral": neu_ratio / total_ratio
                 }
             else: # اگر به طریقی total_ratio صفر شد
                 final_scores = {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

        else: # هیچ کلمه احساسی نبود
            final_scores = {"positive": 0.0, "negative": 0.0, "neutral": 1.0}


    # اصلاح نهایی برای سادگی و تمرکز بر برچسب اصلی
    if final_label == "positive":
        final_scores_simplified: SentimentScore = {"positive": 1.0, "negative": 0.0, "neutral": 0.0}
    elif final_label == "negative":
        final_scores_simplified = {"positive": 0.0, "negative": 1.0, "neutral": 0.0}
    else: # neutral
        # در حالت خنثی، اگر کلمات مثبت و منفی وجود داشتند اما همدیگر را خنثی کردند،
        # می‌توانیم امتیازاتشان را نشان دهیم.
        if positive_score > 0 or negative_score > 0:
            p_s = positive_score / total_sentiment_words if total_sentiment_words else 0
            n_s = negative_score / total_sentiment_words if total_sentiment_words else 0
            # اطمینان از اینکه جمعشان ۱ شود
            sum_ps_ns = p_s + n_s
            if sum_ps_ns > 0 :
                final_scores_simplified = {
                    "positive": p_s / sum_ps_ns * (1- (1/(total_sentiment_words+1) if total_sentiment_words else 0.5)), # ضریب خنثی بودن
                    "negative": n_s / sum_ps_ns * (1- (1/(total_sentiment_words+1) if total_sentiment_words else 0.5)),
                    "neutral": (1/(total_sentiment_words+1) if total_sentiment_words else 0.5)
                }
                # نرمال‌سازی مجدد برای اطمینان از جمع ۱
                current_sum = sum(final_scores_simplified.values())
                if current_sum > 0:
                    final_scores_simplified = {k: v / current_sum for k, v in final_scores_simplified.items()}
                else: # اگر به دلیلی همه صفر شدند
                     final_scores_simplified = {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

            else: # هیچ کلمه احساسی نبود
                final_scores_simplified = {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
        else: # هیچ کلمه احساسی نبود
            final_scores_simplified = {"positive": 0.0, "negative": 0.0, "neutral": 1.0}


    return final_label, final_scores_simplified
