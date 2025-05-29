import pandas as pd
import requests

# 读取代理 IP 文件
proxy_file_path = "D:/Study/数据/chinese_proxies.csv"  # 你的代理 IP 文件路径
proxy_df = pd.read_csv(proxy_file_path)
test_url = "https://weibo.com/"

# 生成代理列表（格式：IP:端口）
proxies = proxy_df.apply(lambda row: f"http://{row['ip_address']}:{row['port']}", axis=1).tolist()

print(f"读取到 {len(proxies)} 个代理 IP")

valid_proxies = []

for proxy in proxies:
    try:
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            print(f"✅ 代理可用: {proxy}")
            valid_proxies.append(proxy)
        else:
            print(f"❌ 代理无效: {proxy}")
    except requests.RequestException:
        print(f"❌ 代理超时: {proxy}")

# 将有效代理存储到 Excel 文件
df = pd.DataFrame(valid_proxies, columns=["Valid Proxy"])
df.to_excel("D:/Study/数据/valid_proxies.xlsx", index=False)

print(f"有效代理数量: {len(valid_proxies)}，已保存到 valid_proxies.xlsx")