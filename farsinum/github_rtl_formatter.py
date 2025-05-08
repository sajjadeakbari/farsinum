# farsinum/github_rtl_formatter.py

import re

RLM = '\u200f'  # RIGHT-TO-LEFT MARK
LRM = '\u200e'  # LEFT-TO-RIGHT MARK

# الگو برای تشخیص بلوک‌های کد چند خطی (``` یا ~~~)
# این الگو باید گروه‌های غیرضبط‌کننده (non-capturing) برای خود فنس‌ها داشته باشد
# و گروه ضبط‌کننده برای محتوای داخل آن.
# (?s) برای DOTALL flag (نقطه همه چیز را شامل شود، حتی خط جدید)
CODE_BLOCK_PATTERN = re.compile(r"(?P<fence>```|~~~)(?P<lang>[\w+-]*)\n(?P<code>.*?)\n(?P=fence)", re.DOTALL | re.MULTILINE)

# الگو برای تشخیص کد اینلاین (`)
INLINE_CODE_PATTERN = re.compile(r"`([^`]+?)`")

# الگو برای تشخیص لینک‌های مارک‌داون [text](url "title")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+?)\]\(([^)]+?)\)")

# الگو برای تشخیص کلمات/عبارات انگلیسی (ساده شده)
# این الگو می‌تواند بسیار پیچیده‌تر باشد. فعلا کلماتی که فقط حروف لاتین و اعداد دارند.
ENGLISH_WORD_PATTERN = re.compile(r"\b[a-zA-Z0-9_.-]+\b(?![\]\)])") # منفی برای اینکه بخشی از لینک نباشد

def _is_predominantly_rtl(text: str) -> bool:
    """
    بررسی می‌کند آیا متن عمدتاً شامل کاراکترهای راست‌به‌چپ است یا خیر.
    این یک روش ساده است و می‌تواند بهبود یابد.
    """
    if not text.strip():
        return False # متن خالی جهت خاصی ندارد

    rtl_chars = 0
    ltr_chars = 0
    # محدوده‌ای از کاراکترهای رایج فارسی و عربی
    # این لیست می‌تواند کامل‌تر باشد.
    for char_code in map(ord, text):
        if 0x0600 <= char_code <= 0x06FF or \
           0x0750 <= char_code <= 0x077F or \
           0x08A0 <= char_code <= 0x08FF or \
           0xFB50 <= char_code <= 0xFDFF or \
           0xFE70 <= char_code <= 0xFEFF:
            rtl_chars += 1
        elif 'a' <= chr(char_code).lower() <= 'z':
            ltr_chars += 1
    
    return rtl_chars > ltr_chars

def _ensure_rlm_at_boundaries(line: str) -> str:
    """
    اطمینان از وجود RLM در ابتدا و انتهای خط فارسی اگر با کاراکتر LTR شروع/پایان یابد.
    این تابع باید هوشمندتر عمل کند و فقط روی خطوطی که واقعا فارسی هستند اعمال شود.
    """
    stripped_line = line.strip()
    if not stripped_line or not _is_predominantly_rtl(stripped_line):
        return line

    # اگر خط با یک کاراکتر چپ‌به‌راست (لاتین، عدد، برخی علائم) شروع شود و فارسی باشد
    # این شرط نیاز به دقت بیشتری دارد. فعلا اگر اولین کاراکتر غیرفاصله، لاتین یا عدد باشد.
    first_char = stripped_line[0]
    last_char = stripped_line[-1]
    
    # اگر خط با کاراکتر LTR شروع شود و RLM نداشته باشد
    if re.match(r"^[a-zA-Z0-9\[\(`]", stripped_line) and not line.startswith(RLM):
        line = RLM + line
        
    # اگر خط با کاراکتر LTR تمام شود و RLM نداشته باشد
    if re.search(r"[a-zA-Z0-9\]\)`]$", stripped_line) and not line.endswith(RLM):
        line = line + RLM
        
    return line

def _process_paragraph(paragraph: str) -> str:
    """پردازش یک پاراگراف برای بهبود جهت‌دهی."""
    # این تابع باید بسیار هوشمندتر باشد.
    # فعلا یک پردازش ساده روی کل پاراگراف انجام می‌دهیم.
    if not _is_predominantly_rtl(paragraph):
        return paragraph # اگر پاراگراف عمدتا LTR است (مثلا یک بلوک کد که جدا نشده)

    # یک ایده: کلمات/عبارات انگلیسی را با LRM محصور کنیم
    # def replace_english(match):
    #     return f"{LRM}{match.group(0)}{LRM}"
    # paragraph = ENGLISH_WORD_PATTERN.sub(replace_english, paragraph)
    # این کار ممکن است بیش از حد باشد و خوانایی را کم کند.

    # افزودن RLM به ابتدا و انتهای پاراگراف اگر لازم باشد
    # این باید در سطح خطوط انجام شود.
    lines = paragraph.splitlines()
    processed_lines = [_ensure_rlm_at_boundaries(line) for line in lines]
    return "\n".join(processed_lines)


def format_markdown_for_rtl(markdown_content: str) -> str:
    """
    قالب‌بندی محتوای مارک‌داون فارسی برای نمایش بهتر جهت‌گیری راست‌به‌چپ.
    این یک تابع ساده‌سازی شده است.
    """
    
    # 1. جداسازی بلوک‌های کد
    # ما باید متن را به بخش‌های کد و غیرکد تقسیم کنیم.
    # این کار با regex پیچیده است. یک روش ساده‌تر، جایگزینی موقت است.
    
    code_blocks = []
    def

  
