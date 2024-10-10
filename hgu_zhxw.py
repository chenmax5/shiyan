import requests
from lxml import etree
import re
import pymysql

# 基础 URL 和目标 URL
baseurl = 'https://www.hgu.edu.cn/'
url = 'https://www.hgu.edu.cn/xww/zhxw.htm'

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}

# 连接 MySQL 数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123.com',
    database='hgu',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    for page in range(1, 158):
        # 请求主页面
        resp = requests.get(url, headers=header)
        resp.encoding = 'utf-8'
        html = resp.text
        tree = etree.HTML(html)

        # 提取新闻文章的链接
        data = '/html/body/div[6]/div[2]/div[1]//a/@href'
        result = tree.xpath(data)

        with connection.cursor() as cursor:
            for i in result:
                # 完整的新闻文章 URL
                sec_url = baseurl + i[2:]
                resp1 = requests.get(sec_url)
                resp1.encoding = 'utf-8'
                htm = resp1.text
                tree1 = etree.HTML(htm)

                # 提取新闻标题
                data1 = '/html/body/div[6]/div[2]/form/div/h2/text()'
                title = tree1.xpath(data1)

                # 提取新闻内容
                data2 = '//*[@id="vsb_content_2"]//p[not(img)]/text()'
                content = tree1.xpath(data2)
                content = ''.join(content)  # 将列表中的文本连接成字符串

                # 提取其他信息：发布时间、来源、作者、编辑
                data3 = re.compile('<span style="display: flex;justify-content: center;">.*?发布时间：(?P<发布时间>.*?)&nbsp;.*?来源：(?P<来源>.*?)&nbsp;.*?作者：(?P<作者>.*?)&nbsp;.*?编辑：(?P<编辑>.*?)</span>')
                result3 = data3.finditer(htm)

                # 提取浏览次数
                url2 = 'https://www.hgu.edu.cn/system/resource/code/news/click/dynclicksbatch.jsp'
                q = str(sec_url)
                w = re.compile('([0-9]+)')
                a = w.finditer(q)
                for i in a:
                    params = {
                        'clickids': f'{i.group()}',
                        'owner': '1265528620',
                        'clicktype': 'wbnews'
                    }
                resp2 = requests.get(url=url2, params=params)
                sum = resp2.text

                for match in result3:
                    dic = match.groupdict()
                    pub_time = dic['发布时间']
                    source = dic['来源']
                    author = dic['作者']
                    editor = dic['编辑']

                    # 将数据插入 MySQL 表
                    sql = """
                    INSERT INTO news_data (title, content, pub_time, source, author, editor, sum)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        content = VALUES(content),
                        pub_time = VALUES(pub_time),
                        source = VALUES(source),
                        author = VALUES(author),
                        editor = VALUES(editor),
                        sum = VALUES(sum);
                    """
                    cursor.execute(sql, (title, content, pub_time, source, author, editor, sum))

        # 提交事务
        connection.commit()
        print(f'第{page}页保存成功')
        url = f'https://www.hgu.edu.cn/xww/zhxw/{page}.htm'

finally:
    # 关闭数据库连接
    connection.close()

print("数据已成功保存到数据库。")
