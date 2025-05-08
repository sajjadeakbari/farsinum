# setup.py
import setuptools
import os

# برای خواندن نسخه از __init__.py بدون وارد کردن کل پکیج
def get_version(package_name):
    version_path = os.path.join(package_name, "__init__.py")
    with open(version_path, "r", encoding="utf-8") as fp:
        for line in fp:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "0.0.0" # مقدار پیشفرض اگر پیدا نشد

# خواندن محتوای README.md برای long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = get_version("farsinum") # نام پوشه اصلی پکیج شما

setuptools.setup(
    name="farsinum", # نام پکیج شما در PyPI
    version=VERSION,
    author="Sajjad Akbari", # نام شما
    author_email="sajjad.akbari.dev@gmail.com", # ایمیل شما
    description="کتابخانه پایتون برای تبدیل اعداد فارسی به انگلیسی و برعکس، و تبدیل عدد به حروف فارسی.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sajjadeakbari/farsinum", # آدرس مخزن گیت‌هاب پروژه
    project_urls={ # لینک‌های اضافی (اختیاری)
        "Bug Tracker": "https://github.com/sajjadeakbari/farsinum/issues",
        "Homepage": "https://sajjadakbari.ir", # اگر وبسایت شخصی یا پروژه دارید
    },
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]), # پیدا کردن خودکار پکیج‌ها
    # اگر پکیج شما به کتابخانه‌های دیگری نیاز دارد، اینجا لیست کنید:
    # install_requires=[
    #     "requests>=2.20.0",
    # ],
    classifiers=[
        # وضعیت توسعه:
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta", # یا 3 - Alpha برای شروع

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic", # مرتبط با پردازش زبان
        "Natural Language :: Persian", # مشخص کردن زبان فارسی

        "License :: OSI Approved :: MIT License", # مجوز شما

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12", # نسخه‌های پایتون پشتیبانی شده
        "Operating System :: OS Independent", # مستقل از سیستم عامل
    ],
    python_requires='>=3.7', # حداقل نسخه پایتون مورد نیاز
    keywords="farsi, persian, numbers, numerals, convert, words, اعداد, فارسی, تبدیل, حروف", # کلمات کلیدی برای جستجو
)
