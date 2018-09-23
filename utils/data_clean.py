import csv


class Dataclean(object):

    def __init__(self, filename, data_save_path):
        self.data_save_path = data_save_path
        self.filename = filename
        pass

    def clean_newsflash(self):
        with open(self.data_save_path + self.filename[:-4] + '_text.csv', 'w+', encoding='utf-8') as wf:
            wf_csv = csv.writer(wf)

            with open(self.data_save_path + self.filename) as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    text = row[3]
                    result = [text]
                    wf_csv.writerow(result)