RLM = '\u200f'  # RIGHT-TO-LEFT MARK
LRM = '\u200e'  # LEFT-TO-RIGHT MARK

# الگوی شروع و پایان بلوک کد
CODE_FENCE_PATTERN = re.compile(r"^(```|~~~)")

# الگوی تشخیص کلمات انگلیسی که ممکن است نیاز به LRM داشته باشند
# این الگو فقط کلماتی که کاملا انگلیسی هستند و با فاصله یا شروع/پایان خط احاطه شده‌اند را می‌گیرد
# و همچنین بخشی از لینک یا کد اینلاین نیستند.
# (این الگو بسیار ساده است و false positive/negative زیادی خواهد داشت)
# ENGLISH_IN_PERSIAN_PATTERN = re.compile(r"(?<!`)(?<!\]\()(\s|^)([a-zA-Z0-9_.-]+)((?=\s)|$)(?![^[]*?\]\()(?![^`]*?`)")
# الگوی ساده‌تر برای کلمات انگلیسی
ENGLISH_SEGMENT_PATTERN = re.compile(r"([a-zA-Z0-9][a-zA-Z0-9\s`'\"().,?!:;-]*[a-zA-Z0-9]|[a-zA-Z0-9]+)")


def _is_predominantly_rtl(text: str) -> bool:
    # ... (همانند قبل) ...
    if not text.strip(): return False
    rtl_chars, ltr_chars = 0, 0
    for char_code in map(ord, text):
        if 0x0600 <= char_code <= 0x06FF or \
           0x0750 <= char_code <= 0x077F or \
           0x08A0 <= char_code <= 0x08FF or \
           0xFB50 <= char_code <= 0xFDFF or \
           0xFE70 <= char_code <= 0xFEFF:
            rtl_chars += 1
        elif 'a' <= chr(char_code).lower() <= 'z':
            ltr_chars += 1
    return rtl_chars > ltr_chars if (rtl_chars + ltr_chars) > 0 else False # اگر کاراکتر فارسی بیشتر بود، RTL


def format_markdown_for_rtl(markdown_content: str, add_rlm_to_rtl_lines: bool = True) -> str:
    """
    قالب‌بندی محتوای مارک‌داون فارسی برای نمایش بهتر جهت‌گیری راست‌به‌چپ.
    - کاراکتر RLM را به ابتدا و انتهای خطوطی که عمدتا فارسی هستند و با کاراکتر LTR شروع یا پایان می‌یابند، اضافه می‌کند.
    - سعی می‌کند جهت بلوک‌های کد را حفظ کند.
    - این یک رویکرد "بهترین تلاش" است و ممکن است برای همه موارد کار نکند.
    """
    lines = markdown_content.splitlines()
    processed_lines = []
    in_code_block = False

    for line in lines:
        # بررسی برای شروع یا پایان بلوک کد
        if CODE_FENCE_PATTERN.match(line):
            in_code_block = not in_code_block
            processed_lines.append(line) # خود خط حصار کد دست نخورده باقی می‌ماند
            continue

        if in_code_block:
            # داخل بلوک کد، هیچ تغییری اعمال نمی‌کنیم
            processed_lines.append(line)
        else:
            # خارج از بلوک کد
            stripped_line = line.strip()
            if not stripped_line: # خط خالی
                processed_lines.append(line)
                continue

            # اگر خط عمدتا فارسی است
            if _is_predominantly_rtl(stripped_line):
                processed_line = line
                if add_rlm_to_rtl_lines:
                    # افزودن RLM اگر با کاراکتر LTR شروع می‌شود
                    # (مثلا یک لینک یا کلمه انگلیسی در ابتدای خط فارسی)
                    # این شرط می‌تواند دقیق‌تر شود تا فقط به کاراکترهای واقعا LTR واکنش نشان دهد
                    first_visible_char = stripped_line[0]
                    if re.match(r"[a-zA-Z0-9(\[`]", first_visible_char) and not line.lstrip().startswith(RLM):
                        # پیدا کردن اولین کاراکتر غیرفاصله و اضافه کردن RLM قبل از آن
                        match = re.search(r"\S", line)
                        if match:
                            idx = match.start()
                            processed_line = line[:idx] + RLM + line[idx:]
                        else: # اگر خط فقط فاصله بود (که با strip باید حذف می‌شد)
                            processed_line = RLM + line


                    # افزودن RLM اگر با کاراکتر LTR تمام می‌شود
                    last_visible_char = stripped_line[-1]
                    # (دقت کنید که line ممکن است فضاهای انتهایی داشته باشد)
                    current_line_to_check_end = processed_line # از خطی که شاید RLM اول را گرفته
                    if re.search(r"[a-zA-Z0-9)\]`]$", current_line_to_check_end.rstrip()) and not current_line_to_check_end.rstrip().endswith(RLM):
                        match = re.search(r"\s*$", current_line_to_check_end) # فضاهای انتهایی
                        if match:
                            idx = match.start()
                            processed_line = current_line_to_check_end[:idx] + RLM + current_line_to_check_end[idx:]
                        else: # اگر هیچ فضای انتهایی نبود
                             processed_line = current_line_to_check_end + RLM
                
                processed_lines.append(processed_line)
            else:
                # اگر خط عمدتا LTR است (مثلا یک خط کد اینلاین یا یک جمله انگلیسی)
                # در اینجا می‌توان LRM اضافه کرد اما ممکن است بیش از حد باشد.
                # فعلا خطوط LTR را دست نخورده رها می‌کنیم.
                processed_lines.append(line)
                
    return "\n".join(processed_lines)
