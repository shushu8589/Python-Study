#需要安装pandas openpyxl模块，安装代码：pip install pandas openpyxl
#2024年7月6日
#功能：把当前文件夹下data.xlsx文件中的第A列数据读取后查询当前文件夹下有无对应开头的pdf文件，如果有，就重命名文件，以A1+空格+B2形式重命名
import os
import pandas as pd
import glob

# 读取Excel文件
def read_excel(file_path):
    df = pd.read_excel(file_path, sheet_name='rename', header=None, engine='openpyxl')
    print(df.columns)  # 打印列名
    return df

# 查找并重命名PDF文件
def rename_pdfs(excel_file, directory):
    df = read_excel(excel_file)
    total_rows = len(df)

    for index in range(0, total_rows - 1, 2):  # 每次跳过两行
        current_row = df.iloc[index]  # 当前行
        next_row = df.iloc[index + 1]  # 下一行

        file_pattern = f"{current_row[1].strip()}*.pdf"  # 查找以A列数据开头的PDF文件
        file_list = glob.glob(os.path.join(directory, file_pattern))

        if file_list:
            for old_file_path in file_list:
                file_base_name = os.path.basename(old_file_path)
                new_name = f"{current_row[1].strip()} {next_row[2].strip()}.pdf"  # 新文件名
                new_file_path = os.path.join(directory, new_name)
                os.rename(old_file_path, new_file_path)
                print(f'Renamed {file_base_name} to {new_name}')
        else:
            print(f'No files found starting with {current_row[1]}')

# 主程序
if __name__ == '__main__':
    directory = os.getcwd()  # 获取当前工作目录
    #directory = os.path.join(directory, 'worktools')
    #exc_directory = os.path.join(directory, '测试')  # 定位到子文件夹
    excel_file = os.path.join(directory, 'data.xlsx')  # 指定Excel文件的完整路径
    rename_pdfs(excel_file, directory)

