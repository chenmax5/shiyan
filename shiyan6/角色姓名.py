import urllib.request
from bs4 import BeautifulSoup


# 获取网页内容
url = "https://baike.baidu.com/item/%E4%BA%BA%E6%B0%91%E7%9A%84%E5%90%8D%E4%B9%89/17545218"
response = urllib.request.urlopen(url).read().decode("utf-8")

# 解析内容
cont = BeautifulSoup(response, "html.parser")

# 爬取名字
name_content = cont.find_all("dl", attrs={"class": "info_HxTJW"})
with open("name.txt", "w", encoding="utf-8") as f:
    for i in name_content:
        name_d = i.get_text().strip().split("\n")[0]
        name = name_d.split("\xa0")[2]
        name = name[0:-2]
        f.write(name.encode("utf-8").decode() + "\n")
