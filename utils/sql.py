

class Sql(object):

    def __init__(self, table, labelid, last_query_id):
        self.table_name = table
        self.label_id = labelid
        self.last_query_id = last_query_id

    def query_weibo_content(self):
        sql = 'select text from %s where labelid = "%s" and id > %d' % \
            (self.table_name, self.label_id, self.last_query_id)
        return sql

    def query_weibo_count(self):
        sql = 'select max(id) from %s where labelid = "%s"' % (self.table_name, self.label_id)
        return sql








