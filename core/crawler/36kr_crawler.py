import urllib.request
import urllib
import json
import codecs
import csv
import time


'''
entity_type=newsflash,目前爬取的是快讯内容,因此数据表kr_crwaler中text项的类型为mediumtext
另外,url = http://36kr.com/api/tag/wuliu 查询所有标签为物流的文章
'''


def gen_url(keyword, page=1, per_page=40, entity_type='newsflash'):
    params = {'keyword': keyword, 'page': page, 'per_page': per_page, 'entity_type': entity_type}
    url_param = urllib.parse.urlencode(params)
    url = "http://36kr.com/api//search/entity-search?" + url_param
    return url


def spider(keyword):
    header = ['时间', '标题', 'url', '内容']
    total_count, page, page_size = 1, 0, 40

    with codecs.open('../../results/wuliu_newsflash.csv', 'w+', encoding='utf8') as cf:
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
                url = item['news_url']
                published_time = item['published_at'][:-6].replace('T', ' ')
                print(published_time)
                result = [published_time, title, url, text]
                f_csv.writerow(result)

            if page % 10 == 0:
                time.sleep(10)
                print(str(page) + 'th页爬取完成')


def main():
    spider("物流")


if __name__ == '__main__':
    main()