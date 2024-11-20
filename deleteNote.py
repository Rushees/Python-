import re
import os
import json
import argparse
import tkinter as tk
from tkinter import filedialog

# 创建主窗口
root = tk.Tk()
root.title("选择目录示例")
root.geometry("400x400")

# 显示选定目录的标签
selected_dir_label = tk.Label(root, text="选定目录路径将显示在此处")
selected_dir_label.pack(pady=20)

# 显示选定目录的标签
selected_output_dir_label = tk.Label(root, text="压缩后文件保存的目录")
selected_output_dir_label.pack(pady=20)

Selected_dir_path = ""

# 选择目录的函数
def select_directory():
    global Selected_dir_path
    # 打开目录选择对话框
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        selected_dir_label.config(text=f"选定的目录: {selected_dir}")
        Selected_dir_path = selected_dir
    else:
        selected_dir_label.config(text="未选择目录")

# 删除一个文件中的注释和空行
# 多行注释不删除
def remove_comments_and_blank_lines_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    # 删除单行注释（排除在字符串中的）
    code = re.sub(r'(?<!["\'])#.*', '', code)
    
    # 删除未赋值的多行注释
    # code = re.sub(
    #     r'(^|\n)\s*(?<!\S)(?<!\S)(?:"""|\'\'\')(.*?)(?:"""|\'\'\')', 
    #     '', 
    #     code, 
    #     flags=re.DOTALL
    # )
    
    # 删除多余的空行
    code = re.sub(r'\n\s*\n', '\n', code)

    return code

# 删除JSON文件中的空格和换行
def minify_json_file(input_file_path, output_file_path):
    # 读取 JSON 文件
    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 将数据写入新文件，去除空格和换行
    with open(output_file_path, 'w', encoding='utf-8') as minified_file:
        json.dump(data, minified_file, ensure_ascii=False, separators=(',', ':'))

# 遍历指定目录下的所有 Python 文件，并删除注释和空行
def process_python_files_in_directory():
    select_out_text = ''
    global Selected_dir_path
    directory_path = Selected_dir_path
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return

    # 定义输出目录路径
    # output_directory = os.path.join(directory_path, 'cleaned_files')
    output_directory = f'{directory_path}_cleaned_files'
    # 如果输出目录不存在，则创建它
    os.makedirs(output_directory, exist_ok=True)

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"Processing file: {file_path}")
            
            # 生成新的文件路径，并保存在输出目录中
            new_file_name = os.path.basename(file_path) 
            new_file_path = os.path.join(output_directory, new_file_name)
            
            if file_name.endswith('.py'):
                cleaned_code = remove_comments_and_blank_lines_from_file(file_path)
                
                # 写入新的文件
                with open(new_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(cleaned_code)
                print(f"Saved cleaned file as: {new_file_path}")
                
            
            if file_name.endswith('.json'):

                minify_json_file(file_path, new_file_path)
                pass
    selected_output_dir_label.config(text=f"压缩后文件保存的目录: {output_directory}")

if __name__ == '__main__':

    # 创建按钮
    select_dir_button = tk.Button(root, text="选择目录", command=select_directory)
    select_dir_button.pack(pady=10)

    # 创建按钮
    select_dir_button = tk.Button(root, text="开始压缩", command=process_python_files_in_directory)
    select_dir_button.pack(pady=10)

    

        # 运行主循环
    root.mainloop()
