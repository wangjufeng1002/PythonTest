
from PyPDF4 import PdfFileReader, PdfFileWriter


def remove_text_watermark(input_path, output_path):
    reader = PdfFileReader(input_path)
    writer = PdfFileWriter()

    for page_num in range(reader.getNumPages()):
        page = reader.getPage(page_num)

        # 1. 移除注释（部分水印以注释形式存在）
        if '/Annots' in page:
            page['/Annots'] = []  # 清空注释

        # 2. 移除图层（针对带图层的水印）
        if '/OCProperties' in page:
            del page['/OCProperties']  # 删除图层属性

        writer.addPage(page)

    # 保存结果
    with open(output_path, 'wb') as f:
        writer.write(f)


# 使用示例
remove_text_watermark('D:\\学习\\中资\\中公-整理\\25版中公教育知识与能力 中学 有目录.pdf', 'output_no_watermark.pdf')