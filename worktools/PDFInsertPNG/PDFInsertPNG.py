import os
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import io

# 1. 获取当前运行文件所在目录
current_dir = os.path.dirname(os.path.realpath(__file__))

# 2. 获取“图标.png”文件路径
icon_path = os.path.join(current_dir, "图标.png")

# 3. 遍历当前文件夹及子文件夹下所有PDF文件
def get_pdf_files(root_dir):
    pdf_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.pdf'):
                pdf_files.append(os.path.join(dirpath, filename))
    return pdf_files

pdf_files = get_pdf_files(current_dir)

# 函数：获取PDF页面大小
def get_pdf_page_size(pdf_path):
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    # 将页面宽度和高度转换为 float 类型
    return float(page.mediabox[2]), float(page.mediabox[3])

# 函数：将图标添加到PDF页面
def add_icon_to_pdf(pdf_path, output_pdf_path, icon_path):
    # 读取原始PDF文件
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # 载入图标
    icon = Image.open(icon_path)
    icon_width, icon_height = icon.size  # 单位pixels
    dpi = 72
    icon_width = icon_width * (dpi / 72)   # 单位pt
    icon_height = icon_height * (dpi / 72) # 单位pt

    # 创建一个新的PDF文件，将图标插入到每一页
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        # 获取PDF页面尺寸
        page_width, page_height = float(page.mediabox[2]), float(page.mediabox[3])

        # 计算插入图标的位置
        if round(page_width) == round(595.276):  # A4尺寸的宽度（单位：pt）
            x = page_width - 11.5 * 28.35  # 11.5cm to pt
            y = 5.5 * 28.35  # 5.5cm to pt
        else:
            x = page_width - 8.6 * 28.35
            y = 11.7 * 28.35  # 11.8cm to pt

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # 判断第一页是否为A4尺寸，并只在第一页插入图标
        if round(float(reader.pages[0].mediabox[2])) == round(595.276):  # A4尺寸的宽度（单位：pt）
            # 只在第一页插入图标
            if page_num == 0:
                can.drawImage(icon_path, x, y, width=icon_width, height=icon_height, mask='auto')
        else:
            # 对于其他页面，插入图标
            can.drawImage(icon_path, x, y, width=icon_width, height=icon_height, mask='auto')

        can.save()

        # 生成新的内容
        packet.seek(0)
        
        # 检查 packet 中是否有有效内容
        new_pdf = PdfReader(packet)
        
        if len(new_pdf.pages) > 0:  # 确保有内容
            page.merge_page(new_pdf.pages[0])

        writer.add_page(page)

    # 保存新生成的PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

# 4. 处理每个PDF文件，按原目录结构保存
for pdf_file in pdf_files:
    # 获取相对路径
    relative_path = os.path.relpath(pdf_file, current_dir)
    # 获取新文件夹路径
    new_folder = os.path.join(current_dir, "签字后pdf文件", os.path.dirname(relative_path))
    # 创建新文件夹（如果不存在）
    os.makedirs(new_folder, exist_ok=True)
    
    # 新的输出PDF路径
    output_pdf_path = os.path.join(new_folder, os.path.basename(pdf_file).replace('.pdf', '_Z.pdf'))

    # 给每个PDF添加图标
    add_icon_to_pdf(pdf_file, output_pdf_path, icon_path)
    print(f"Processed {pdf_file}, saved as {output_pdf_path}")
