# tests/test_seo_analyzer.py

import unittest
from farsinum.seo_analyzer import (
    check_text_length,
    check_keyword_density,
    check_headings_simple,
    check_readability_simple,
    run_seo_checklist_on_text,
    SEOResult,
    RECOMMENDED_MIN_WORD_COUNT,
    RECOMMENDED_KEYWORD_DENSITY_MIN,
    RECOMMENDED_KEYWORD_DENSITY_MAX
)

class TestSEOAnalyzer(unittest.TestCase):

    def test_seoresult_class(self):
        res = SEOResult("Test Check", True, "Passed successfully", value=10)
        self.assertEqual(res.check_name, "Test Check")
        self.assertTrue(res.passed)
        self.assertEqual(res.message, "Passed successfully")
        self.assertEqual(res.value, 10)
        self.assertIn("'Test Check'", repr(res))
        self.assertEqual(res.to_dict()['check_name'], "Test Check")


    def test_check_text_length(self):
        short_text = "این متن کوتاه است." # 4 کلمه
        long_text = " ".join(["کلمه"] * (RECOMMENDED_MIN_WORD_COUNT + 50))

        res_short = check_text_length(short_text)
        self.assertFalse(res_short.passed)
        self.assertIn(f"حداقل {RECOMMENDED_MIN_WORD_COUNT} کلمه", res_short.message)
        self.assertEqual(res_short.value, 4)

        res_long = check_text_length(long_text)
        self.assertTrue(res_long.passed)
        self.assertIn("مناسب به نظر می‌رسد", res_long.message)
        self.assertEqual(res_long.value, RECOMMENDED_MIN_WORD_COUNT + 50)

    def test_check_keyword_density(self):
        text = "کلمه کلیدی ما سئو است. سئو یک بحث مهم در وب است. سئو کمک می‌کند."
        # "سئو" 3 بار تکرار شده، کل کلمات: 14 (تقریبی، بستگی به شمارشگر دارد)
        # اگر count_words دقیقتر باشد، مثلا "سئو" 3 بار و کل کلمات 13
        # چگالی: 3/13 = 0.23 (23%)

        res_good_density = check_keyword_density(text, "سئو", min_density=0.1, max_density=0.3)
        self.assertTrue(res_good_density.passed)
        self.assertAlmostEqual(res_good_density.value, 3/13, delta=0.01) # با توجه به خروجی واقعی تنظیم شود
        
        res_low_density = check_keyword_density(text, "محتوا", min_density=0.1, max_density=0.3) # "محتوا" 0 بار
        self.assertFalse(res_low_density.passed)
        self.assertEqual(res_low_density.value, 0)
        self.assertIn("کمتر از حد توصیه شده", res_low_density.message)

        text_stuffed = "سئو سئو سئو سئو سئو سئو خوب است." # 6 سئو، کل کلمات 7. چگالی: 6/7 = 85%
        res_high_density = check_keyword_density(text_stuffed, "سئو", min_density=0.01, max_density=0.05)
        self.assertFalse(res_high_density.passed)
        self.assertIn("بیشتر از حد توصیه شده", res_high_density.message)
        self.assertAlmostEqual(res_high_density.value, 6/7, delta=0.01)

        res_no_keyword = check_keyword_density(text, "")
        self.assertFalse(res_no_keyword.passed)
        self.assertIn("ارائه نشده", res_no_keyword.message)

        res_empty_text = check_keyword_density("", "سئو")
        self.assertFalse(res_empty_text.passed)
        self.assertIn("متن خالی است", res_empty_text.message)


    def test_check_headings_simple(self):
        text_with_headings = """
# عنوان اصلی سایت
این یک پاراگراف است.
## یک زیر عنوان مهم
محتوای بیشتر در اینجا.
### عنوان کوچکتر
نکات جزئی.
خط کوتاه تنها
"""
        res = check_headings_simple(text_with_headings)
        self.assertTrue(res.passed) # چون H1 دارد و عناوین دیگر
        self.assertGreater(res.value, 2)
        self.assertEqual(res.details.get("H1 (Markdown)"), 1)
        self.assertEqual(res.details.get("H2 (Markdown)"), 1)
        self.assertEqual(res.details.get("H3+ (Markdown)"), 1)
        self.assertEqual(res.details.get("Short Line Heading"), 1)


        text_no_headings = "این یک متن ساده بدون هیچ عنوانی است. فقط پاراگراف‌های معمولی."
        res_no = check_headings_simple(text_no_headings)
        self.assertFalse(res_no.passed)
        self.assertEqual(res_no.value, 0)
        self.assertIn("هیچ عنوانی", res_no.message)

        text_only_h2 = "## فقط یک زیر عنوان\nبدون عنوان اصلی."
        res_h2 = check_headings_simple(text_only_h2)
        self.assertFalse(res_h2.passed) # چون H1 ندارد
        self.assertIn("عنوان اصلی (H1 با #) وجود ندارد", res_h2.message)


    def test_check_readability_simple(self):
        # متن با جملات کوتاه: 2 جمله، 8 کلمه. میانگین: 4
        text_readable = "سلام. این یک تست است. همه چیز خوب است." # 3 جمله، 8 کلمه. میانگین 8/3 = 2.66
        res_readable = check_readability_simple(text_readable, max_avg_sentence_len=5)
        self.assertTrue(res_readable.passed)
        self.assertLessEqual(res_readable.value, 5)

        # متن با جملات طولانی: 1 جمله، 15 کلمه. میانگین: 15
        text_long_sentences = "این یک جمله بسیار بسیار طولانی است که برای تست خوانایی نوشته شده و کلمات زیادی دارد تا میانگین طول جمله بالا برود."
        # farsinum.count_sentences برای این متن 1 برمی‌گرداند (اگر نقطه در آخر نباشد)
        # farsinum.count_words حدود 20 کلمه
        # میانگین 20/1 = 20
        res_long = check_readability_simple(text_long_sentences, max_avg_sentence_len=10)
        self.assertFalse(res_long.passed)
        self.assertGreater(res_long.value, 10)

        res_no_sentence = check_readability_simple("فقطکلماتبدوننقطه")
        self.assertFalse(res_no_sentence.passed) # چون count_sentences ممکن است 1 برگرداند اگر متنی باشد
                                               # یا اگر متن خالی شود 0 برگرداند
                                               # منطق باید بررسی شود.
        # اگر count_sentences برای "abc" یک برگرداند و count_words هم یک، میانگین 1 می‌شود.
        # اگر count_sentences برای متن بدون نقطه، 0 برگرداند، آنگاه اینجا باید False شود.
        # با پیاده‌سازی فعلی، اگر متنی باشد و نقطه نداشته باشد count_sentences = 1
        # پس باید value چیزی باشد.
        # اگر متن کاملا خالی باشد، آنگاه value = 0 و passed = False

        res_empty_text = check_readability_simple("")
        self.assertFalse(res_empty_text.passed)
        self.assertEqual(res_empty_text.value, 0)


    def test_run_seo_checklist_on_text(self):
        sample_text = """
# بهینه سازی موتور جستجو (سئو)
سئو یک فرآیند مهم برای دیده شدن در نتایج جستجو است.
این متن درباره سئو و اهمیت آن صحبت می‌کند. ما باید به سئو توجه کنیم.
## چرا سئو مهم است؟
چون به کسب و کارها کمک می‌کند. سئو بازدید سایت را افزایش می‌دهد.
"""
        # این متن حدود 30 کلمه دارد.
        # "سئو" 5 بار تکرار شده.
        # 1 H1, 1 H2.
        # حدود 4 جمله. میانگین طول جمله: 30/4 = 7.5

        results = run_seo_checklist_on_text(sample_text, keyword="سئو")
        self.assertEqual(len(results), 4) # Text Length, Keyword Density, Headings, Readability

        length_res = next(r for r in results if r.check_name == "Text Length")
        self.assertFalse(length_res.passed) # چون کمتر از RECOMMENDED_MIN_WORD_COUNT است

        density_res = next(r for r in results if r.check_name == "Keyword Density")
        # 5 / (حدود 30) = 16% . اگر min=1% و max=3% باشد، این باید False باشد (خیلی زیاد)
        # باید مقادیر پیش‌فرض را در نظر بگیریم
        # RECOMMENDED_KEYWORD_DENSITY_MIN = 0.01
        # RECOMMENDED_KEYWORD_DENSITY_MAX = 0.03
        # پس 16% خارج از محدوده و False است.
        self.assertFalse(density_res.passed)
        self.assertIn("بیشتر از حد توصیه شده", density_res.message)


        headings_res = next(r for r in results if r.check_name == "Headings Usage")
        self.assertTrue(headings_res.passed)

        readability_res = next(r for r in results if r.check_name == "Readability (Avg Sentence Length)")
        self.assertTrue(readability_res.passed) # 7.5 < 25


        results_no_keyword = run_seo_checklist_on_text(sample_text)
        density_res_no_kw = next(r for r in results_no_keyword if r.check_name == "Keyword Density")
        self.assertFalse(density_res_no_kw.passed)
        self.assertIn("ارائه نشده", density_res_no_kw.message)


if __name__ == '__main__':
    unittest.main()
