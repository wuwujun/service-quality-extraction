import urllib.request
import urllib
import json
import codecs
import csv
import time
from utils.data_clean import Dataclean


'''
url = http://36kr.com/api/tag/wuliu 查询所有标签为物流的文章
'''


def gen_url(keyword, page=1, per_page=40, entity_type='newsflash', sort='date'):
    params = {'keyword': keyword, 'page': page, 'per_page': per_page, 'entity_type': entity_type, 'sort': sort}
    url_param = urllib.parse.urlencode(params)
    url = "http://36kr.com/api//search/entity-search?" + url_param
    return url


def spider(keyword):
    header = ['时间', '标题', 'url', '内容']
    total_count, page, page_size = 1, 0, 40
    data_save_path = '../../results/36kr/'
    filename = 'wuliu_newsflash.csv'

    with codecs.open(data_save_path + filename, 'w+', encoding='utf8') as cf:
        f_csv = csv.writer(cf)
        f_csv.writerow(header)

        while total_count > page * page_size:
            url = gen_url(keyword=keyword, page=page + 1)
            data = urllib.request.urlopen(url).read().decode('UTF-8')
            data = json.loads(data)['data']
            total_count, page = data['total_count'], data['page']
            if total_count == 0:
                break

            items = data['items']
            for item in items:
                title = item['title']
                text = item['description_text']
                text = ''.join(text.split())  # 去除空格和换行符
                url = item['news_url']
                published_time = item['published_at'][:-6].replace('T', ' ')
                result = [published_time, title, url, text]
                f_csv.writerow(result)

            if page % 10 == 0:
                time.sleep(10)
                print(str(page) + 'th页爬取完成')


def clean(file, path):
    dc = Dataclean(filename=file, data_save_path=path)
    dc.clean_newsflash()

    pass


def main():
    # spider("物流")
    # spider("新零售")
    # spider("电商")
    data_save_path = '../../results/36kr/'
    filename = 'wuliu_newsflash.csv'
    clean(filename, data_save_path)


if __name__ == '__main__':
    main()
