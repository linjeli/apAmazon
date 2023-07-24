#!/usr/bin/python
import time
from datetime import datetime
import threading
import pytz
import requests
import json
from lxml import etree
from dateutil.tz import gettz
from dateutil import parser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ssl
# 全局取消ssl验证
ssl._create_default_https_context = ssl._create_unverified_context
# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import logging
# 创建logger对象
logger = logging.getLogger('test_logger')
# 日志等级
logger.setLevel(logging.DEBUG)
# 日志文件
test_log = logging.FileHandler('log.log', 'w', encoding='utf-8')
# 日志级别
test_log.setLevel(logging.DEBUG)
# 日志信息格式
formatter = logging.Formatter('%(asctime)s - %(filename)s - line:%(lineno)d - %(levelname)s - %(message)s -%(process)s')
test_log.setFormatter(formatter)
# 加载文件到logger对象中
logger.addHandler(test_log)

proxies = {
  'http': 'http://fyltl827:Qwert12345@unblock.oxylabs.io:60000',
  'https': 'http://fyltl827:Qwert12345@unblock.oxylabs.io:60000',
}

COOKIE = 'session-id=141-8966403-6060727; ubid-main=130-7414500-8728762; lc-main=en_US; session-token=CtfJ1dOIHH2Irc68DXziV37vKQpiDEuTnA7qXoUQLBBsYO2ZNMMN764HwOO9KSSVWTW67TMn8/OpMJFCkQmk7m98JtJesC2V8eRBJDJV+QDHUpuPgSyjmU7ArInuf3HoQWLRu2u+8FhsLyh5RQakEbYDrJPbd2ZbIK9jY7TO5SaFRTJYSgu6GejZ1C3ZMKw80QzXZXydLgmPpigl8o6ekX3fuxhDBJud0BSXjZ8S8+qfy55Cse/lx3rtGZhQHPyg; x-main="RoYnjiKNO?tYg8YFfq0JHsTc4YL@B5LdUnygp1AOMUB2F4z?Hbf23W7z4nKX1TDb"; at-main=Atza|IwEBICmVQYzrvrATcvY3VdvcI96MHCysxprBsP7QI9XnjY0phsf3r8LSCuI9vNBOqmWingBqiBKzr12yv6Ab6FwBX3M-lrbPj6zRHN56jny2mWCYwCSejheM7srz1sUIZUP1ve7Q5CZrtlJuXlV6GvSgC5BKBADzvQDKxSzmxEdEM9g6Zd_2HjbyRHCYfCJHHQ0ULxDBP91hj0pVspFGJoOWs5lmKOsejZFUsAcHWQK6P2BiBA; sess-at-main="cF2oZOvHmQCR6Ri1pxHsp1cEzzDRyaCsuKcciSVS/4c="; sst-main=Sst1|PQFFD27UN60f8NGi2W2yOC9oCSdMiBbfy7QGyNWrHlQtMJzDwx_xDKTp0B40X-sdFUaF_2mNQTnkAFBlicZ__CAtMhUjCdbSg4PRzjlvnwffNYm9GkwkDIvlYaB2w1hbVHTy4qDogrnbnrBJHLEhDqw40TCHVq4Gj-ps57FD-FfYPcc2agtwLvZlacYkUG-U2s1I6aH-O7yA3LrfrLRJGOMa_ovtDXPCI4UR-f3MmQev3PoZPU3as9peBAGI9LCf9KdrRQSe2T4olzwDV_0DNtAnk6pDv1xnFdzZfKmIG1BIF6I; i18n-prefs=USD; ac-language-preference=en_US%2F%22RoYnjiKNO%3FtYg8YFfq0JHsTc4YL%40B5LdUnygp1AOMUB2F4z%3FHbf23W7z4nKX1TDb%22; ac-is-Tiered=false%3Astudentdeal0b-20%2F%22RoYnjiKNO%3FtYg8YFfq0JHsTc4YL%40B5LdUnygp1AOMUB2F4z%3FHbf23W7z4nKX1TDb%22; s_fid=32EA63287E71E6C6-136C1D3C94A5432F; s_cc=true; _rails-root_session=VlBQYUcxSE5YTFZsOFk5ZjFtT1JFNlhyNDFQKzNzRS8vUlRjRTJOTmxJLzBZRXo2M3V0NlNFcmt3T0lmUTRPUVlXdEh6QmJ4NDdYS1pOQkpxYlMrSVA2dTV5UFQrcFhGTzc0YXlFd1ArM1YvOFRLcGUrcE9RN0xRTkc1b2dhZ2RQeDQrd3U1cmdvSm42MlRyTVRUaW1VWWZHeUpMVkVSQnRzSkxuTlQvUThEM0RtMWM2YmtFTVM0N1JhemlqRUtuLS1jOXltNkJwbDN1UTFsbDhOVTRzK1BRPT0%3D--64bf3976ff9c9346eda00d7e1b0447676ca41b8c; session-id-time=1721663873'

head = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Cookie": COOKIE,
    "Host": "affiliate-program.amazon.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

def get_category_list():
    try:
        url = 'https://affiliate-program.amazon.com/home/promohub/promocodes?ac-ms-src=nav&type=mpc&active_date_range=0&is_featured_promotions=0&start_date_range=&link_type=&created_days=&category=arts-crafts'
        resp = requests.get(url, headers=head)
        e = etree.HTML(resp.text)
        category_list = e.xpath('//*[@id="ac-promohub-category-filter"]/div/span/div/label/input/@value')
        return category_list
    except Exception as e:
        logger.info(e)

def get_list(category, page_total):
    url = 'https://affiliate-program.amazon.com/home/promohub/promocodes/mpc'
    page = 1
    while True:
        try:
            params = {
                "ac-ms-src": "nav",
                "type": "mpc",
                "active_date_range": "0",
                "is_featured_promotions": "0",
                "start_date_range": "",
                "link_type": "",
                "created_days": "",
                "category": category,
                "store_id": "studentdeal0b-20",
                "page": page
            }
            resp = requests.get(url, headers=head, params=params)
            html = resp.json().get('search_result')
            if html:
                e = etree.HTML(html)
                items = e.xpath('//div[@class="a-section a-spacing-none promotion-row search-result-item promo-item-display"]')
                threads = []
                for item in items:
                    thread = threading.Thread(target=task, args=(item,))
                    threads.append(thread)
                # 启动所有线程
                for thread in threads:
                    thread.start()
                # 等待所有线程执行完成
                for thread in threads:
                    thread.join()
                page += 1
                if page > page_total + 1:
                    break
            else:
                break
        except Exception as e:
            logger.info(e)
            break

def task(item):
    try:
        title = ''.join(item.xpath('.//a[@class="a-link-normal"]/text()')).strip()
        a_link = ''.join(item.xpath('.//a[@class="a-link-normal"]/@href')).strip()
        with open('id_list.txt', 'a+', encoding='utf-8') as f:
            f.write(f"{a_link.split('/')[-1]}\n")
        code = title.split('code')[-1].split(',')[0].strip()
        expire_date_str = title.split(',')[-1].split('while')[0].replace('through', '').strip()
        expire_timestamp = e_timestamp(expire_date_str)
        start_date_str = ''.join(
            item.xpath('.//span[@class="a-size-small a-color-tertiary promo-date-range a-text-normal"]/text()')).split(
            '|')[0].strip()
        s_date_timestamp = s_timestamp(start_date_str)
        product_info = get_product_info(a_link)
        percentage = float(title.split('%')[0].replace('Save', '').strip())
        if product_info:
            for product in product_info:
                listPrice = eval(product[1])
                dealPrice = eval('%.2f' % (percentage / 100 * listPrice))
                discounted_price = round(listPrice - dealPrice, 2)
                # push_sql(product[0], code, discounted_price, listPrice, expire_timestamp, s_date_timestamp)
                logger.info(
                    f'{a_link},{product[0]},{code},{discounted_price},{listPrice},{expire_timestamp},{s_date_timestamp}')
    except Exception as e:
        logger.info(e)

