import os
import PyPDF2
import re

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

def merge_pdfs(pdf_paths, output_path):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_paths:
        with open(pdf, 'rb') as file:
            pdf_merger.append(file)
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pdf_files = get_all_pdfs_in_directory(current_directory)
    if pdf_files:
        output_pdf = os.path.join(current_directory, '合并.pdf')
        merge_pdfs(pdf_files, output_pdf)
        print(f'Merged {len(pdf_files)} PDF files into "{output_pdf}"')
    else:
        print('No PDF files found in the directory.')

if __name__ == '__main__':
    main()
