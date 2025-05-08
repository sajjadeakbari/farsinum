# farsinum/cli.py

import argparse
import os
import sys
from farsinum.github_rtl_formatter import format_markdown_for_rtl
from farsinum import __version__ as farsinum_version # برای نمایش نسخه

def main():
    parser = argparse.ArgumentParser(
        description=f"Farsinum CLI v{farsinum_version} - ابزاری برای قالب‌بندی فایل‌های README.md فارسی.",
        formatter_class=argparse.RawTextHelpFormatter # برای نمایش بهتر help
    )
    
    subparsers = parser.add_subparsers(dest="command", title="دستورات موجود", help="راهنمای دستورات")
    subparsers.required = True # یک دستور باید انتخاب شود

    # --- دستور format-readme ---
    readme_parser = subparsers.add_parser(
        "format-readme",
        help="فایل مارک‌داون (مانند README.md) را برای نمایش بهتر فارسی (راست‌به‌چپ) قالب‌بندی می‌کند.",
        description=(
            "این دستور محتوای یک فایل مارک‌داون را می‌خواند و با افزودن کاراکترهای کنترل جهت یونیکد (RLM)\n"
            "در نقاط مناسب، سعی در بهبود نمایش متن‌های ترکیبی فارسی و انگلیسی دارد.\n"
            "توجه: این یک راه‌حل کامل نیست و ممکن است نیاز به تنظیمات دستی وجود داشته باشد."
        )
    )
    readme_parser.add_argument(
        "input_file",
        type=str,
        help="مسیر فایل مارک‌داون ورودی (مثلاً README.md)."
    )
    readme_parser.add_argument(
        "-o", "--output-file",
        type=str,
        default=None,
        help="مسیر فایل خروجی. اگر مشخص نشود، فایل ورودی بازنویسی می‌شود (با احتیاط استفاده شود!)."
    )
    readme_parser.add_argument(
        "--no-rlm",
        action="store_false", # مقدار پیش‌فرض True برای add_rlm_to_rtl_lines
        dest="add_rlm",
        help="از افزودن خودکار کاراکتر RLM به خطوط فارسی جلوگیری می‌کند."
    )
    readme_parser.add_argument(
        "--stdout",
        action="store_true",
        help="خروجی را به جای فایل، در خروجی استاندارد (stdout) چاپ می‌کند."
    )
    readme_parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s (farsinum {farsinum_version})",
        help="نمایش نسخه برنامه و خروج."
    )


    # اینجا می‌توانید دستورات دیگری برای CLI اضافه کنید (مثلاً تبدیل عدد به حروف از طریق CLI)
    # num_to_words_parser = subparsers.add_parser("num2words", help="تبدیل عدد به حروف فارسی")
    # num_to_words_parser.add_argument("number", type=int, help="عددی که می‌خواهید به حروف تبدیل شود")


    args = parser.parse_args()

    if args.command == "format-readme":
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"خطا: فایل ورودی '{args.input_file}' یافت نشد.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"خطا در خواندن فایل ورودی: {e}", file=sys.stderr)
            sys.exit(1)

        formatted_content = format_markdown_for_rtl(content, add_rlm_to_rtl_lines=args.add_rlm)

        if args.stdout:
            print(formatted_content)
        else:
            output_path = args.output_file if args.output_file else args.input_file
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                if output_path == args.input_file:
                    print(f"فایل '{args.input_file}' با موفقیت قالب‌بندی و بازنویسی شد.")
                else:
                    print(f"فایل قالب‌بندی شده با موفقیت در '{output_path}' ذخیره شد.")
            except Exception as e:
                print(f"خطا در نوشتن فایل خروجی: {e}", file=sys.stderr)
                sys.exit(1)
    
    # elif args.command == "num2words":
    #     from farsinum.number_to_words import number_to_persian_words
    #     print(number_to_persian_words(args.number))


if __name__ == '__main__': # برای تست مستقیم cli.py
    main()
