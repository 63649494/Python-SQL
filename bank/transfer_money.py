# coding:utf8
import sys
import MySQLdb

def check_acct_available(self, acctid):
    cursor = self.conn.cursor()
    try:
        sql = "select * from account where acctid=%s" % acctid
        cursor.execute(sql)
        print "check_acct_available:" + sql
        rs = cursor.fetchall() #把结果集放入变量
        if len(rs) != 1: 
            raise Exception("账号%s不存在" % acctid)
    finally:
        cursor.close()

def has_enough_money(self, acctid, money):
    cursor = self.conn.cursor()
    try:
        sql = "select * from account where acctid=%s and money>%s" % (acctid, money)
        cursor.execute(sql)
        print "has_enough_money:" + sql
        rs = cursor.fetchall() #把结果集放入变量
        if len(rs) != 1:
            raise Exception("账号%s没有足够钱" % acctid)
    finally:
        cursor.close()

def reduce_money(self, acctid, money):
    cursor = self.conn.cursor()
    try:
        sql = "update account set money=money-%s where acctid=%s" % (money, acctid)
        cursor.execute(sql)
        print "reduce_money:" + sql
        rs = cursor.fetchall() #把结果集放入变量
        if cursor.rowcount != 1: #检验update看影响多少条数据！！
            raise Exception("账号%s减款失败" % acctid)
    finally:
        cursor.close()

def add_money(self, acctid, money):
    cursor = self.conn.cursor()
    try:
        sql = "update account set money=money+%s where acctid=%s" % (money, acctid)
        cursor.execute(sql)
        print "add_money:" + sql
        rs = cursor.fetchall() #把结果集放入变量
        if cursor.rowcount != 1: #检验update看影响多少条数据！！
            raise Exception("账号%s加款失败" % acctid)
    finally:
        cursor.close()
        
class TransferMoney(object):
    def __init__(self, conn): #类的构造函数，传入参数conn
        self.conn = conn
    def transfer(self, source_acctid, target_acctid, money): #实现transfer方法
        try:
            self.check_acct_available(source_acctid) #检查两个账号是否可用
            self.check_acct_available(target_acctid)
            self.has_enough_money(source_acctid, money) #检查付款人是否有足够的钱
            self.reduce_money(source_acctid, money) #检测通过，付款人减掉钱
            self.add_money(target_acctid, money) #检测通过，收款人加上钱
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
    
if __name__ == "__main__":  #脚本执行的入口
    source_acctid = sys.argv[1] #设置三个参数：付款人id，收款人id，转账金额
    target_acctid = sys.argv[2]
    money = sys.argv[3]
    
    conn = MySQLdb.Connect(host='127.0.0.1', user='root', passwd='root', port=3306, db='test1') #创建数据库的connection
    tr_money = TransferMoney(conn) #创建转账操作的对象，使用TransferMoney类来实现
    
    try:
        tr_money.transfer(source_acctid, target_acctid, money)
    except Exception as e:
        print "出现问题：" + str(e)
    finally: #无论如何，关闭连接
        conn.close()
