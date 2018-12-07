import requests
from lxml import etree
import json
import pymongo
from pymongo import MongoClient

from mongo_helper import insert_company

url = 'https://www.qichamao.com/cert-wall'
headers = {
    'Referer': 'https://www.qichamao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Host': 'www.qichamao.com'
}

# 第一页
def get_first_page():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# 第二页之后
def get_page(page):
    session = requests.Session()
    post_data = {'page': page, 'pagesize': 100}

    response = session.post(url, post_data, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


# 解析第一页
def parse_first_page(html):
    # print(html)
    result_list = []
    etree_html = etree.HTML(html)
    list_boxs = etree_html.xpath('//div[@class="firmwall_list_box"]')
    for item in list_boxs:
        result_dict = {}

        result_dict['company_name'] = item.xpath('.//h2[@class="firmwall_list_tit toe"]/a/text()')[0]
        # print(company_name)

        result_dict['contact_info'] = item.xpath('.//li[@class="firmwall_list_citem"]/div[@class="firmwall_list_cinfo"]/text()')[0]
        # print(contact_info)

        result_dict['contactor'] = item.xpath('.//li[@class="firmwall_list_citem firmwall_list_citem2"]/div[@class="firmwall_list_cinfo"]/text()')[0]
        # print(contactor)

        email = item.xpath('.//div[@class="firmwall_list_cinfo"]/text()')
        if len(email) > 2:
            email = email[2]
            # print(email[2])
        else:
            email = ''
        result_dict['email'] = email
        # 插入MongoDB数据库中
        insert_company(result_dict)
        result_list.append(result_dict) 
    return result_list   

# 解析json数据
def parse_json(html):
    result_json = json.loads(html)
    data_list = result_json['dataList']
    result_list = []
    for item in data_list:
        result_dict = {}
        result_dict['company_name'] = item.get('CompanyName', '')    
        result_dict['contactor'] = item.get('c_name', '')    
        result_dict['contact_info'] = item.get('c_phone', '')    
        result_dict['email'] = item.get('c_email', '')    
        result_list.append(result_dict)
        # 插入MongoDB
        insert_company(result_dict)
    return result_list

def main():
    first_page = get_first_page()
    # print(first_page)
    result_list = parse_first_page(first_page)
    # print(result_list)

    page = 2
    while True:
        print(page)
        html = get_page(page)
        # print(html)
        json_results = parse_json(html)
        if len(json_results) == 0:
            break

        print(json_results)
        print(len(json_results))
        page += 1


if __name__ == '__main__':
    main()