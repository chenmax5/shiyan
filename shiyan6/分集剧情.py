from playwright.sync_api import sync_playwright
import subprocess
import re

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
    page.goto(
        "https://baike.baidu.com/item/%E4%BA%BA%E6%B0%91%E7%9A%84%E5%90%8D%E4%B9%89/17545218"
    )
    page.wait_for_load_state("networkidle")
    page.locator(
        "xpath=//*[@id='J-lemma-main-wrapper']/div[2]/div/div[1]/div/div[6]/div[8]/div/div[1]/a"
    ).click()

    # 写入文件
    with open("drama_list.txt", "w", encoding="utf-8") as f:
        for i in range(11):
            content = page.locator(
                'xpath=//*[@id="J-lemma-main-wrapper"]/div[2]/div/div[1]/div/div[6]/div[8]/div/ul'
            ).inner_text()

            # 提取并清理内容
            content = str(content)
            content1 = re.sub(r"<[^>]+>", "", content)
            f.write(content1)

            page.locator(
                f'xpath=//*[@id="J-lemma-main-wrapper"]/div[2]/div/div[1]/div/div[6]/div[8]/div/div[1]/div/a[{i+1}]'
            ).click()

    # 关闭浏览器连接
    browser.close()


# 使用 Playwright 启动自动化
with sync_playwright() as playwright:
    run(playwright)


