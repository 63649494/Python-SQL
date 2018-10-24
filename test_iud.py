#coding=utf8
import MySQLdb

conn = MySQLdb.Connect(
			host = '127.0.0.1',
                        port = 3306,
    			user = 'root',
    			passwd = 'root',
    			db = 'test1',
    			charset = 'utf8'
			)
						
cursor = conn.cursor()

try:    #防止错误发生
    sql_insert = "insert into user(userid,username) values(10,'name10')"
    sql_update = "update user set username='name51' where userid=5"
    sql_delete = "delete from user where userid<3"

    cursor.execute(sql_insert)
    print.cursor.rowcount  #查看sql对数据库进行了几行的影响
    cursor.execute(sql_update)
    print.cursor.rowcount 
    cursor.execute(sql_delete)
    print.cursor.rowcount 

    conn.commit() #提交，不加 以上操作无效
except Exception as e:  #注意这里是except不是catch
    print e
    conn.rollback() #操作失败回滚操作

cursor.close()
conn.close
