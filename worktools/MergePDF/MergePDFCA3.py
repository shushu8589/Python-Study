import os
import PyPDF2
import re
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject
from decimal import Decimal

def get_all_pdfs_in_directory(directory):
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    pdf_files.sort(key=lambda x: extract_sort_key(os.path.basename(x)))
    return pdf_files

def extract_sort_key(filename):
    match = re.match(r'(\d{5})([a-zA-Z]{2})(\d{2})([a-zA-Z]{2})(\d{2})(TB|DW)?(\d{2})?', filename)
    if match:
        part1, part2, part3, part4, part5, part6, part7 = match.groups()
        part1 = int(part1) if part1 else float('-inf')
        part2 = part2 if part2 else ''
        part3 = int(part3) if part3 else float('-inf')
        part4 = part4 if part4 else ''
        part5 = int(part5) if part5 else float('-inf')
        part6_order = {'TB': 0, 'DW': 1}.get(part6, float('-inf'))
        part7 = int(part7) if part7 else float('-inf')
        return (part1, part2, part3, part4, part5, part6_order, part7)
    return (float('-inf'), '', float('-inf'), '', float('-inf'), float('-inf'), float('-inf'))

def resize_large_pages(pdf_path, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    a3_width, a3_height = Decimal("841.89"), Decimal("1190.55")  # A3 size in points

    for page in reader.pages:
        media_box = page.mediabox
        width = media_box.width
        height = media_box.height

        # Ensure width is the shorter side and height is the longer side, regardless of rotation
        if width < height:
            short_side, long_side = width, height
        else:
            short_side, long_side = height, width

        # Resize pages larger than A3 to A3 size, keeping aspect ratio and scaling the page
        if long_side > a3_height or short_side > a3_width:
            scale_ratio = min(a3_width / short_side, a3_height / long_side)
            new_width = short_side * scale_ratio
            new_height = long_side * scale_ratio
            page.scale_by(float(scale_ratio))

            # Set the page size to A3 and add blank space if needed, ensuring correct orientation
            if width > height:  # Landscape
                page.mediabox = RectangleObject([0, 0, a3_height, a3_width])
                page.trimbox = RectangleObject([0, 0, a3_height, a3_width])
                page.cropbox = RectangleObject([0, 0, a3_height, a3_width])
                translation_x = (a3_height - new_width) / 2
                translation_y = (a3_width - new_height) / 2
            else:  # Portrait
                page.mediabox = RectangleObject([0, 0, a3_width, a3_height])
                page.trimbox = RectangleObject([0, 0, a3_width, a3_height])
                page.cropbox = RectangleObject([0, 0, a3_width, a3_height])
                translation_x = (a3_width - new_width) / 2
                translation_y = (a3_height - new_height) / 2

            # Manually add translation to content stream for centering both horizontally and vertically
            content = page.get_contents()
            if content:
                content.stream = f'q 1 0 0 1 {translation_x} {translation_y} cm {scale_ratio} 0 0 {scale_ratio} 0 0 cm {content.stream} Q'

        writer.add_page(page)

    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

def merge_pdfs(pdf_paths, output_path):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_paths:
        resized_pdf = pdf.replace('.pdf', '_resized.pdf')
        resize_large_pages(pdf, resized_pdf)
        with open(resized_pdf, 'rb') as file:
            pdf_merger.append(file)
        os.remove(resized_pdf)
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pdf_files = get_all_pdfs_in_directory(current_directory)
    if pdf_files:
        output_pdf = os.path.join(current_directory, '合并A3.pdf')
        merge_pdfs(pdf_files, output_pdf)
        print(f'Merged {len(pdf_files)} PDF files into "{output_pdf}"')
    else:
        print('No PDF files found in the directory.')

if __name__ == '__main__':
    main()
