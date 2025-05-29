# import pandas as pd
#
# # 读取CSV文件
# file_path = 'weibo_content.csv'  # 替换为你的CSV文件路径
# df = pd.read_csv(file_path)
#
# # 提取label列为0的数据
# filtered_data = df[df['label'] == 0]
#
# # 将筛选后的数据保存为Excel文件
# output_file = 'non_rumor_weibo.xlsx'  # 指定输出的Excel文件名
# filtered_data.to_excel(output_file, index=False)
#
# print(f"筛选后的数据已保存到 {output_file}")

import pandas as pd

# 读取Excel文件
file_path = 'non_rumor_weibo.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 假设第二列的列名是未知的，我们可以通过列索引来访问它
# 获取第二列的数据
second_column = df.iloc[:, 1]  # 第二列的索引是1（从0开始计数）

# 修改第二列的内容
df.iloc[:, 1] = second_column.apply(lambda x: f"non_rumor_images\\{x}.jpg")

# 查看修改后的数据
print(df)

# 将修改后的数据保存回Excel文件
output_file = 'modified_non_rumor_weibo.xlsx'  # 指定输出的Excel文件名
df.to_excel(output_file, index=False)

print(f"修改后的数据已保存到 {output_file}")