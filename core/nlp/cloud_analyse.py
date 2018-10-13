import jieba
import json
from pyltp import SentenceSplitter
from urllib import request
from urllib import parse


# 将分词结果切分成几个小部分方便之后通过一次url来处理多段文本
def text_split():
    contents = []
    content = ''
    i = 0

    with open('../../results/didizhuanche.txt', encoding='utf-8') as f:
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


# 分句
def sentence_split():
    content = ''
    with open('../../results/didizhuanche.txt', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines.strip()
            # 去除过短的句子
            if len(line) > 3:
                content += line
    sentences = SentenceSplitter.split(content)
    return list(sentences)


# 分词
def word_split(sentences):
    words_list = []
    jieba.load_userdict('../../settings/userdict.txt')
    for sentence in sentences:
        temple = jieba.cut(sentence, cut_all=False)
        words_list.append(list(temple))
    # print(words_list)
    return words_list

# 使用ltp云api进行处理
def test(contents):

    url_get_base = "https://api.ltp-cloud.com/analysis/"
    i = 0
    for item in contents:
        i += 1
        if i >= 2:
            break
        args = {
            'api_key': 'w1L626j522EpwyoydgfUkgFfSzLVcsecWioDZgEb',
            'text': item,
            'pattern': 'srl',
            'format': 'json'
        }
        response = request.urlopen(url_get_base, parse.urlencode(args).encode(encoding='utf8'))
        result_list = response.read().strip().decode('utf-8')  # 将Unicode编码为utf-8
        print(result_list)
        result_list = json.loads(result_list)  # 转换为json格式

        vob_list = []
        for paragraph in result_list:
            for sentence in paragraph:
                for word in sentence:
                    srl = word['arg']
                    if word['pos'] == 'v':
                        if srl:
                            verb = word['cont']
                            flag = False
                            temp = {'verb': '', 'adv': '', 'object': ''}
                            for it in srl:
                                tt = ''
                                for j in range(it['beg'], it['end'] + 1):
                                    tt += sentence[j]['cont']
                                if it['type'] == 'A1':
                                    temp['object'] = tt
                                    flag = True
                                elif it['type'] == 'ADV':
                                    temp['adv'] = tt

                            if flag:
                                temp['verb'] = verb
                                vob_list.append(temp)

        for vob in vob_list:
            print(vob)
            print('\n')


def main():
    try:
        sentences = text_split()
        test(sentences)
        pass

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
