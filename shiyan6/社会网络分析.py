import urllib.request
from bs4 import BeautifulSoup
import re

# 获取网页内容
url = "https://baike.baidu.com/item/%E4%BA%BA%E6%B0%91%E7%9A%84%E5%90%8D%E4%B9%89/17545218"
response = urllib.request.urlopen(url).read().decode("utf-8")

# 解析内容
cont = BeautifulSoup(response, "html.parser")

# 爬取分集剧情
content = cont.find_all("ul", {"id": "dramaSerialList"})

# 提取并清理内容
content = str(content)
content1 = re.sub(r"<[^>]+>", "", content)

# 写入文件
with open("drama_list.txt", "w", encoding="utf-8") as f:
    f.write(content1)
