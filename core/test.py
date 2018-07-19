import jieba
import json
import re
from pyltp import SentenceSplitter
from urllib import request
from urllib import parse


# 将分词结果切分成几个小部分方便之后通过一次url来处理多段文本
def text_split():
    contents = []
    content = ''
    i = 0

    with open('../results/didizhuanche.txt', encoding='utf-8') as f:
        for lines in f.readlines():
            i += 1
            if i % 2 == 0:
                i = 0
                print(content)
                print('-' * 60)
                contents.append(content)
                content = ''
                continue
            if len(lines) > 10:  # 去除过短的句子
                content += lines
    return contents


def test(contents):

    url_get_base = "https://api.ltp-cloud.com/analysis/"
    i = 0
    for item in contents:
        i += 1
        if i >= 2:
            break
        args = {
            'api_key': 'w1L626j522EpwyoydgfUkgFfSzLVcsecWioDZgEb',
            'text': '#629神秘橙品首发# 从今日起，滴滴专车全新升级为：礼橙专车.',
            'pattern': 'srl',
            'format': 'json'
        }
        response = request.urlopen(url_get_base, parse.urlencode(args).encode(encoding='utf8'))
        result_list = response.read().strip().decode('utf-8')  # 将Unicode编码为utf-8
        # result_list = json.loads(result_list)  # 转换为json格式

        print(result_list)


def main():
    try:
       pass

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
