'''
mysql
'''
import pymysql

'''
mysql operation
'''
db_table_name = ['user', 'mail', 'edu_expe', 'work_expe', 'diary', 'diary_reply', 'friend', 'friend_group', 'share', 'message_reply']
db_user = ['name', 'sex', 'birthday', 'addr', 'passwd', 'mail']
db_user_decorate = [1, 1, 0, 1, 1, 1]
db_mail = ['email', 'mail_iduser', 'active']
db_work_expe = ['work_place', 'work_start_time', 'work_end_time', 'work_job', 'work_iduser']
db_work_decorate = [1, 0, 0, 1, 0]
db_edu_expe = ['edu_level', 'edu_start_time', 'edu_end_time', 'edu_schoolname', 'edu_degree', 'edu_iduser']
db_edu_decorate = [1, 0, 0, 1, 1, 0]

def connect_mysql():
    '''
    connect mysql
    '''
    return pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='mydb',charset="utf8")

def search(conn, sql):
    '''
    search by sql
    '''
    cur = conn.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    cur.execute(sql)
    result = [x for x in cur.fetchall()]
    cur.close()
    return result

def other_action(conn, sql):
    '''
    update/insert/delete
    '''
    cur = conn.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    ret = cur.execute(sql)
    conn.commit()
    cur.close()
    return ret

def gen_insert_sql(table_name, table, info):
    print(table)
    print(info)
    xy = zip(table, info)
    want = [x for x in xy if x[1] != '' and x[1] != None]
    cloumn_list = ', '.join([x[0] for x in want])
    value_list = ', '.join([str(x[1]) for x in want])
    sql = 'insert into ' + table_name + ' ( ' + cloumn_list + ' ) values (' + value_list + ')'
    return sql
def decorate(db_decorate, info):
    for i in range(0, len(info)):
        if info[i] != '' and db_decorate[i] == 1:
            info[i] = '"' + info[i] + '"'


