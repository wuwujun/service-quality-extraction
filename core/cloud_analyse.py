from urllib import request
from urllib import parse


def test():
    with open('../results/didizhuanche.txt', encoding='utf-8') as f:
        url_get_base = "https://api.ltp-cloud.com/analysis/"
        args = {
            'api_key': 'w1L626j522EpwyoydgfUkgFfSzLVcsecWioDZgEb',
            'text': '我是中国人.',
            'pattern': 'srl',
            'format': 'plain'
        }
        result = request.urlopen(url_get_base, parse.urlencode(args).encode(encoding='utf8'))
        content = result.read().strip().decode('utf-8')

        print(content)
