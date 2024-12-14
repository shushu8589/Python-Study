import os
import PyPDF2
import openpyxl
from PyPDF2 import PdfReader

# A1 纸张面积，单位为平方磅（以 72dpi 为计算）
A1_AREA = (594 / 25.4 * 72) * (841 / 25.4 * 72)

# 创建一个新的工作簿并选择活动工作表
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "PDF 信息"

# 写入表头
sheet.append(["序号", "文件全名", "档案号", "文件名", "页数", "当量A1"])

# 读取目录并处理 PDF 文件的函数
def process_pdfs():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pdf_files = []

    # 遍历目录并找到所有 PDF 文件
    for root, _, files in os.walk(current_directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))

    serial_number = 1

    # 处理每个 PDF 文件
    for pdf_file in pdf_files:
        try:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PdfReader(f)
                
                # 获取页数
                num_pages = len(pdf_reader.pages)

                # 计算所有页面的总面积
                total_area = 0
                for i in range(num_pages):
                    page = pdf_reader.pages[i]
                    width = float(page.mediabox.width)
                    height = float(page.mediabox.height)
                    total_area += width * height

                # 将总面积除以 A1 纸张面积
                area_ratio = total_area / A1_AREA

                # 按第一个空格拆分文件名
                file_name = os.path.basename(pdf_file)
                name_parts = file_name.split(' ', 1)
                left_part = name_parts[0]
                right_part = name_parts[1].rsplit('.', 1)[0] if len(name_parts) > 1 else ''

                # 将信息写入 Excel 工作表
                sheet.append([serial_number, file_name, left_part, right_part, num_pages, area_ratio])
                serial_number += 1

        except Exception as e:
            error_file = os.path.join(current_directory, 'err.txt')
            with open(error_file, 'a') as err_file:
                err_file.write(f"处理文件 {pdf_file} 时出错: {e}\n")

# 运行函数
process_pdfs()

# 保存 Excel 工作簿
current_directory = os.path.dirname(os.path.abspath(__file__))
output_pdf = os.path.join(current_directory, 'PDF_Info.xlsx')
wb.save(output_pdf)
