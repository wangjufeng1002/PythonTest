import os
import re

import cv2
import pytesseract
from PIL import Image
import numexpr

from py.ju.jbs.utils import pymysql_comm
from py.ju.jbs.utils import db_sql

# 方法1：使用PIL直接打开图片
def extract_text_with_pil(image_path):
    """
    使用PIL和Tesseract提取文字
    """
    # 打开图片
    image = Image.open(image_path)

    # 提取文字
    text = pytesseract.image_to_string(image, lang='chi_sim')  # 中文简体+英文

    return text


# 方法2：使用OpenCV预处理后提取（效果更好）
def extract_text_with_preprocessing(image_path):
    """
    使用OpenCV预处理图片后提取文字
    """
    # 读取图片
    image = cv2.imread(image_path)

    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 转换为PIL格式
    image_pil = Image.fromarray(binary)

    # 提取文字
    text = pytesseract.image_to_string(image_pil, lang='chi_sim')

    return text


# 方法3：更高级的预处理
def extract_text_advanced(image_path):
    """
    带更多预处理的文字提取
    """
    # 读取图片
    img = cv2.imread(image_path)

    # 调整大小（如果图片太大或太小）
    height, width = img.shape[:2]
    if height > 2000 or width > 2000:
        scale = 2000 / max(height, width)
        img = cv2.resize(img, None, fx=scale, fy=scale)

    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 降噪
    gray = cv2.medianBlur(gray, 3)

    # 自适应阈值二值化
    binary = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # 转换为PIL格式
    image_pil = Image.fromarray(binary)

    # 设置Tesseract配置（提高准确率）
    custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'

    # 提取文字
    text = pytesseract.image_to_string(image_pil,
                                       lang='chi_sim+eng',
                                       config=custom_config)

    return text




def ocr_png(dir_path):
    # listdir = os.listdir(dir_path)

    for i in range(1, 10):
        item_name = str(i) + '.png'
        item_path = os.path.join(dir_path, item_name)  # 自动处理路径分隔符
        print(item_path + "---->start")
        text = extract_text_with_preprocessing(image_path=item_path)
        print(item_path + "---->read finish")
        file = open("D:\\time\\text\\" + item_name.replace(".png", ".txt") + "", "w", encoding='utf-8')
        file.write(text)
        file.flush()
        file.close()
        print(item_path + "---->end")


def is_complex_number(s: str) -> bool:
    """支持复杂数字格式（如 '(123)'、'1+2'），但仅判断纯数字表达式"""
    s = s.strip()
    if not s:
        return False
    try:
        numexpr.evaluate(s)  # 安全解析数字/数学表达式
        return True
    except (ValueError, SyntaxError,KeyError):
        return False

def merge_spaces(text: str) -> str:
    """合并所有连续空白字符（空格、制表符）为单个空格，去除首尾空格"""
    # \s+ 匹配 1 个及以上空白字符（空格、\t、\n 等）
    # 替换为 ' '，最后用 strip() 去除首尾可能多余的空格
    return re.sub(r'\s+', ' ', text).strip()

def data_cleaning(lines):
    valid_lines = []
    for line in lines:
        line = line.replace(",","")
        if len(line) <= 5:
            continue
        if is_complex_number(line[0:5]) is False:
            continue
        valid_lines.append(merge_spaces(line))
    return valid_lines

def analyze():
    dir_path = "D:\\time\\text\\"
    item_paths = os.listdir(dir_path)

    for item_path in item_paths:
        file_text = open(os.path.join(dir_path, item_path), "r", encoding='utf-8').read()
        splits = file_text.split("\n")
        data_cleaning(splits)


# 使用示例
if __name__ == "__main__":

    #ocr_png("D:\\time")
    #analyze()
    #方法1：简单提取
    # print("方法1 - 简单提取:")
    text1 = extract_text_with_preprocessing("D:\\time\\3.png")
    file = open("D:\\time\\text\\2.txt", "w", encoding='utf-8')
    file.write(text1)
    file.flush()
    # for i in range(1, 11):
    #     print(i)


    # lines = text1.split('\n')
    # for line in lines:
    #     job_number = line[0:5]
    #     print(line)

    # print(f"OpenCV版本: {cv2.__version__}")
    # # 尝试读取一张已知存在的图片
    # try:
    #     img = cv2.imread(image_path)
    #     if img is None:
    #         print("无法读取图片，可能是路径问题或文件损坏")
    #     else:
    #         print(f"图片读取成功，尺寸: {img.shape}")
    # except Exception as e:
    #     print(f"错误: {e}")
