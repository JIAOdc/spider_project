""" @Author: jiaogege"""
from lxml import etree

import requests


post_url = 'https://www.qichamao.com/cert-wall'
headers = {
    'Referer': 'https://github.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Host': 'https://www.qichamao.com'
}


def get_one_page():
    response = requests.get(post_url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def get_page(page):
    session = requests.session()
    post_data = {'page': page, 'pagesize': 100}
    response = session.post(post_url, data=post_data, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


# 解析页面
def parse_page(html):
    print(html)
    etree_html = etree.HTML(html)
    list_boxs = etree_html.xpath('//div[@class="firmwall_list_box"]')
    for list_box in list_boxs:
        result_dict = {}
        company_name = list_box.xpath('//h2[@class="firmwall_list_box toe"]/a/text()')
        result_dict['company_name'] = company_name
        # 公司简介
        company_info = list_box.xpath('//li[@class="firmwall_list_box toe"]/div[@class="firmwall_list_info ellipsisln2"]/text()')
        #
        compactor = list_box.xpath('//h2[@class="firmwall_list_box toe"]/a/text()')
        company_email = list_box.xpath('//h2[@class="firmwall_list_box toe"]/a/text()')
        print(company_name)


def main():
    first_page = get_one_page()
    html = get_page(first_page)
    parse_page(html)



if __name__ == '__main__':
    main()