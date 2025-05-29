import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# 读取 Excel 文件中的 URL
file_path = "D:/Study/数据/Sina Visitor System.xlsx"
df = pd.read_excel(file_path)
urls = df.iloc[:, 0].dropna().tolist()

# 读取代理 IP
proxy_file_path = "D:/Study/数据/valid_proxies.xlsx"
proxy_df = pd.read_excel(proxy_file_path)
proxies = proxy_df["Valid Proxy"].dropna().tolist()

# 代理索引（用于轮换代理）
proxy_index = 0
N = 5  # 每 5 次更换一次代理

# 解析页面数据
results = []

for i, url in enumerate(urls):
    try:
        # 每 N 次更换代理
        if i % N == 0:
            proxy = proxies[proxy_index]
            proxy_index = (proxy_index + 1) % len(proxies)

        # 设置 Selenium 选项
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f'--proxy-server={proxy}')  # 设置代理

        # 使用随机 User-Agent
        ua = UserAgent()
        chrome_options.add_argument(f"user-agent={ua.random}")

        # **修改 WebDriver 初始化方式**
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        # 访问 URL
        driver.get(url)
        time.sleep(random.uniform(5, 10))  # 随机等待，避免被封

        # 获取页面 HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 查找 "站方判定" 部分
        h1_tag = soup.find("h1", class_="whitetxt")  # 站方判定标题
        if h1_tag and "站方判定" in h1_tag.text:
            p_tag = h1_tag.find_next("p", class_="p")  # 获取下一个<p>标签
            result_text = p_tag.get_text(strip=True) if p_tag else "未找到相关内容"
        else:
            result_text = "无站方判定信息"

        # 存储结果
        results.append({"URL": url, "站方判定": result_text})
        print(f"成功爬取: {url}")

        # 关闭 WebDriver
        driver.quit()

    except Exception as e:
        print(f"访问失败: {url}, 错误: {e}")
        results.append({"URL": url, "站方判定": "爬取失败"})

# 保存为 Excel
output_df = pd.DataFrame(results)
output_file = "D:/Study/数据/Sina_Weibo_判定结果.xlsx"
output_df.to_excel(output_file, index=False)

print(f"爬取完成，数据已保存至 {output_file}")
