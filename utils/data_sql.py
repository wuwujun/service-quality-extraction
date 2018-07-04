from utils.connenction_pool import ConnectionPool
from utils.sql import Sql
import os

last_query_id = 0


class DataSql(object):

    def __init__(self):
        self.labelids = ['didizhuanche', 'didichuxing']
        self.tables = ['weibo_crawler']
        self.data_save_path = '../results/{}.txt'
        pass

    def save_weibo_cotent(self):
        global last_query_id

        weibo_content_save_path = self.data_save_path.format(self.labelids[0])
        print(weibo_content_save_path)

        sql_obejct = Sql(self.tables[0], self.labelids[0], last_query_id)
        sql_weibo_count = sql_obejct.query_weibo_count()
        sql_weibo_content = sql_obejct.query_weibo_content()
        print(sql_weibo_count)
        print(sql_weibo_content)

        weibo_count = 0
        weibo_content = ()

        with ConnectionPool() as cp:
            try:
                cp.cursor.execute(sql_weibo_count)
                temp = cp.cursor.fetchone()
                if temp[0] is None:
                    weibo_count = 0
                else:
                    weibo_count = temp[0]
                print(weibo_count)

                cp.cursor.execute(sql_weibo_content)
                weibo_content = cp.cursor.fetchall()

            except Exception as e:
                print(e)

        if weibo_count != 0:
            last_query_id = weibo_count

        with open(weibo_content_save_path, 'a') as f:
            if weibo_content:
                f.write('\n'.join(item[0] for item in weibo_content))
                print('done')
            else:
                print('weibo_crawler表的该列为空')


def main():
    ds = DataSql()
    ds.save_weibo_cotent()


if __name__ == '__main__':
    main()








