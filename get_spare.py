import json
import requests
from datetime import datetime
from send_email import *
import time

today = datetime.today()
day_of_week = today.weekday() + 1

session = requests.Session()

cookies = {
    'PHPSESSID': '***',
    'user_info': '***',
}

with open('cookies.txt','w') as f:
    f.write(json.dumps(cookies))

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'PHPSESSID=tcimhnbac5h8i8gnq6e0iqlka4; user_info=65dee8be8a6fc2f65200001f',
    'Origin': 'https://feishu.nankai.edu.cn',
    'Referer': 'https://feishu.nankai.edu.cn/nkapp/web/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
params = {
    'time': '1709107395000',
}


Spare = {}

while True:
    try:
        # 更新cookie
        file = open('/root/nku/feishu_cookies.txt', 'r')
        js = file.read()
        cookies = json.loads(js)
        session.cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
        
        response = session.post('https://feishu.nankai.edu.cn/Home/Index/refreshInfo', params=params, headers=headers)
        session.cookies.update(session.cookies)
        print(session.cookies)
         with open('/root/nku/feishu_cookies.txt','w') as f:
            f.write(json.dumps(requests.utils.dict_from_cookiejar(session.cookies)))
             
        # 获取数据
        data = {
            'campus': '八里台校区',
            'building': '八里台第二主教学楼',
            'area': 'A',
        }

        response = session.post(
            'https://feishu.nankai.edu.cn/Classroom/Index/fetch',
            params=params,
            headers=headers,
            data=data,
        ).json()

        a = response['result']
        data = {
            'campus': '八里台校区',
            'building': '八里台第二主教学楼',
            'area': 'B',
        }
        response = session.post(
            'https://feishu.nankai.edu.cn/Classroom/Index/fetch',
            params=params,
            headers=headers,
            data=data,
        ).json()

        b = response['result']

        # 读取星期
        today = datetime.today()
        today_of_week = today.weekday() + 1

        Spare[fr'{today_of_week}'] = {'a':a,'b':b}
        file_path = '/root/nku/spare_classroom.json'
        with open(file_path, 'w') as json_file:
            json_str = json.dumps(Spare)
            json_file.write(json_str)  # 添加一个换行符以确保新的 JSON 数据单独一行
        time.sleep(500)


    except Exception as e:

        send_email('空闲教室获取出错' + f'{e}')
        
        break
                                              
