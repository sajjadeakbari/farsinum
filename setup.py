# setup.py

from pathlib import Path
import setuptools


def get_version(package_name: str) -> str:
    """
    استخراج نسخه از فایل __init__.py داخل پکیج
    """
    version_file = Path(package_name) / "__init__.py"
    with version_file.open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "0.0.0"  # مقدار پیش‌فرض در صورت عدم یافتن نسخه


# خواندن توضیحات کامل از README.md
long_description = Path("README.md").read_text(encoding="utf-8")

# تعیین نسخه پکیج
VERSION = get_version("farsinum")

setuptools.setup(
    name="farsinum",
    version=VERSION,
    author="Sajjad Akbari",
    author_email="sajjad.akbari.dev@gmail.com",
    description="کتابخانه پایتون برای تبدیل اعداد، نرمال‌سازی متن، تحلیل متن، تبدیل تاریخ و تحلیل احساسات ساده فارسی.", # توضیحات به‌روز شد
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sajjadeakbari/farsinum",
    project_urls={
        "Bug Tracker": "https://github.com/sajjadeakbari/farsinum/issues",
        "Homepage": "https://sajjadakbari.ir",
    },
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    package_data={ # اضافه کردن این بخش برای شامل کردن فایل‌های داده
        'farsinum': ['data/positive_words_fa.txt', 'data/negative_words_fa.txt'],
    },
    # include_package_data=True, # راه دیگر، اگر از MANIFEST.in استفاده می‌کنید (اینجا package_data صریح‌تر است)
    install_requires=[
        "jdatetime>=2.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic", # برای تحلیل احساسات هم مناسب است
        "Topic :: Utilities",
        "Natural Language :: Persian",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    keywords="farsi, persian, numbers, numerals, text, normalize, nlp, analysis, date, jalali, shamsi, sentiment, احساسات, convert, words, اعداد, فارسی, تبدیل, حروف, متن, نرمال‌سازی, تحلیل, تاریخ, شمسی, جلالی", # کلمات کلیدی به‌روز شد
)
