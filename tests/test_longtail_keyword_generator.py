# tests/test_longtail_keyword_generator.py

import unittest
from farsinum.longtail_keyword_generator import (
    generate_longtail_keywords,
    _normalize_keywords,
    QUESTION_PREFIXES, # برای دسترسی در تست
    COMMON_SUFFIXES
)

class TestLongtailKeywordGenerator(unittest.TestCase):

    def test_normalize_keywords(self):
        self.assertEqual(sorted(_normalize_keywords("کتاب پایتون")), sorted(["کتاب", "پایتون"]))
        self.assertEqual(sorted(_normalize_keywords("کتاب, پایتون ")), sorted(["کتاب", "پایتون"]))
        self.assertEqual(sorted(_normalize_keywords([" کتاب خوب  ", "آموزش پایتون"])),
                         sorted(["کتاب خوب", "اموزش پایتون"])) # نرمالایزر "آموزش" را به "اموزش" تبدیل می‌کند
        self.assertEqual(_normalize_keywords(["پایتون", "پایتون"]), ["پایتون"]) # حذف تکراری
        self.assertEqual(_normalize_keywords(""), [])
        with self.assertRaises(TypeError):
            _normalize_keywords(123) # type: ignore

    def test_generate_with_single_seed(self):
        seed = "طراحی سایت"
        suggestions = generate_longtail_keywords(seed, max_combinations=1, max_suggestions_per_seed=50)
        
        self.assertIn(seed, suggestions) # include_original=True
        self.assertTrue(any(s.startswith("چگونه") and seed in s for s in suggestions))
        self.assertTrue(any(s.endswith("آنلاین") and seed in s for s in suggestions))
        self.assertTrue(any("بهترین" in s and seed in s and "چیست" in s for s in suggestions)) # تست ترکیب سه‌تایی
        
        # بررسی min_length
        short_suggestions = generate_longtail_keywords("وب", min_length=3, question_prefixes=["در"], common_suffixes=["نو"])
        # "در وب نو" باید باشد، اما "در وب" نه
        self.assertIn("در وب نو", short_suggestions)
        self.assertNotIn("در وب", short_suggestions) # چون "در وب" دو کلمه است

    def test_generate_with_multiple_seeds_and_combinations(self):
        seeds = ["آموزش", "پایتون"] # نرمالایزر "آموزش" را ممکن است تغییر دهد
        normalized_seeds = _normalize_keywords(seeds) # ["اموزش", "پایتون"]

        # تست با max_combinations=1 (فقط روی هر کلمه جداگانه)
        suggestions_combo1 = generate_longtail_keywords(seeds, max_combinations=1)
        self.assertTrue(any("چگونه اموزش" in s for s in suggestions_combo1))
        self.assertTrue(any("چگونه پایتون" in s for s in suggestions_combo1))
        self.assertFalse(any("اموزش پایتون" in s and "چگونه" in s for s in suggestions_combo1)) # نباید ترکیب شوند

        # تست با max_combinations=2 (ترکیبات دوتایی هم مجاز)
        suggestions_combo2 = generate_longtail_keywords(seeds, max_combinations=2)
        # باید شامل پیشنهادات برای "اموزش پایتون" و "پایتون اموزش" باشد
        self.assertTrue(any("چگونه اموزش پایتون" in s for s in suggestions_combo2) or \
                        any("چگونه پایتون اموزش" in s for s in suggestions_combo2))
        self.assertTrue(any("اموزش پایتون چیست" in s for s in suggestions_combo2) or \
                        any("پایتون اموزش چیست" in s for s in suggestions_combo2))


    def test_max_suggestions_per_seed_limit(self):
        # استفاده از لیست‌های کوچک برای کنترل دقیق‌تر
        custom_prefixes = [f"پ{i}" for i in range(30)] # 30 پیشوند
        suggestions = generate_longtail_keywords(
            "تست",
            question_prefixes=custom_prefixes,
            common_suffixes=[], # بدون پسوند برای سادگی
            max_suggestions_per_seed=10,
            include_original=False, # فقط تولید شده‌ها
            max_combinations=1
        )
        # باید حداکثر 10 پیشنهاد وجود داشته باشد (چون فقط از پیشوندها تولید می‌شود)
        self.assertLessEqual(len(suggestions), 10)


    def test_empty_seed_keywords(self):
        self.assertEqual(generate_longtail_keywords(""), set())
        self.assertEqual(generate_longtail_keywords([]), set())

    def test_include_original_false(self):
        seed = "نمونه"
        suggestions = generate_longtail_keywords(seed, include_original=False)
        self.assertNotIn(seed, suggestions)
        self.assertTrue(len(suggestions) > 0)

    def test_min_length_filter(self):
        # "الف" یک کلمه است، "ب ج" دو کلمه
        suggestions = generate_longtail_keywords(
            "الف",
            question_prefixes=["پیش"], # "پیش الف" -> 2 کلمه
            common_suffixes=["پس"],   # "الف پس" -> 2 کلمه
            max_combinations=1,
            include_original=True
        )
        # با min_length=2 (پیش‌فرض)
        self.assertIn("پیش الف", suggestions)
        self.assertIn("الف پس", suggestions)
        self.assertNotIn("الف", suggestions) # چون "الف" یک کلمه است و min_length=2

        suggestions_min3 = generate_longtail_keywords(
            "الف",
            question_prefixes=["پیش یک"], # "پیش یک الف" -> 3 کلمه
            common_suffixes=["پس دو"],   # "الف پس دو" -> 3 کلمه
            max_combinations=1,
            min_length=3,
            include_original=True
        )
        self.assertIn("پیش یک الف", suggestions_min3)
        self.assertIn("الف پس دو", suggestions_min3)
        self.assertNotIn("الف", suggestions_min3)


if __name__ == '__main__':
    unittest.main()
