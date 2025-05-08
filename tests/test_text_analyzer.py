# tests/test_text_analyzer.py

import unittest
from farsinum.text_analyzer import count_words, count_sentences, count_paragraphs

class TestTextAnalyzer(unittest.TestCase):

    def test_count_words(self):
        self.assertEqual(count_words("سلام دنیا، این یک تست است."), 6)
        self.assertEqual(count_words("  سلام   دنیا  "), 2)
        self.assertEqual(count_words("یک\nکلمه\nدیگر"), 3)
        self.assertEqual(count_words("کلمه."), 1) # علائم نگارشی چسبیده به کلمه با split جدا نمی‌شوند
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words("   "), 0)

    def test_count_sentences(self):
        self.assertEqual(count_sentences("سلام. خوبی؟ تست!"), 3)
        self.assertEqual(count_sentences("این یک جمله است بدون نقطه پایانی"), 1)
        self.assertEqual(count_sentences("جمله اول. جمله دوم."), 2)
        self.assertEqual(count_sentences("سلام!!! خوبی؟؟؟"), 2) # چند علامت پشت سر هم
        self.assertEqual(count_sentences(""), 0)
        self.assertEqual(count_sentences("   "), 0)
        self.assertEqual(count_sentences("آقای دکتر. احمدی رفتند."), 2) # Ph.D. style can be tricky
        self.assertEqual(count_sentences("قیمت ۲.۵ دلار است."), 1) # اعداد اعشاری

    def test_count_paragraphs(self):
        self.assertEqual(count_paragraphs("پاراگراف اول.\n\nپاراگراف دوم."), 2)
        self.assertEqual(count_paragraphs("یک پاراگراف تنها."), 1)
        self.assertEqual(count_paragraphs("پاراگراف اول.\n \nپاراگراف دوم.\n\n\nپاراگراف سوم."), 3)
        self.assertEqual(count_paragraphs(""), 0)
        self.assertEqual(count_paragraphs("   \n   "), 0) # فقط فضای خالی
        self.assertEqual(count_paragraphs("خط اول\nخط دوم\nخط سوم"), 1) # بدون خط خالی بینشان

    def test_input_types(self):
        with self.assertRaises(TypeError):
            count_words(123) # type: ignore
        with self.assertRaises(TypeError):
            count_sentences(None) # type: ignore
        with self.assertRaises(TypeError):
            count_paragraphs([]) # type: ignore


if __name__ == '__main__':
    unittest.main()
