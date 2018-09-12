import urllib.request
import urllib
import json
import codecs
import csv
import time

def gen_url(query, order_type='time', limit=20, cursor=1):
    params = {'query': query, 'cursor': cursor, 'limit': limit, 'order_type': order_type}
    url_param = urllib.parse.urlencode(params)
    url = "https://api-prod.wallstreetcn.com/apiv1/search/live?" + url_param
    return url


def spider(keyword):
    header = ['内容']
    total_count, page, page_size = 1, 0, 20

    with codecs.open('../../results/wallstreetcn/xls_newsflash.csv', 'w+', encoding='utf8') as cf:
        f_csv = csv.writer(cf)
        f_csv.writerow(header)

        while total_count > page * page_size:
            page += 1
            url = gen_url(query=keyword, cursor=page)
            print(url)
            data = urllib.request.urlopen(url).read().decode('UTF-8')
            data = json.loads(data)['data']
            total_count = data.get('count')
            print(total_count)
            if total_count == 0:
                break
                
            items = data.get('items')
            for item in items:
                text = item['content_text']
                text = ''.join(text.split())  # 去除空格和换行符
                f_csv.writerow(text)

            if page % 10 == 0:
                time.sleep(10)
                print(str(page) + 'th页爬取完成')


def main():
    # spider("物流")
    spider("新零售")
    # spider("电商")


if __name__ == '__main__':
    main()
