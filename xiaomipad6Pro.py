from playwright.sync_api import sync_playwright
import subprocess
import time
import csv

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

    page.goto('https://item.jd.com/100056375403.html')
    page.wait_for_load_state("networkidle")
    time.sleep(5)
    with open('小米平板6pro_comments.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['用户', '评论内容', '样式', '机型', '评论时间'])

        for p in range(100):#爬取前100页
            for i in range(1,11):
                user = page.locator(f'xpath=//*[@id="comment-0"]/div[{i}]/div[1]/div[1]').inner_text()
                content = page.locator(f'xpath=//*[@id="comment-0"]/div[{i}]/div[2]/p').inner_text()
                style = page.locator(f'xpath=//*[@id="comment-0"]/div[{i}]/div[2]/div[@class]/div[1]/span[1]').inner_text()
                specification = page.locator(f'xpath=//*[@id="comment-0"]/div[{i}]/div[2]/div[@class]/div[1]/span[2]').inner_text()
                creation_time = page.locator(f'xpath=//*[@id="comment-0"]/div[{i}]/div[2]/div[@class]/div[1]/span[51]').inner_text()

                # 将数据写入 CSV 文件
                writer.writerow([user, content, style, specification, creation_time])
                print(user, content, style, specification, creation_time)

            page.locator('text=下一页').click()
            page.wait_for_load_state("networkidle")
            time.sleep(5)

    # 关闭浏览器连接
    browser.close()

# 使用 Playwright 启动自动化
with sync_playwright() as playwright:
    run(playwright)
