from playwright.sync_api import sync_playwright
import subprocess
import pymysql
import time

# 连接 MySQL 数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='******',
    database='hgu',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# 设置 Edge 浏览器路径和调试端口
edge_path = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
debugging_port = "--remote-debugging-port=9222"

# 启动 Edge 浏览器并开放调试端口
command = f'"{edge_path}" {debugging_port}'
subprocess.Popen(command, shell=True)

def run(playwright):
    # 通过 CDP (Chrome DevTools Protocol) 连接到 Edge 浏览器
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")

    # 获取默认的上下文并打开新页面
    context = browser.contexts[0]  # 获取现有的上下文
    page = context.new_page()  # 在该上下文中创建新的页面

    # 导航到指定网页
    page.goto('https://www.cnvd.org.cn/')

    # 等待页面加载完成
    page.wait_for_load_state("networkidle")

    page.goto('https://www.cnvd.org.cn/flaw/typelist?typeId=29')
    page.wait_for_load_state("networkidle")

    try:
        with connection.cursor() as cursor:
            for p in range(100):#爬取前100页
                for i in range(1,11):
                    # 获取指定元素的 title 属性
                    title = page.locator(f'xpath=//*[@id="flawList"]/table/tbody/tr[{i}]/td[1]/a').get_attribute('title')
                    level = page.locator(f'//*[@id="flawList"]/table/tbody/tr[{i}]/td[2]').inner_text()
                    date = page.locator(f'//*[@id="flawList"]/table/tbody/tr[{i}]/td[6]').inner_text()
                    print(title, level, date)
                    # 将数据插入 MySQL 表
                    sql = """
                    INSERT INTO leak (title, level, date)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        level = VALUES(level),
                        date = VALUES(date);
                    """
                    cursor.execute(sql, (title, level, date))
                page.locator('text=下页').click()
                page.wait_for_load_state("networkidle")
                time.sleep(5)
        # 提交事务
        connection.commit()
    finally:
        # 关闭数据库连接
        connection.close()
    # 关闭浏览器连接
    browser.close()

# 使用 Playwright 启动自动化
with sync_playwright() as playwright:
    run(playwright)
