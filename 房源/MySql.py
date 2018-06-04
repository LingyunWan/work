# -!- coding: utf-8 -!-
import pymysql


# 数据库操作类
class MySql:
    def __init__(self, host, user, password, db, port, charset='utf8'):
        try:
            self.conn = pymysql.connect(host, user, password, db, port, charset=charset)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('连接失败：%s' % str(e))

    # 带查重的增删改
    def exe(self, sql1, sql2):
        try:
            # 查重处理
            self.cursor.execute(sql1)
            repetition = self.cursor.fetchall()
            if repetition:
                print('重复')
                rows = None
            else:
                rows = self.cursor.execute(sql2)
                self.conn.commit()
        except Exception as e:
            # 执行插入失败的话进行回滚,返回到执行插入之前的状态
            self.conn.rollback()
            print('语句增删改执行失败:%s' % str(e))
            print(sql2)
            rows = None
        return rows

    # 不带查重的增删改
    def exec(self, sql):
        try:
            rows = self.cursor.execute(sql)
            self.conn.commit()
            print('语句增删改执行成功')
        except Exception as e:
            # 执行插入失败的话进行回滚,返回到执行插入之前的状态
            self.conn.rollback()
            print('语句增删改执行失败:%s' % str(e))
            rows = None
        return rows

    # 查询方法
    def query(self, sql):
        try:
            self.cursor.execute(sql)
            """
            最近在用python操作mysql数据库时，碰到了下面这两个函数，标记一下：
            fetchone() ：
            返回单个的元组，也就是一条记录(row)，如果没有结果则返回None

            fetchall() ：
            返回多个元组，即返回多个记录(rows), 如果没有结果则返回()
            需要注明：在MySQL中是NULL，而在Python中则是None
            """
            # 查询,有时候符合条件的结果不仅仅是一条，因此需要用fetchall，而不是fetchone
            res = self.cursor.fetchall()
        except Exception as e:
            print('执行查询语句失败：%s' % str(e))
            print(sql)
            res = None
        return res

    # 数据库信息的去重

    # 关闭数据库方法
    def close(self):
        self.cursor.close()
        self.conn.close()
