import os
import jieba
from pyltp import SentenceSplitter
from pyltp import Postagger
from pyltp import Parser
from pyltp import SementicRoleLabeller

LTP_DATA_DIR = '/home/wuwujun/NLP/ltp_data'
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'srl')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
TRIGGER_WORDS = ['送出', '抽', '抽取', '赢得', '赢取', '送', '领取', '获得', '获', '享受', '享', '减免']


def sentence_split():
    content = ''
    with open('test.txt', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines.strip()
            content += line
    sentences = SentenceSplitter.split(content)
    # print('\n'.join(sentences))
    # print(type(sentences))
    return list(sentences)


def word_split(sentences):
    words_list = []
    jieba.load_userdict('userdict.txt')
    for sentence in sentences:
        temple = jieba.cut(sentence, cut_all=False)
        words_list.append(list(temple))
    # print(words_list)
    return words_list


def word_posttag(words_list):
    tags_list = []
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    for words in words_list:
        temple = postagger.postag(words)
        tags = list(temple)
        tags_list.append(tags)
    postagger.release()

    find_sentence = {}  # 找到的含有触发词的句子的位置:该句分词结果，词性标注结果
    for index, tags in enumerate(tags_list):
        for tag_index, tag in enumerate(tags):
            temp = []
            # count = 0
            # flag = True
            if (tag == 'v') & (words_list[index][tag_index] in TRIGGER_WORDS):
                # count += 1
                # if words_list[index][tag_index] == '送':
                # if count <= 1:
                # flag = False
                # if flag:
                temp.append(words_list[index])  # 分词结果
                temp.append(tags)  # 词性标注结果
                find_sentence[index] = temp
                break

    # print(find_sentence)
    return find_sentence


def sentence_parse(find_sentence):
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型

    for key, value in find_sentence.items():
        words = value[0]
        postags = value[1]
        arcs = parser.parse(words, postags)
        find_sentence[key].append(list(arcs))

    parser.release()
    return find_sentence


def sentence_label(parse_result):
    labeller = SementicRoleLabeller()  # 初始化实例
    labeller.load(srl_model_path)  # 加载模型

    for key, value in parse_result.items():
        words = value[0]
        postags = value[1]
        arcs = value[2]
        print(arcs)
        # roles = labeller.label(words, postags, arcs)
        # for role in roles:
        # print (role.index,
        # "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

    labeller.release()


def main():
    try:
        sentences = sentence_split()
        words_list = word_split(sentences)
        # print(words_list)
        print('done')
        find_sentence = word_posttag(words_list)
        print('done')
        parse_result = sentence_parse(find_sentence)
        print('done')
        # sentence_label(parse_result)

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()

