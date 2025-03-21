#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
import argparse

def is_vsc_folder(folder_path):
    if os.path.basename(folder_path) in ['.git', '.svn', 'CVS']:
        return True
    else:
        return False

def translate(text, target_lang="en"):
    """
    使用 Google Translate API 翻译文本。
    
    参数:
        text (str): 要翻译的文本
        target_lang (str): 目标语言（默认: 英文 'en'）

    返回:
        str: 翻译后的文本
    """
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",     # 自动检测源语言
        "tl": target_lang,  # 目标语言
        "dt": "t",        # 翻译文本
        "q": text         # 翻译内容
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        translated_text = "".join([item[0] for item in result[0]])
        return translated_text
    except requests.exceptions.RequestException as e:
        print(f"请求翻译 API 失败: {e}")
        return text
    except Exception as e:
        print(f"发生未知错误: {e}")
        return text

def process_text(text, target_lang="en"):
    """
    检测文本中的中文并翻译为目标语言，非中文部分保留原样。
    
    参数:
        text (str): 原始文本
        target_lang (str): 目标语言（默认: 英文 'en'）

    返回:
        str: 翻译后的完整文本
    """
    def translate_match(match):
        chinese_text = match.group()
        translated_txt = translate(chinese_text, target_lang)
        new_text = ' ' + translated_txt.lower() + ' '
        #print(f'{chinese_text} -> {new_text}')
        return new_text
    
    # 仅匹配连续的中文字符，并逐段翻译
    return re.sub(r'[\u4e00-\u9fff]+', translate_match, text)

def process_file(file_path, output_dir, target_lang="en"):
    """
    处理单个文件，翻译中文内容并生成结果文件。
    
    参数:
        file_path (str): 输入文件路径
        output_dir (str): 输出目录路径
        target_lang (str): 目标语言（默认: 英文 'en'）
    """
    try:
        # 读取文件内容
        try:
            with open(file_path, "r+", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"跳过文件 {file_path}: 不是utf-8文本文件")
            return

        # 翻译中文内容
        translated_content = process_text(content, target_lang)

        if translated_content == content:
            return

        # 确保输出目录存在
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 保存结果到输出目录
        if output_dir:
            output_path = os.path.join(output_dir, os.path.basename(file_path))
        else:
            output_path = file_path
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_content)

        print(f"文件处理完成: {file_path} -> {output_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def process_directory(input_dir, output_dir, target_lang="en"):
    """
    递归处理目录中的所有文件。
    
    参数:
        input_dir (str): 输入目录路径
        output_dir (str): 输出目录路径
        target_lang (str): 目标语言（默认: 英文 'en'）
    """
    if is_vsc_folder(input_dir):
        return

    for item in os.listdir(input_dir):
        input_path = os.path.join(input_dir, item)
        if os.path.isdir(input_path):
            print(f'处理目录 {input_path} ...')
            process_directory(input_path, output_dir, target_lang)
        else:
            print(f"处理文件 {input_path} ...")
            process_file(input_path, output_dir, target_lang)


def main():
    """
    主函数，解析命令行参数并启动翻译任务。
    """
    parser = argparse.ArgumentParser(description="检测文本中的中文并翻译为英文。")
    parser.add_argument("inputs", nargs="+", help="输入文件或目录，可以指定多个。")
    parser.add_argument("-o", "--output", help="输出目录，用于保存翻译后的文件。")
    parser.add_argument("-l", "--lang", default="en", help="目标语言代码（默认: 英文 'en'）。")

    args = parser.parse_args()

    for input_path in args.inputs:
        if os.path.isfile(input_path):
            # 处理单个文件
            process_file(input_path, args.output, args.lang)
        elif os.path.isdir(input_path):
            # 处理目录
            process_directory(input_path, args.output, args.lang)
        else:
            print(f"路径无效: {input_path}")

if __name__ == "__main__":
    main()

