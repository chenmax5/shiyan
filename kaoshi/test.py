import requests
from lxml import etree
import csv

baseurl = 'https://www.hgu.edu.cn/'
url = 'https://www.hgu.edu.cn/xww/zhxw.htm'

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}

csv_file = 'news.csv'
csv_headers = ['title', 'content']

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()

    for page in range(1, 175):
        resp = requests.get(url, headers=header)
        resp.encoding = 'utf-8'
        html = resp.text
        tree = etree.HTML(html)

        data = '/html/body/div[6]/div[2]/div[1]//a/@href'
        result = tree.xpath(data)

        for i in result:
            sec_url = baseurl + i[2:]
            resp1 = requests.get(sec_url)
            resp1.encoding = 'utf-8'
            htm = resp1.text
            tree1 = etree.HTML(htm)

            data1 = '/html/body/div[6]/div[2]/form/div/h2/text()'
            title = tree1.xpath(data1)

            data2 = '//*[@id="vsb_content_2"]//p[not(img)]/text()'
            content = tree1.xpath(data2)
            content = ''.join(content)  # 将列表中的文本连接成字符串

            writer.writerow({
                'title': title[0] if title else '',
                'content': content,
            })

        print(f'第{page}页保存成功')
        url = f'https://www.hgu.edu.cn/xww/zhxw/{page}.htm'

print("数据已成功保存到 CSV 文件。")
