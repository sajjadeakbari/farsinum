# tests/test_number_to_words.py

import unittest
from farsinum import number_to_persian_words

class TestNumberToWords(unittest.TestCase):

    def test_simple_numbers(self):
        self.assertEqual(number_to_persian_words(0), "صفر")
        self.assertEqual(number_to_persian_words(1), "یک")
        self.assertEqual(number_to_persian_words(10), "ده")
        self.assertEqual(number_to_persian_words(15), "پانزده")
        self.assertEqual(number_to_persian_words(20), "بیست")
        self.assertEqual(number_to_persian_words(21), "بیست و یک")
        self.assertEqual(number_to_persian_words(99), "نود و نه")

    def test_hundreds(self):
        self.assertEqual(number_to_persian_words(100), "یکصد")
        self.assertEqual(number_to_persian_words(101), "یکصد و یک")
        self.assertEqual(number_to_persian_words(128), "یکصد و بیست و هشت")
        self.assertEqual(number_to_persian_words(550), "پانصد و پنجاه")
        self.assertEqual(number_to_persian_words(999), "نهصد و نود و نه")

    def test_thousands(self):
        self.assertEqual(number_to_persian_words(1000), "یک هزار")
        self.assertEqual(number_to_persian_words(1001), "یک هزار و یک")
        self.assertEqual(number_to_persian_words(2500), "دو هزار و پانصد")
        self.assertEqual(number_to_persian_words(12345), "دوازده هزار و سیصد و چهل و پنج")
        self.assertEqual(number_to_persian_words(999999), "نهصد و نود و نه هزار و نهصد و نود و نه")

    def test_millions(self):
        self.assertEqual(number_to_persian_words(1000000), "یک میلیون")
        self.assertEqual(number_to_persian_words(2500000), "دو میلیون و پانصد هزار")
        self.assertEqual(number_to_persian_words(123456789), "یکصد و بیست و سه میلیون و چهارصد و پنجاه و شش هزار و هفتصد و هشتاد و نه")

    def test_negative_numbers(self):
        self.assertEqual(number_to_persian_words(-1), "منفی یک")
        self.assertEqual(number_to_persian_words(-128), "منفی یکصد و بیست و هشت")
        self.assertEqual(number_to_persian_words(-1000000), "منفی یک میلیون")

    def test_edge_cases_and_errors(self):
        with self.assertRaises(TypeError):
            number_to_persian_words("123") # type: ignore
        
        # تست عدد بسیار بزرگ (بسته به مقیاس‌های تعریف شده)
        # اگر کوادریلیون آخرین مقیاس باشد، 1000^6 قابل قبول است اما 1000^7 نه.
        # 10^18 (یک کوادریلیون)
        number_to_persian_words(10**18) # باید کار کند
        with self.assertRaises(ValueError): # فراتر از کوادریلیون
             number_to_persian_words(10**21)


if __name__ == '__main__':
    unittest.main()
