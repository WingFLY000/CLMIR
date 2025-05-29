import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import numpy as np
from PIL import Image
from io import BytesIO
import pyzbar.pyzbar as pyzbar  # 解析二维码
import time

# 设置图片下载目录（相对路径）
IMAGE_SAVE_DIR = "images"  # 图片存储在脚本所在目录下的 "images" 文件夹
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def detect_qr_code(image_data):
    """尝试解析图片中的二维码，返回二维码指向的URL"""
    try:
        image = Image.open(BytesIO(image_data)).convert("L")  # 转换为灰度，提高识别率
        decoded_objects = pyzbar.decode(image)

        for obj in decoded_objects:
            return obj.data.decode("utf-8")  # 返回二维码解析的URL
    except Exception as e:
        print(f"二维码解析失败: {e}")

    return None  # 没有找到二维码


def fetch_url(url, max_retries=3, timeout=10):
    """带重试机制的网页请求"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败（{attempt + 1}/{max_retries}）：{url}, 错误: {e}")
            time.sleep(2)  # 休息2秒后重试
    return None


def download_first_image(url):
    """访问 URL 并下载主要内容的第一张图片"""
    response = fetch_url(url)
    if response is None:
        return ""

    try:
        # 解析网页
        soup = BeautifulSoup(response.content, "html.parser")
        img_tags = soup.find_all("img")  # 找到所有图片

        for img_tag in img_tags:
            img_url = img_tag.get("src")
            if not img_url:
                continue

            img_url = urljoin(url, img_url)  # 处理相对路径
            img_response = fetch_url(img_url)
            if img_response is None:
                continue

            img = Image.open(BytesIO(img_response.content))

            # 解析二维码
            qr_url = detect_qr_code(img_response.content)
            if qr_url:  # 如果是二维码，进入二维码指向的新页面
                print(f"检测到二维码，跳转到新页面: {qr_url}")
                return download_first_image(qr_url)

            # 过滤掉小尺寸图片（二维码一般较小）
            if img.width > 200 and img.height > 200:
                img_filename = os.path.join(IMAGE_SAVE_DIR, os.path.basename(img_url).split("?")[0])  # 去掉URL参数

                # 确保文件扩展名正确
                if not img_filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    img_filename += ".jpg"

                img.save(img_filename)
                return img_filename  # 返回本地图片相对路径

    except Exception as e:
        print(f"无法下载图片: {url}, 错误: {e}")

    return ""  # 下载失败，返回空字符串


def process_excel(input_excel, output_excel):
    """读取 Excel 文件并下载每个 URL 的主要图片"""
    try:
        df = pd.read_excel(input_excel, engine="openpyxl")

        # 确保至少有四列
        if df.shape[1] < 4:
            print("错误：Excel 文件中没有第四列！")
            return

        url_column = df.columns[3]  # 第四列索引为 3
        image_paths = []  # 存储图片相对路径

        for idx, url in enumerate(df[url_column].astype(str)):
            if url.startswith("http"):
                print(f"[{idx + 1}/{len(df)}] 处理 URL: {url}")
                image_path = download_first_image(url)
                image_paths.append(image_path if image_path else "")  # 下载失败则为空
            else:
                image_paths.append("")  # 如果不是URL，保持为空

        # 在新的一列添加图片相对路径
        df["local_image_path"] = image_paths

        # 保存处理后的 Excel 文件
        df.to_excel(output_excel, index=False, engine="openpyxl")
        print(f"数据已处理完成，结果保存在 {output_excel}")

    except Exception as e:
        print(f"Excel 处理失败: {e}")


if __name__ == "__main__":
    input_excel = r"D:\Study\数据\新建文件夹\output5_labeled.xlsx"  # 输入文件路径
    output_excel = r"D:\Study\数据\新建文件夹\output5_labeled_image.xlsx"  # 输出文件路径
    process_excel(input_excel, output_excel)
