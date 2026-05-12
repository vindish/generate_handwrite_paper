from pathlib import Path
from fontTools.ttLib import TTFont

# =========================================================
# 你要搜索的字体名
# =========================================================
TARGETS = [

    # "方正褚遂良楷书 简",
    # "褚遂良",
    # "赵孟頫",
    # "方正赵孟頫楷书 简",
    # "方正赵孟頫行书 简",
    "文征明",
    "灵飞经",
    "钟繇",
    "虞世南",

]

# =========================================================
# 搜索目录
# =========================================================
SEARCH_DIRS = [

    r"C:\Windows\Fonts",

    str(
        Path.home()
        / "AppData"
        / "Local"
    ),

    str(
        Path.home()
        / "AppData"
        / "Roaming"
    ),

]

# =========================================================
# 支持字体格式
# =========================================================
EXTS = {

    ".ttf",
    ".otf",
    ".ttc",

}


# =========================================================
# 搜索字体
# =========================================================
def search_font(font_path):

    try:

        font = TTFont(
            str(font_path),
            fontNumber=0
        )

        names = font["name"].names

        for record in names:

            try:

                text = record.toUnicode()

            except:
                continue

            for target in TARGETS:

                if target in text:

                    print("\n================================")
                    print(f"找到字体: {target}")
                    print(f"文件路径: {font_path}")
                    print(f"nameID: {record.nameID}")
                    print(f"内部名称: {text}")
                    print("================================")

        font.close()

    except:
        pass


# =========================================================
# 主程序
# =========================================================
for base in SEARCH_DIRS:

    base = Path(base)

    if not base.exists():
        continue

    print(f"\n扫描目录: {base}")

    for file in base.rglob("*"):

        if file.suffix.lower() not in EXTS:
            continue

        search_font(file)