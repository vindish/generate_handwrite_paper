from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ===== 字体 =====
FONT_PATH = "FONTS\田英章硬笔楷书简体.ttf"
FONT_NAME = "CustomFont"
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

# ===== 页面参数 =====
PAGE_WIDTH, PAGE_HEIGHT = A4

MARGIN = 15 * mm
GRID_SIZE = 12 * mm

ROWS = int((PAGE_HEIGHT - 2 * MARGIN) // GRID_SIZE)
COLS = int((PAGE_WIDTH - 2 * MARGIN) // GRID_SIZE)

FONT_SIZE = GRID_SIZE * 0.90

# ===== 微调参数 =====
OFFSET_X = 0
OFFSET_Y = 0
TEXT_OFFSET = 0


def draw_page(c, chars):
    x_start = MARGIN + OFFSET_X
    y_start = PAGE_HEIGHT - MARGIN + OFFSET_Y

    char_index = 0

    face = pdfmetrics.getFont(FONT_NAME).face
    descent = abs(face.descent / 1000 * FONT_SIZE)

    mid_col = COLS // 2

    for row in range(ROWS):
        y_top = y_start - row * GRID_SIZE
        y_bottom = y_top - GRID_SIZE

        # 每行一个字
        if char_index < len(chars):
            demo_char = chars[char_index]
            char_index += 1
        else:
            demo_char = ""

        for col in range(COLS):
            x = x_start + col * GRID_SIZE

            # ===== 外框 =====
            c.setStrokeAlpha(1)
            c.rect(x, y_bottom, GRID_SIZE, GRID_SIZE)

            # ===== 虚线米字格（40%透明）=====
            c.setStrokeAlpha(0.4)
            c.setDash(1, 2)

            # 横线
            c.line(x, y_bottom + GRID_SIZE / 2, x + GRID_SIZE, y_bottom + GRID_SIZE / 2)
            # 竖线
            c.line(x + GRID_SIZE / 2, y_bottom, x + GRID_SIZE / 2, y_top)
            # 对角线
            c.line(x, y_bottom, x + GRID_SIZE, y_top)
            c.line(x, y_top, x + GRID_SIZE, y_bottom)

            c.setDash()
            c.setStrokeAlpha(1)

            # ===== 示例字 =====
            if demo_char and (col == 0 or col == mid_col):
                c.setFont(FONT_NAME, FONT_SIZE)

                bottom_padding = GRID_SIZE * 0.05 + TEXT_OFFSET

                text_y = y_bottom + bottom_padding + descent -0.6 * mm

                c.drawCentredString(
                    x + GRID_SIZE / 2 + 0.2 * mm,
                    text_y,
                    demo_char
                )


def create_copybook(output, text):
    c = canvas.Canvas(output, pagesize=A4)

    page_capacity = ROWS

    for i in range(0, len(text), page_capacity):
        page_chars = text[i:i + page_capacity]

        draw_page(c, page_chars)
        c.showPage()

    c.save()


if __name__ == "__main__":
    practice_text = list("一二三十人入八大小口日月田山石土日木水火人大")

    create_copybook("output\copybook2.pdf", practice_text)

    print("生成完成")