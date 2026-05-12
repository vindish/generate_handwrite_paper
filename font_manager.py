import hashlib
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont as FTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import FONT_DIR
from config import FONT_PRIORITY


# =========================================================
# 禁用字体（不参与加载）
# =========================================================
DISABLED_FONTS = {

    # 重复字体
    "yanzhenqingyanti.ttf",

    # 不适合练字的字体可以继续加
    # "方圆钢笔粉笔字.TTF",

}


# =========================================================
# 检测字体是否支持字符
# =========================================================
def font_supports_char(font_path, char):

    try:

        font = FTFont(str(font_path))

        for table in font["cmap"].tables:

            if ord(char) in table.cmap:
                return True

        return False

    except Exception:

        return False


# =========================================================
# 修复 PostScript Name
# =========================================================
def fix_font_psname(font_path):

    try:

        font = FTFont(str(font_path))

        safe_ps_name = hashlib.md5(
            str(font_path).encode()
        ).hexdigest()[:16]

        for record in font["name"].names:

            if record.nameID == 6:

                try:

                    record.string = safe_ps_name.encode(
                        "ascii"
                    )

                except Exception:
                    pass

        # =================================================
        # 安全临时文件
        # =================================================
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".ttf"
        ) as tmp:

            tmp_path = tmp.name

        font.save(tmp_path)

        return tmp_path

    except Exception as e:

        print(
            f"⚠️ psName 修复失败: "
            f"{font_path} | {e}"
        )

        return None


# =========================================================
# 注册字体
# =========================================================
def register_font(
    safe_name,
    font_path,
    file_name
):

    try:

        pdfmetrics.registerFont(
            TTFont(
                safe_name,
                str(font_path)
            )
        )

        return font_path

    except Exception as e:

        error_text = str(e)

        # =================================================
        # reportlab 字体兼容问题
        # =================================================
        if any(key in error_text for key in [

            "psName",
            "PostScript",
            "name",
            "autoGenerateTTFMissingTTFName",

        ]):

            print(
                f"⚠️ 修复字体名称: "
                f"{file_name}"
            )

            fixed_path = fix_font_psname(
                font_path
            )

            if not fixed_path:

                return None

            pdfmetrics.registerFont(
                TTFont(
                    safe_name,
                    fixed_path
                )
            )

            return Path(fixed_path)

        raise e


# =========================================================
# 加载字体
# =========================================================
def load_fonts(test_char="永"):

    font_list = []

    loaded_display_names = set()

    for file in FONT_PRIORITY:

        # =================================================
        # 禁用字体
        # =================================================
        if file in DISABLED_FONTS:

            print(f"⏭️ 已禁用字体: {file}")

            continue

        font_path = FONT_DIR / file

        # =================================================
        # 文件不存在
        # =================================================
        if not font_path.exists():

            print(f"⚠️ 字体不存在: {file}")

            continue

        # =================================================
        # 去重（按文件名stem）
        # =================================================
        display_name = font_path.stem.lower()

        if display_name in loaded_display_names:

            print(f"⚠️ 重复字体跳过: {file}")

            continue

        safe_name = f"font_{len(font_list)}"

        try:

            # =================================================
            # 注册字体
            # =================================================
            fixed_font_path = register_font(
                safe_name,
                font_path,
                file
            )

            if not fixed_font_path:

                continue

            # =================================================
            # 检测字符支持
            # =================================================
            if not font_supports_char(
                fixed_font_path,
                test_char
            ):

                print(
                    f"⚠️ 缺少字符: "
                    f"{file}"
                )

                continue

            # =================================================
            # 保存
            # =================================================
            font_list.append({

                "internal": safe_name,

                "display": font_path.stem,

                "path": str(fixed_font_path)

            })

            loaded_display_names.add(
                display_name
            )

            print(f"✅ 加载成功: {file}")

        except Exception as e:

            print(
                f"❌ 跳过字体: "
                f"{file} | {e}"
            )

    return font_list