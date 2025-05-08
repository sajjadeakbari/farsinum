# tests/test_numeral_converter.py

import unittest
from farsinum import to_persian_numerals, to_english_numerals

class TestNumeralConverter(unittest.TestCase):

    def test_to_persian_numerals(self):
        self.assertEqual(to_persian_numerals("123"), "۱۲۳")
        self.assertEqual(to_persian_numerals("0987654321"), "۰۹۸۷۶۵۴۳۲۱")
        self.assertEqual(to_persian_numerals("test 456 with 789"), "test ۴۵۶ with ۷۸۹")
        self.assertEqual(to_persian_numerals("No digits here"), "No digits here")
        self.assertEqual(to_persian_numerals(""), "")
        self.assertEqual(to_persian_numerals(123), "۱۲۳")
        self.assertEqual(to_persian_numerals("۱۲۳"), "۱۲۳") # Already Persian

    def test_to_english_numerals(self):
        self.assertEqual(to_english_numerals("۱۲۳"), "123")
        self.assertEqual(to_english_numerals("۰۹۸۷۶۵۴۳۲۱"), "0987654321")
        self.assertEqual(to_english_numerals("تست ۴۵۶ با ۷۸۹"), "تست 456 با 789")
        self.assertEqual(to_english_numerals("اینجا عددی نیست"), "اینجا عددی نیست")
        self.assertEqual(to_english_numerals(""), "")
        # self.assertEqual(to_english_numerals(۱۲۳), "123") # Python int cannot be Persian numeral
        self.assertEqual(to_english_numerals("123"), "123") # Already English

if __name__ == '__main__':
    unittest.main()
