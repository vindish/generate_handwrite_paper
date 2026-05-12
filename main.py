import reportlab.rl_config as rl_config

# =========================================================
# 修复 reportlab 字体兼容问题
# =========================================================
if not hasattr(
    rl_config,
    "autoGenerateTTFMissingTTFName"
):

    rl_config.autoGenerateTTFMissingTTFName = 1

import math
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from config import *
from font_manager import *
from draw_core import *

from reportlab.pdfbase import pdfmetrics

# =========================================================
# 注册 UI 字体
# =========================================================
pdfmetrics.registerFont(
    TTFont("UI_FONT", UI_FONT_PATH)
)

# =========================================================
# 创建字帖
# =========================================================
def create_copybook(output_pdf, chars):

    OUTPUT_DIR.mkdir(exist_ok=True)

    fonts = load_fonts(chars[0])

    if not fonts:

        raise Exception("没有可用字体")

    c = canvas.Canvas(
        str(output_pdf),
        pagesize=A4
    )

    for char in chars:

        valid_fonts = []

        for f in fonts:

            if font_supports_char(
                f["path"],
                char
            ):
                valid_fonts.append(f)

        if not valid_fonts:

            print(f"⚠️ 没有字体支持字符: {char}")

            continue

        total_pages = math.ceil(
            len(valid_fonts)
            / MAX_ROWS_PER_PAGE
        )

        for page_index in range(total_pages):

            start = (
                page_index
                * MAX_ROWS_PER_PAGE
            )

            end = (
                start
                + MAX_ROWS_PER_PAGE
            )

            page_fonts = valid_fonts[start:end]

            draw_page(
                c,
                char,
                page_fonts
            )

            draw_header(c)

            c.showPage()

    c.save()

    print(f"\n✅ PDF 生成完成: {output_pdf}")


# =========================================================
# 启动
# =========================================================
if __name__ == "__main__":
    hanzi = "豆"
    practice_text = list(hanzi)
    filename = (f"多页字体字帖_37_{hanzi}_.pdf")
    create_copybook(
        OUTPUT_DIR / filename,
        practice_text
    )