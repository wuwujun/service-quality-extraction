import csv
import jieba
from pyltp import SentenceSplitter


class Dataclean(object):

    def __init__(self, filename, data_save_path):
        self.data_save_path = data_save_path
        self.filename = filename
        self.cleandt_save_path = self.data_save_path + self.filename[:-4] + '_text.csv'
        self.tagdt_save_path = self.data_save_path + self.filename[:-4] + '_tag.csv'
        pass

    # 去除文本中的表情符号emoji和颜文字
    def clean_expression(self):
        pass

    # 取出爬取的36kr新闻快讯的文本内容导入到新文件中存储
    def clean_newsflash(self):
        with open(self.cleandt_save_path, 'w+', encoding='utf-8') as wf:
            wf_csv = csv.writer(wf)

            with open(self.data_save_path + self.filename, encoding='utf-8') as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    text = row[3]
                    result = [text]
                    wf_csv.writerow(result)

    # 标数据之前进行预处理：分句，分词，打'/o '标签
    def tag_data(self):
        content = ''
        with open(self.cleandt_save_path, encoding='utf-8') as f:
            for lines in f.readlines():
                line = lines.strip()
                content += line
        sentences = SentenceSplitter.split(content)

        new_sentences = []
        jieba.load_userdict('../../settings/userdict.txt')
        for sentence in sentences:
            lcut_result = jieba.lcut(sentence, cut_all=False)
            temp = ''
            new_sentence = []
            for word in lcut_result:
                temp += (word + '/o ')
            new_sentence.append(temp)
            new_sentences.append(new_sentence)

        with open(self.tagdt_save_path, 'w+', encoding='utf-8') as wf:
            wf_csv = csv.writer(wf)
            wf_csv.writerows(new_sentences)

    # 对美团数据训练集进行预处理
    def clean_meituan(self):
        with open(self.cleandt_save_path, 'w+', encoding='utf-8') as wf:
            wf_csv = csv.writer(wf)

            with open(self.data_save_path + self.filename, encoding='utf-8') as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    text = row[1]
                    result = [text]
                    wf_csv.writerow(result)
        return self.cleandt_save_path


