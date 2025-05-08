# tests/test_date_converter.py

import unittest
import datetime
import jdatetime
from farsinum.date_converter import (
    gregorian_to_jalali,
    jalali_to_gregorian,
    today_jalali,
    DEFAULT_JALALI_FORMAT,
    COMMON_JALALI_FORMAT_WITH_DAY_NAME
)
from farsinum.numeral_converter import to_english_numerals # برای تست راحت‌تر

class TestDateConverter(unittest.TestCase):

    def test_gregorian_to_jalali_string_input(self):
        self.assertEqual(gregorian_to_jalali("2023-03-21"), "۱۴۰۲/۰۱/۰۱")
        self.assertEqual(gregorian_to_jalali("2023/10/08"), "۱۴۰۲/۰۷/۱۶")
        self.assertEqual(gregorian_to_jalali("2024-02-29", use_persian_numerals=False), "1402/12/10") # سال کبیسه
        
        # تست فرمت با نام ماه و روز
        # خروجی دقیق نام روز و ماه بستگی به لوکیل سیستم و پیاده‌سازی jdatetime دارد
        # اینجا یک مثال برای مقایسه دستی است
        # print(gregorian_to_jalali("2023-10-08", output_format=COMMON_JALALI_FORMAT_WITH_DAY_NAME))
        # باید چیزی شبیه "یکشنبه ۱۶ مهر ۱۴۰۲" باشد

        # تست خروجی تاپل
        self.assertEqual(gregorian_to_jalali("2023-03-21", output_format=None), (1402, 1, 1))

    def test_gregorian_to_jalali_date_input(self):
        dt = datetime.date(2023, 10, 8)
        self.assertEqual(gregorian_to_jalali(dt), "۱۴۰۲/۰۷/۱۶")
        dt_time = datetime.datetime(2023, 3, 21, 10, 30)
        self.assertEqual(gregorian_to_jalali(dt_time), "۱۴۰۲/۰۱/۰۱")

    def test_gregorian_to_jalali_invalid_input(self):
        with self.assertRaises(ValueError):
            gregorian_to_jalali("2023-13-01") # ماه نامعتبر
        with self.assertRaises(ValueError):
            gregorian_to_jalali("invalid-date")
        with self.assertRaises(TypeError):
            gregorian_to_jalali(12345) # type: ignore

    def test_jalali_to_gregorian_string_input(self):
        self.assertEqual(jalali_to_gregorian("۱۴۰۲/۰۱/۰۱"), "2023-03-21")
        self.assertEqual(jalali_to_gregorian("1402/07/16"), "2023-10-08")
        self.assertEqual(jalali_to_gregorian("1402-12-10"), "2024-02-29") # سال کبیسه شمسی
        
        # تست خروجی شیء date
        self.assertEqual(jalali_to_gregorian("۱۴۰۲/۰۱/۰۱", output_format=None), datetime.date(2023, 3, 21))

    def test_jalali_to_gregorian_tuple_input(self):
        self.assertEqual(jalali_to_gregorian((1402, 7, 16)), "2023-10-08")

    def test_jalali_to_gregorian_jdate_input(self):
        jd = jdatetime.date(1402, 1, 1)
        self.assertEqual(jalali_to_gregorian(jd), "2023-03-21")
        jdt = jdatetime.datetime(1402, 7, 16, 10, 0)
        self.assertEqual(jalali_to_gregorian(jdt), "2023-10-08")

    def test_jalali_to_gregorian_invalid_input(self):
        with self.assertRaises(ValueError): # از تابع _parse_jalali_date_str
            jalali_to_gregorian("۱۴۰۲/۱۳/۰۱") # ماه نامعتبر شمسی
        with self.assertRaises(ValueError): # از jdatetime.date
            jalali_to_gregorian((1402, 2, 32)) # روز نامعتبر شمسی
        with self.assertRaises(ValueError):
            jalali_to_gregorian("invalid-date-شمسی")
        with self.assertRaises(TypeError):
            jalali_to_gregorian(12345) # type: ignore
        with self.assertRaises(ValueError): # فرمت پشتیبانی نشده توسط _parse_jalali_date_str
            jalali_to_gregorian("اول فروردین ۱۴۰۲")


    def test_today_jalali(self):
        # این تست حساس به زمان است و ممکن است در روزهای مختلف نتایج متفاوتی بدهد.
        # بهتر است خروجی را چک کنیم که آیا یک رشته با فرمت صحیح است یا نه.
        today_str = today_jalali()
        self.assertIsInstance(today_str, str)
        # تبدیل به اعداد انگلیسی برای بررسی فرمت YYYY/MM/DD
        today_en_num = to_english_numerals(today_str)
        try:
            datetime.datetime.strptime(today_en_num, "%Y/%m/%d") # بررسی فرمت پیش‌فرض
        except ValueError:
            self.fail(f"فرمت today_jalali نامعتبر است: {today_str}")

        today_formatted = today_jalali(output_format=COMMON_JALALI_FORMAT_WITH_DAY_NAME)
        self.assertIsInstance(today_formatted, str)
        # بررسی اینکه آیا شامل نام روز و ماه است (به طور ساده)
        self.assertTrue(any(day_name in today_formatted for day_name in ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]))
        self.assertTrue(any(month_name in today_formatted for month_name in jdatetime.date.j_months_fa))
        # print(f"\nامروز به شمسی: {today_formatted}")

if __name__ == '__main__':
    unittest.main()
