# coding=utf-8
import MySQLdb
import time
__author__ = 'zengyuetian'

'''
操作Mysql的底层库
'''


class MysqlDB(object):
    def __init__(self, host, user, password, database):
        start = time.time()
        print "Connect to mysql database by {0}, it should be only call one time!!!".format(user)
        self._db = MySQLdb.connect(host, user, password, database)
        self._cursor = self._db.cursor()
        end = time.time()
        print "Connection cost {0} seconds.".format(start - end)

    def __del__(self):
        self._db.close()

    def create_database(self, name):
        sql = "create database {0}".format(name)
        self._cursor.execute(sql)
        self._db.commit()

    def drop_database(self, name):
        sql = "drop database if exists {0}".format(name)
        self._cursor.execute(sql)
        self._db.commit()

    def drop_table(self, name):
        sql = "drop table if exists {0}".format(name)
        self._cursor.execute(sql)
        self._db.commit()

    def clear_table(self, name):
        sql = "delete from {0}".format(name)
        self._cursor.execute(sql)
        self._db.commit()

    def insert(self, table, **kwags):
        """
        新增一行数据
        :param table:表
        :param kwags:
        :return:void
        """
        values = [kwags[key] for key in kwags]
        keys = '('
        for key in kwags:
            keys += key
            keys += ','
        keys = keys[0:-1]  # remove "," from the end
        keys += ')'
        values_clause = str(tuple(values))

        # 如果只有一项，那么删除tuple函数自动加上的逗号
        if len(values) < 2:
            print "enter"
            values_clause = values_clause.replace(',', '')

        sql = 'INSERT INTO {0}{1} VALUES{2}'.format(table, keys, values_clause)
        print sql
        self._cursor.execute(sql)
        self._db.commit()

    def delete(self, table, **kwags):
        """
        删除满足条件的数据
        :param table:表
        :param kwags:字典条件
        :return:void
        """
        sentence = ''
        # create the "where" clause
        for key in kwags:
            value = '\'' + str(kwags[key]) + '\''
            sentence = '{0} {1}={2} AND'.format(sentence, key, value)
        sentence = sentence[0:-4]  # remove "AND" from end
        sql = 'DELETE FROM {0} WHERE {1}'.format(table, sentence)
        print sql
        self._cursor.execute(sql)
        self._db.commit()

    def delete_except(self, table, **kwags):
        """
        删除不满足条件的所有数据(慎重使用)
        :param table:表
        :param kwags:字典条件
        :return:void
        """
        sentence = ''
        for key in kwags:
            value = '\'' + str(kwags[key]) + '\''
            sentence = '{0} {1}!={2} AND'.format(sentence, key, value)
        sentence = sentence[0:-4]  # remove "AND" from end
        sql = 'DELETE FROM {0} WHERE {1}'.format(table, sentence)
        print sql
        self._cursor.execute(sql)
        self._db.commit()

    def select(self, table, *args, **kwags):
        """
        查询某些列的数据
        :param table: 表
        :param args: 列
        :param kwags: 条件
        :return:
        """
        columns = ''
        for arg in args:
            columns = '{0}{1}{2}'.format(columns, arg, ',')
        columns = columns[0:-1]  # remove "," from the end
        sentence = ''
        time_sentence = ''

        if 'start_time' in kwags.keys():
            start_time = kwags.pop('start_time')
            time_sentence = time_sentence + 'case_start_time > {0}'.format(start_time)

            if 'end_time' in kwags.keys() and kwags['end_time'] is not None:
                end_time = kwags.pop('end_time')
                time_sentence = time_sentence + ' AND case_start_time < {0}'.format(end_time)
            else:
                kwags.pop('end_time')

        for key in kwags:
            value = '\'' + str(kwags[key]) + '\''
            sentence = '{0} {1}={2} AND'.format(sentence, key, value)

        sentence = sentence[0:-4]
        if '' == sentence:
            sql = 'SELECT {0} FROM {1}'.format(columns, table)
        else:
            sql = 'SELECT {0} FROM {1} WHERE {2}'.format(columns, table, sentence)

        if time_sentence is not '':
            sql = sql + ' AND ' + time_sentence

        print sql
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fuzzy_select(self, table, condition, *args):
        """
        for fuzzy query
        :param table:
        :param condition:
        :param args:
        :return:
        """
        columns = ''
        for arg in args:
            columns = '{0}{1}{2}'.format(columns, arg, ',')
        columns = columns[0:-1]  # remove "," from the end
        if '' == condition:
            sql = 'SELECT {0} FROM {1}'.format(columns, table)
        else:
            sql = 'SELECT {0} FROM {1} WHERE {2}'.format(columns, table, condition)
        print sql
        self._cursor.execute(sql)
        return self._cursor.fetchall()


if __name__ == "__main__":
    pass










