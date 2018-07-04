import os
import re
import jieba
import time
from pyltp import SentenceSplitter
from pyltp import Postagger
from pyltp import Parser
from pyltp import SementicRoleLabeller
from urllib import request
from urllib import parse

LTP_DATA_DIR = '/home/wuwujun/NLP/ltp_data'
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。


# 分句
def sentence_split():
    content = ''
    with open('../results/didizhuanche.txt', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines.strip()
            # 去除过短的句子
            if len(line) > 3:
                content += line
    sentences = SentenceSplitter.split(content)
    # print('\n'.join(sentences))
    # print(type(sentences))
    return list(sentences)


def test(sentences):

    url_get_base = "https://api.ltp-cloud.com/analysis/"
    i = 0
    for item in sentences:
        i += 1
        if i > 10:
            break
        args = {
            'api_key': 'w1L626j522EpwyoydgfUkgFfSzLVcsecWioDZgEb',
            'text': item,
            'pattern': 'srl',
            'format': 'plain'
        }
        result = request.urlopen(url_get_base, parse.urlencode(args).encode(encoding='utf8'))
        content = result.read().strip().decode('utf-8') # 将Unicode编码为utf-8
        print(content)


# 分词
def word_split(sentences):
    words_list = []
    jieba.load_userdict('../settings/userdict.txt')
    for sentence in sentences:
        temple = jieba.cut(sentence, cut_all=False)
        words_list.append(list(temple))
    # print(words_list)
    return words_list


# 词性标注
def word_posttag(words_list):
    tags_list = []
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    for words in words_list:
        temple = postagger.postag(words)
        tags = list(temple)
        tags_list.append(tags)
    postagger.release()

    find_sentence = {}  # 该句分词结果，词性标注结果
    for index, tags in enumerate(tags_list):
        find_sentence[index] = [words_list[index], tags]

    return find_sentence


# 句法分析
def sentence_parse(find_sentence):
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型

    for key, value in find_sentence.items():
        words = value[0]
        postags = value[1]
        arcs = parser.parse(words, postags)
        find_sentence[key].append(arcs)
        # print(words)
        # print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

    parser.release()

    # for value in find_sentence.values():
    #     print(value[0])
    #     print(value[1])

    return find_sentence


# 语义角色标注
def sentence_label(parse_result):
    labeller = SementicRoleLabeller()  # 初始化实例
    labeller.load(srl_model_path)  # 加载模型
    i = 0
    final_result = []

    for key, value in parse_result.items():
        i += 1
        if i % 50 == 0:
            print('休息一下')
            time.sleep(5)
        words = value[0]
        postags = value[1]
        arcs = value[2]
        roles = labeller.label(words, postags, arcs)

    print('done')
    print(final_result)
    labeller.release()


def main():
    try:
        print('分句')
        sentences = sentence_split()
        test(sentences)
        # print('分词')
        # words_list = word_split(sentences)
        # print('词性标注')
        # find_sentence = word_posttag(words_list)
        # print('句法分析')
        # parse_result = sentence_parse(find_sentence)
        # print('语义角色标注')
        # sentence_label(parse_result)

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
