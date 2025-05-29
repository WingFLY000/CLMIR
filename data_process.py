# import json
# import pandas as pd
#
#
# def extract_rumor_text(json_file, output_excel):
#     data = []
#
#     with open(json_file, 'r', encoding='utf-8') as file:
#         for line in file:
#             try:
#                 entry = json.loads(line.strip())
#                 rumor_text = entry.get("rumorText", "")
#                 result = entry.get("result", "")
#                 data.append([rumor_text, result])
#             except json.JSONDecodeError as e:
#                 print(f"Error decoding JSON line: {e}")
#
#     df = pd.DataFrame(data, columns=["rumorText", "result"])
#
#     # 修正：移除 encoding 参数
#     df.to_excel(output_excel, index=False)
#
#     print(f"Data successfully saved to {output_excel}")
#
#
# if __name__ == "__main__":
#     json_file = "./rumors_v170613.json"  # 替换为你的 JSON 文件路径
#     output_excel = r"D:\Study\数据\新建文件夹\output1.xlsx"  # 生成的 Excel 文件路径
#     extract_rumor_text(json_file, output_excel)

# import pandas as pd
# import re
#
# def extract_text_and_url(input_excel, output_excel):
#     # 读取 Excel 文件
#     df = pd.read_excel(input_excel, engine="openpyxl")
#
#     # 定义正则表达式
#     text_pattern = r'“(.*?)”'  # 提取第一个中文引号内的内容
#     url_pattern = r'https?://[^\s，。]+'  # 提取 URL，匹配到第一个中文逗号 `，` 或中文句号 `。` 之前
#
#     # 存储提取的内容
#     extracted_texts = []
#     extracted_urls = []
#
#     for result in df["result"].astype(str):  # 确保数据为字符串
#         # 提取第一个中文引号内的文本
#         text_match = re.search(text_pattern, result)
#         extracted_texts.append(text_match.group(1) if text_match else "")
#
#         # 提取第一个 URL（只取到第一个 `，` 或 `。` 之前）
#         url_match = re.search(url_pattern, result)
#         extracted_urls.append(url_match.group(0) if url_match else "")
#
#     # 添加到 DataFrame
#     df["extracted_text"] = extracted_texts
#     df["extracted_url"] = extracted_urls  # 只包含 URL，没有其他多余文本
#
#     # 保存到新的 Excel 文件
#     df.to_excel(output_excel, index=False, engine="openpyxl")
#
#     print(f"数据已成功保存至 {output_excel}")
#
# if __name__ == "__main__":
#     input_excel = r"D:\Study\数据\新建文件夹\a.xlsx"  # 替换为你的输入文件路径
#     output_excel = r"D:\Study\数据\新建文件夹\b.xlsx"  # 替换为你的输出文件路径
#     extract_text_and_url(input_excel, output_excel)


# import pandas as pd
# import re
#
# def clean_extracted_url(input_excel, output_excel):
#     # 读取 Excel 文件
#     df = pd.read_excel(input_excel, engine="openpyxl")
#
#     # 确保至少有四列
#     if df.shape[1] < 4:
#         print("错误：Excel 文件中没有第四列！")
#         return
#
#     # 获取第四列（extracted_url）
#     url_column = df.columns[3]  # 第四列索引为 3
#
#     # 删除 NaN 值（空白行）
#     df = df.dropna(subset=[url_column])
#
#     # 正则匹配包含中文字符
#     chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
#
#     # 转换为字符串并去除前后空格
#     df[url_column] = df[url_column].astype(str).str.strip()
#
#     # 删除包含中文字符的行
#     df = df[~df[url_column].str.contains(chinese_pattern, na=False)]
#
#     # 删除完全为空的行（空字符串）
#     df = df[df[url_column] != ""]
#
#     # 保存到新的 Excel 文件
#     df.to_excel(output_excel, index=False, engine="openpyxl")
#
#     print(f"清理后的数据已保存至 {output_excel}")
#
# if __name__ == "__main__":
#     input_excel = r"D:\Study\数据\新建文件夹\output2.xlsx"  # 替换为你的输入文件路径
#     output_excel = r"D:\Study\数据\新建文件夹\output3.xlsx"  # 替换为你的输出文件路径
#     clean_extracted_url(input_excel, output_excel)


# import pandas as pd
#
# def remove_duplicate_urls(input_excel, output_excel):
#     # 读取 Excel 文件
#     df = pd.read_excel(input_excel, engine="openpyxl")
#
#     # 确保 Excel 至少有四列
#     if df.shape[1] < 4:
#         print("错误：Excel 文件中没有第四列！")
#         return
#
#     # 获取第四列（extracted_url）
#     url_column = df.columns[3]  # 第四列索引为 3
#
#     # 去除 extracted_url 列中的重复值，保留第一次出现的行
#     df_unique = df.drop_duplicates(subset=[url_column], keep='first')
#
#     # 保存去重后的数据到新的 Excel 文件
#     df_unique.to_excel(output_excel, index=False, engine="openpyxl")
#
#     print(f"去重后的数据已保存至 {output_excel}")
#
# if __name__ == "__main__":
#     input_excel = r"D:\Study\数据\新建文件夹\output3.xlsx"  # 替换为你的输入文件路径
#     output_excel = r"D:\Study\数据\新建文件夹\output4.xlsx"  # 替换为你的输出文件路径
#     remove_duplicate_urls(input_excel, output_excel)

# import pandas as pd
# import re
#
# # 读取Excel文件
# file_path = r"D:\Study\数据\新建文件夹\output3.xlsx"
# df = pd.read_excel(file_path)
#
# # 确保第一列是文本列
# column_name = df.columns[0]
#
# # 处理文本：去除中文“：”、英文“,”，并去除前导空白
# df[column_name] = df[column_name].astype(str).str.replace(r'[：:,@]', '', regex=True).str.lstrip()
#
# # 保存清理后的数据
# output_file = r"D:\Study\数据\新建文件夹\output5.xlsx"
# df.to_excel(output_file, index=False)
#
# print(f"清理完成，结果已保存至 {output_file}")

import pandas as pd
import numpy as np

# 读取Excel文件
file_path = r"D:\Study\数据\新建文件夹\b.xlsx"
df = pd.read_excel(file_path)

# 确保列名正确
rumor_col = "rumorText"  # 第一列
extracted_col = "extracted_text"  # 第三列

# 结果存储列表
processed_rows = []

# 遍历每一行数据
for _, row in df.iterrows():
    rumor_text = str(row[rumor_col]).strip()  # 处理 rumorText
    extracted_text = str(row[extracted_col]).strip()  # 处理 extracted_text

    # 在 rumorText 中查找 extracted_text
    match_start = rumor_text.find(extracted_text)

    if match_start != -1:
        # 初始化标注列表，默认标注为 0
        labels = np.zeros(len(rumor_text), dtype=int)

        # 设置匹配到的部分：第一个字符标 1，其余字符标 2
        labels[match_start] = 1
        labels[match_start + 1: match_start + len(extracted_text)] = 2

        # 创建新行数据，保留原有列，并添加 labels
        row_data = row.to_dict()  # 保留所有原始列
        row_data["labels"] = "".join(map(str, labels))  # 以字符串格式存储标签
        processed_rows.append(row_data)

# 仅保留匹配成功的行
df_processed = pd.DataFrame(processed_rows)

# 保存到新的 Excel 文件
output_file = r"D:\Study\数据\新建文件夹\c.xlsx"
df_processed.to_excel(output_file, index=False)

print(f"处理完成，已保存至 {output_file}")

