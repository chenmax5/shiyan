import requests
import time
import json
from jsonpath import jsonpath

# 设置cookies和headers
cookies = {
    
}

headers = {
    
}

# 打开文件进行写入
with open('weibo.txt', 'w', encoding='utf-8') as f:
    for page in range(1, 101):  # 抓取前100页微博内容
        params = {
            'uid': '2656274875',
            'page': f'{page}',
            'feature': '0',
        }

        try:
            # 发起请求
            response = requests.get('https://weibo.com/ajax/statuses/mymblog', params=params, cookies=cookies, headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                # 解析 JSON 数据
                data = response.json()

                # 提取微博内容
                comments = jsonpath(data, '$.data.list[*]')
                if comments:
                    for comment in comments:
                        # 提取微博内容
                        content = jsonpath(comment, '$.text_raw')[0] if jsonpath(comment, '$.text_raw') else '无内容'
                        
                        # 写入文件，并加换行符
                        f.write(content + '\n')
                        
                else:
                    print("未找到任何评论数据")
            else:
                print(f"请求失败，状态码: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"请求发生错误: {e}")
        except json.decoder.JSONDecodeError:
            print("解析 JSON 时出错，响应内容不是有效的 JSON 数据")

        # 延迟 5 秒，防止请求过快被封禁
        time.sleep(5)
        print(f'第{page}页爬取完成')
