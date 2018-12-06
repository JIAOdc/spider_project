import json
import re
import requests



def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')  # 编码出错的解决方法,concent字节流，在将字节流转换成字符串，
    return None
    # print(response.status_code)
    # print(response.text)


def parse_page(html):
    # 电影名
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?alt="(.*?)" class.*?', re.S)
    movie_items = re.findall(pattern, html)

    # 主演
    pattern = re.compile('<p class="star">\n                主演：(.*?)</p>', re.S)
    actor_items = re.findall(pattern, html)
    star_items = []
    for item in actor_items:
        star_items.append(item .strip())

    # 获取上映时间
    pattern = re.compile('<p class="releasetime">上映时间：(.*?)</p> ', re.S)
    time_items = re.findall(pattern, html)

    # 获取排名
    pattern = re.compile("<dd>.*?board-index.*?>(.*?)</i>", re.S)
    rank_items = re.findall(pattern, html)

    # 获取图片链接
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?src="(.*?)"', re.S)
    img_items = re.findall(pattern, html)

    # 简单清晰数据
    # all_star = []
    # star = re.findall()


    movies = []

    for i in range(len(actor_items)):
        one_movie = {}
        one_movie['电影名'] = movie_items[i]
        one_movie['主演'] = star_items[i]
        one_movie['上映时间'] = time_items[i]
        one_movie['排名'] = rank_items[i]
        one_movie['图片路径'] = img_items[i]
        movies.append(one_movie)
    return movies


def write_img(url):
    arr = url.split('@')[0]  # 按@ 符号切割
    filename = arr.split('/')[-1]

    with open('./image/%s' % filename, 'wb') as f:  # 写入文件image
        response = requests.get(url)
        f.write(response.content)



def main(a):
    url = 'http://maoyan.com/board/4?offset='+str(a*10)
    html = get_page(url)
    items =parse_page(html)
    movies.append(items)
    return movies


if __name__ == '__main__':
    movies = []
    for i in range(10):
        main(i)

    json_str = json.dumps(movies, ensure_ascii=False)
    with open('b.json', 'w', encoding='utf-8') as f:
        f.write(json_str)
