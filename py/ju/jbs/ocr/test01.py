import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pandas as pd

# -------------------------- 配置（根据你的环境修改） --------------------------
# Windows需指定Tesseract安装路径，Mac/Linux无需这行
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
IMAGE_PATH = "D:\\time\\3.png"  # 替换为你这张图片的本地路径


# -----------------------------------------------------------------------------


def preprocess_table_image(image_path):
    """表格图片预处理：增强对比度+二值化+降噪（提升表格文字识别率）"""
    # 1. 打开图片
    img = Image.open(image_path).convert('L')  # 直接转为灰度图

    # 2. 增强对比度（让表格文字和背景更分明）
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(3.0)  # 对比度倍数，可根据图片调整（2-4之间）

    # 3. 二值化（转为黑白，去除灰色干扰）
    threshold = 180  # 阈值，根据图片亮度调整（150-200之间）
    img = img.point(lambda x: 255 if x > threshold else 0)

    # 4. 降噪（去除表格线条/小噪点）
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # 可选：保存预处理后的图片（用于调试）
    img.save("processed_table.png")
    return img


def ocr_table_image(image_path):
    """识别表格图片，返回结构化的DataFrame"""
    # 1. 图片预处理
    processed_img = preprocess_table_image(image_path)

    # 2. 调用Tesseract识别（指定中英文混合）
    # --psm 6：假设图片是单一文本块（表格属于这种场景）
    ocr_result = pytesseract.image_to_string(
        processed_img,
        lang='chi_sim',  # 中文+英文（数字）
        config='--psm 6'
    )

    # 3. 处理识别结果：按行分割，再按空格分割列
    rows = [line.strip() for line in ocr_result.split('\n') if line.strip()]  # 过滤空行
    table_data = []
    for row in rows:
        # 按多个空格分割列（表格列之间是空格分隔）
        cols = [col.strip() for col in row.split() if col.strip()]
        table_data.append(cols)

    # 4. 转为DataFrame（方便查看和后续处理）
    # 假设表格有4列（序号、姓名、列3、列4，可根据实际调整列名）
    df = pd.DataFrame(table_data, columns=["列1", "列2", "列3", "列4"])
    return df


if __name__ == "__main__":
    # 执行识别
    table_df = ocr_table_image(IMAGE_PATH)

    # 打印结果
    print("识别结果（表格）：")
    print(table_df)

    # 可选：保存为Excel/CSV
    table_df.to_excel("识别结果.xlsx", index=False)
    print("结果已保存到：识别结果.xlsx")