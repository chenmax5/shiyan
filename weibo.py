import requests
import time
import json
from jsonpath import jsonpath

# 设置cookies和headers
cookies = {
    'SCF': 'Amd_6kzqC_0kZoPbAa6DNwKCK_ZpL4LCxjvixu58G7Q7a5BeeHQ9UDFWkZvhR_RS_Nm4szlXO8bilfJuyhk2r1Q.',
    'SINAGLOBAL': '6231718287033.996.1726623010016',
    'ULV': '1726623010017:1:1:1:6231718287033.996.1726623010016:',
    'ALF': '1730617214',
    'SUB': '_2A25L--ItDeRhGeNI41AR-CzIyDSIHXVpeXvlrDV8PUJbkNAGLW_XkW1NSD2QK1mOwkgvX7j5Y9_eXzB_O6dRSa1X',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLK8pvAuBHzoUG4Gxlv0vu5JpX5KMhUgL.Fo-c1hz71hzXe0n2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMfSonEehnESheR',
    'XSRF-TOKEN': 'et0rpPPg8Tj9P7DGZXd5_f-H',
    'PC_TOKEN': '08b47de286',
    'WBStorage': 'fcc86192|undefined',
    'webim_unReadCount': '%7B%22time%22%3A1728025651462%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D',
    'WBPSESS': 'jaJyhdK5CSZZqjrj1lvLA2_GAk4pubuRslufIrqC7tPKeLNWurGjoiUkkzuaPgkE1LcjY5C5ghoUxYj1Z2XlsbO09-g0h_QSXVGAqlqlnzMjZ-xttOXlnbS02fVDvjd2scXJvWE533lZGU_Duckl0A==',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://weibo.com/u/2656274875',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XSRF-TOKEN': 'et0rpPPg8Tj9P7DGZXd5_f-H',
    'client-version': 'v2.46.18',
    'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'server-version': 'v2024.09.26.1',
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
