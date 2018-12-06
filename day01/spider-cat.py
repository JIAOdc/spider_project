import json

import requests
import re
from maoyan_db_helper import *


# 抓二进制资源
def get_resource(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None


# 获取页面信息
def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


# 解析页面
def parse_page(html):
    result_list = []
    # 主演
    pattern = re.compile('<p class="star">(.*?)</p>', re.S)
    actor_items = re.findall(pattern, html)
    # 电影名
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?alt="(.*?)" class.*?', re.S)
    movie_items = re.findall(pattern, html)
    # 排名
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>', re.S)
    rate_items = re.findall(pattern, html)
    # 上映时间
    pattern = re.compile('<p class="releasetime">(.*?)</p>', re.S)
    releasetime_items = re.findall(pattern, html)
    # 评分
    pattern = re.compile('<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>', re.S)
    score_items = re.findall(pattern, html)
    # 封面
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?src="(.*?)"', re.S)
    cover_items = re.findall(pattern, html)
    # print(cover_items)

    # 添加数据库连接
    db = get_connection()
    # 创建游标
    cursor = get_cursor(db)


    # 放列表
    for i in range(len(actor_items)):
        result_dict = {}
        result_dict['actor'] = actor_items[i].strip()
        result_dict['movie'] = movie_items[i]
        result_dict['rate'] = rate_items[i]
        result_dict['releasetime'] = releasetime_items[i].strip()
        result_dict['score'] = ''.join(score_items[i])
        result_dict['cover'] = cover_items[i]

        # 插入数据库
        insert_record(db, cursor, result_dict)

        result_list.append(result_dict)

    # 关闭数据库
    close_connection(db)

    return result_list


# 获取所有页面
def get_all_pages():
    result_list = []
    for i in range(10):
        page = i * 10
        url = 'http://maoyan.com/board/4?offset=' + str(page)
        html = get_page(url)
        one_page_result = parse_page(html)
        result_list.extend(one_page_result)

    return result_list


def write_images_files(result_list):
    for item in result_list:
        cover_url = item['cover']
        filename = cover_url.split('/')[-1].split('@')[0]
        content = get_resource(cover_url)
        with open('./images/%s' % filename, 'wb') as f:  # 写入文件images
            f.write(content)


def save_json(result_list):
    json_text = json.dumps(result_list, ensure_ascii=False)
    with open('.maoyan.json', 'w', encoding='utf-8') as f:
        f.write(json_text)


def main():
    # html = get_page('http://maoyan.com/board/4')
    # # print(html)
    # result_list = parse_page(html)
    # print(len(result_list))
    # print(result_list)
    result_list = get_all_pages()
    # print(result_list)
    write_images_files(result_list)
    save_json(result_list)


if __name__ == '__main__':
    main()
