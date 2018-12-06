import requests
import re
import json


# 爬取图片
def get_resource(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content     # content返回的就是二进制流文件，这里是和爬取文本的区别。
    return None


# 第一步：请求url，抓取网页信息
def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # return response.content.decode('utf-8')
        return response.text
    return None


# 第二步：解析页面，解析方法
def parse_one_page(html):
    # 获取电影名，  re.S 清除空格
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?alt="(.*?)" class.*?', re.S)
    movie_items = re.findall(pattern, html)


    # 获取主演
    pattern = re.compile('<p class="star">\n                主演：(.*?)</p>', re.S)
    actor_items = re.findall(pattern, html)
    star_items = []
    for item in actor_items:
        star_items.append(item.strip())


    # 获取排名信息
    pattern = re.compile("<dd>.*?board-index.*?>(.*?)</i>", re.S)
    rank_items = re.findall(pattern, html)

    # 获取上映时间,上映地点
    pattern = re.compile('<p class="releasetime">上映时间：(.*?)</p> ', re.S)
    time_items = re.findall(pattern, html)



    # 获取评分???
    pattern = re.compile('<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>', re.S)
    course_items = re.findall(pattern, html)
    list_0 = []
    for item in course_items:
        aa = ''.join(item)
        list_0.append(aa)


    # 封面图片路径
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?src="(.*?)"', re.S)
    img_items = re.findall(pattern, html)

    result_list = []
    for i in range(len(actor_items)):
        result_dict = {}
        result_dict['电影名'] = movie_items[i]
        result_dict['主演'] = star_items[i]
        result_dict['上映时间'] = time_items[i]
        result_dict['排名'] = rank_items[i]
        result_dict['评分'] = list_0[i]
        result_dict['封面图路径'] = img_items[i]
        result_list.append(result_dict)
    return result_list
    # print(result_list)


# 获取所有页面，获取分页
def get_all_pages():
    result_list = []
    for i in range(10):
        page = i * 10
        url = 'http://maoyan.com/board/4?offset='+str(page)
        html = get_page(url)
        one_result_list = parse_one_page(html)
        result_list.extend(one_result_list)
    return result_list


# 获取图片
def write_image_files(result_list):
    for item in result_list:
        cover_url = item['封面图路径']
        filename = cover_url.split('/')[-1].split('@')[0]
        print(cover_url)
        content = get_resource(cover_url)
        with open('./images/%s' % filename, 'wb') as f:  # 写入文件images，wb写入二进制
            f.write(content)


def save_json(result_list):
    json_str = json.dumps(result_list, ensure_ascii=False)  # ensure_ascii=False
    with open('aabb.json', 'w', encoding='utf-8') as f:
        f.write(json_str)


def main():
    url = "http://maoyan.com/board/4"
    html = get_page(url)
    # print(html)
    result_list = get_all_pages()
    write_image_files(result_list)
    # 获取图片
    save_json(result_list)

    # result_list = parse_one_page(html)
    # json_str = json.dumps(result_list, ensure_ascii=False)
    # with open('dudu.json', 'w', encoding='utf-8') as f:
    #     f.write(json_str)
    # print(len(result_list))
    # print(result_list)


if __name__ == '__main__':
    main()