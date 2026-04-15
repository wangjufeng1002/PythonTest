import easyocr


def ocr_with_easyocr(image_path, langs=['ch_sim', 'en']):
    """
    使用EasyOCR进行OCR识别

    参数:
        image_path: 图片路径
        langs: 语言列表 (默认中文简体和英语)

    返回:
        识别出的文本
    """
    try:
        # 创建reader对象，指定语言
        reader = easyocr.Reader(langs)

        # 读取图片
        result = reader.readtext(image_path)

        # 提取文本
        texts = [detection[1] for detection in result]

        return '\n'.join(texts)
    except Exception as e:
        print(f"OCR处理出错: {e}")
        return ""


# 使用示例
if __name__ == "__main__":
    image_path = "D:\\测试文件\\工时\\09\\1.png"  # 替换为你的图片路径
    result = ocr_with_easyocr(image_path)
    print("识别结果:")
    print(result)