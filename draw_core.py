from reportlab.pdfbase import pdfmetrics

from config import *


# =========================================================
# 页眉
# =========================================================
def draw_header(c):
    c.setFillAlpha(ALPHA_HEADER)
    c.setFont("UI_FONT", 12)

    c.drawCentredString(
        PAGE_WIDTH / 2,
        PAGE_HEIGHT - 8 * mm,
        "姓名：__________    日期：__________"
    )


# =========================================================
# 绘制页面
# =========================================================
def draw_page(c, char, page_fonts):

    x_start = MARGIN + OFFSET_X

    y_start = PAGE_HEIGHT - MARGIN + OFFSET_Y

    last_col = COLS - 1

    mid_col = COLS // 2

    for row, font_info in enumerate(page_fonts):

        y_top = y_start - row * GRID_SIZE

        y_bottom = y_top - GRID_SIZE

        font_name = font_info["internal"]

        font_display = font_info["display"][:12]

        face = pdfmetrics.getFont(font_name).face

        descent = abs(
            face.descent / 1000 * FONT_SIZE
        )

        for col in range(COLS):

            x = x_start + col * GRID_SIZE

            c.setStrokeAlpha(ALPHA_BORDER)

            c.rect(
                x,
                y_bottom,
                GRID_SIZE,
                GRID_SIZE
            )

            c.setStrokeAlpha(ALPHA_GRID)

            c.setDash(1, 2)

            c.line(
                x,
                y_bottom + GRID_SIZE / 2,
                x + GRID_SIZE,
                y_bottom + GRID_SIZE / 2
            )

            c.line(
                x + GRID_SIZE / 2,
                y_bottom,
                x + GRID_SIZE / 2,
                y_top
            )

            c.line(
                x,
                y_bottom,
                x + GRID_SIZE,
                y_top
            )

            c.line(
                x,
                y_top,
                x + GRID_SIZE,
                y_bottom
            )

            if col == 0 or col == mid_col:

                c.setFillAlpha(ALPHA_DEMO_TEXT)

                c.setFont(
                    font_name,
                    FONT_SIZE
                )

                text_y = (
                    y_bottom
                    + GRID_SIZE * 0.05
                    + descent
                    - 0.6 * mm
                    + TEXT_OFFSET
                )

                try:

                    c.drawCentredString(
                        x + GRID_SIZE / 2,
                        text_y,
                        char
                    )

                except:

                    pass

            if col == last_col:

                c.setFillAlpha(ALPHA_FONT_NOTE)

                c.setFont("UI_FONT", 5)

                # =====================================================
                # 字体备注
                # =====================================================
                font_display = (
                    font_info["display"]
                    .replace(".TTF", "")
                    .replace(".ttf", "")
                    [:12]
                )

                # =====================================================
                # 页面右边界对齐
                # =====================================================
                # text_x = PAGE_WIDTH - 3 * mm
                text_x = PAGE_WIDTH - MARGIN / 2
                text_y = (
                    y_bottom + GRID_SIZE * 0.2
                )

                c.drawRightString(
                    text_x,
                    text_y,
                    font_display
                )

                c.setFillAlpha(ALPHA_DEMO_TEXT)