def get_product_info(a_link):
    product_info = []
    head3 = {"x-oxylabs-geo-location": "90201"}
    try:
        resp = requests.get(a_link, headers=head3, verify=False, proxies=proxies)
        e = etree.HTML(resp.text)
        items = e.xpath('//div[@class="a-row grid"]/div')
        if items:
            for item in items:
                try:
                    asin = ''.join(item.xpath('.//a[@class="a-size-base-plus a-link-normal titleLink"]/@href')).split('?')[0]
                    asin = ''.join([i for i in asin.split('/') if 'B' in i])
                    price = ''.join(item.xpath('.//span[@class="a-offscreen"]/text()')).replace('$', '')
                    product_info.append([asin, price])
                except:
                    continue
        return product_info
    except Exception as e:
        logger.info(e)

def push_sql(asin, code, dealPrice, listPrice, expire, start_date):
    # 上传数据库
    try:
        time.sleep(0.2)
        head2 = {"Content-Type": "application/json"}
        api = 'https://us-central1-dealshunter-dev.cloudfunctions.net/importAmazonDeals'
        data = {
            "deals": [
                {
                    "asin": asin,
                    "code": code,
                    "dealPrice": {
                        "amount": dealPrice,
                        "currency": "USD",
                    },
                    "listPrice": {
                        "amount": listPrice,
                        "currency": "USD"
                    },
                    "source": "amazon",
                    "expire": expire,
                    "start_date": start_date
                }
            ]
        }
        return requests.post(api, headers=head2, data=json.dumps(data), timeout=5, verify=False).status_code
    except Exception as e:
        logger.info(e)

def e_timestamp(date_string):
    try:
        # 手动解析日期和月份
        month, day = map(int, date_string.split('/'))
        # 定义PDT时区
        pdt = pytz.timezone('America/Los_Angeles')
        # 构建带有时区信息的datetime对象
        dt_object = pdt.localize(datetime(2023, month, day, 23, 59, 59))
        # 将PDT时区的datetime对象转换为时间戳（以秒为单位）
        timestamp = int(dt_object.timestamp())
        return timestamp
    except Exception as e:
        logger.info(e)

def s_timestamp(date_string):
    try:
        # 定义PDT时区
        pdt = pytz.timezone('America/Los_Angeles')
        # 解析日期时间部分
        dt_object = datetime.strptime(date_string[:-4], "%b %d, %Y at %I:%M %p")
        # 手动添加PDT时区信息
        dt_object_pdt = pdt.localize(dt_object.replace(year=2023))
        # 将PDT时区的datetime对象转换为时间戳（以秒为单位）
        timestamp = int(dt_object_pdt.timestamp())
        return timestamp
    except Exception as e:
        logger.info(e)

if __name__ == '__main__':
    # category_list = get_category_list()
    # print(category_list)
    category_list = [
        ['automotive', 100],
        ['baby', 30],
        ['beauty', 100],
        ['wireless-phones', 150],
        ['classical', 150],
        ['apparel', 100],
        ['pc-hardware', 150],
        ['electronics', 150],
        ['grocery', 50],
        ['hpc', 50],
        ['tools', 50],
        ['jewelry', 50],
        ['kitchen', 50],
        ['appliances', 150],
        ['mi', 30],
        ['office-products', 200],
        ['garden', 50],
        ['lawn-garden', 50],
        ['pet-supplies', 150],
        ['shoes', 100],
        ['sporting', 200],
        ['toys', 30],
        ['gamedownloads', 30],
        ['videogames', 30],
        ['watches', 30]
    ]
    for category, page_total in category_list:
        logger.info(f'{category}, {page_total}')
        if category:
            get_list(category, page_total)
