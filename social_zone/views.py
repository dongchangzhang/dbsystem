#!/usr/bin/env python3
'''
db exp3
'''
from social_zone.dboperator import *
from django.shortcuts import render

# Create your views here.

def social(request):
    conn = connect_mysql()
    print(search(conn, 'select * from mail'))
    conn.close()
    return render(request, 'social.html')
def sign(request):
    # sign in
    if 'smail' in request.POST:
        mail = request.POST['smail']
        passwd = request.POST['spasswd']
        if not sign_in(request, mail, passwd):
             return render(request, 'error.html')
    # sign up
    elif 'name' in request.POST:
        info = []
        info.append(request.POST['name'])
        info.append(request.POST['sex'])
        info.append(str(request.POST['birthday']).replace('-', ''))
        info.append(request.POST['addr'])
        info.append(request.POST['passwd'])
        info.append(request.POST['mail'])

        sign_up(request, info)

    return render(request, 'user.html')
def sign_in(request, mail, passwd):
    sql = 'select passwd, iduser from user where mail = "' + mail + '"'
    conn = connect_mysql()
    r = search(conn, sql)
    conn.close()

    if len(r) == 0 or passwd != r[0][0]:
        return False;
    elif passwd == r[0][0]:
        request.session['user_now'] = r[0][1]
        return True
    else:
        return False
def sign_up(request, info):
    decorate(db_user_decorate, info)
    sql = gen_insert_sql('user', db_user, info)
    conn = connect_mysql()
    r = other_action(conn, sql)
    sql = 'select iduser from user where mail = ' + info[-1]
    r = search(conn, sql)
    request.session['user_now'] = r[0][0]
    conn.close()
def personal(request):
    sql = 'select * from user where iduser = ' + str(request.session['user_now'])
    conn = connect_mysql()
    r = search(conn, sql)
    info = {}
    info['name'] = r[0][1]
    info['sex'] = r[0][2]
    info['birthday'] = str(r[0][3]).replace('-', '')
    info['addr'] = r[0][4]
    info['passwd'] = r[0][5]
    info['mail'] = r[0][6]
    print(info)
    return render(request, 'personal.html', info)

def edu(request):
    sql = 'select * from edu_expe where edu_iduser = ' + str(request.session['user_now'])
    elements = ['idedu', 'level', 'start', 'end', 'school', 'degree', 'user_now']
    conn = connect_mysql()
    r = search(conn, sql)
    info = {}
    List = []
    for e in r:
        print(e)
        List.append(dict(zip(elements, e)))
    info['List'] =  List
    print(len(List))

    return render(request, 'edu.html', info)
def edu_insert(request):
    info = []
    info.append(request.POST['level'])
    info.append(str(request.POST['start']).replace('-', '') )
    info.append(str(request.POST['end']).replace('-', ''))
    info.append(request.POST['school'])
    info.append(request.POST['degree'])
    info.append(request.session['user_now'])
    decorate(db_edu_decorate, info)
    sql = gen_insert_sql('edu_expe', db_edu_expe, info)
    conn = connect_mysql()
    r = other_action(conn, sql)
    conn.close()
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')

def work(request):
    sql = 'select * from work_expe where work_iduser = ' + str(request.session['user_now'])
    elements = ['idwork', 'place', 'start', 'end',  'job', 'user_now']
    conn = connect_mysql()
    r = search(conn, sql)
    info = {}
    List = []
    for e in r:
        print(e)
        List.append(dict(zip(elements, e)))
    info['List'] =  List
    print()

    return render(request, 'work.html', info)
def work_insert(request):
    info = []
    info.append(request.POST['place'])
    info.append(str(request.POST['start']).replace('-', '') )
    info.append(str(request.POST['end']).replace('-', ''))
    info.append(request.POST['job'])
    info.append(request.session['user_now'])
    decorate(db_work_decorate, info)
    sql = gen_insert_sql('work_expe', db_work_expe, info)
    conn = connect_mysql()
    r = other_action(conn, sql)
    conn.close()
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')


def diary(request):
    return render(request, 'diary.html')
def friend(request):
    conn = connect_mysql()
    felements = ['iduser', 'name', 'mail', 'sex', 'birthday']
    sql = 'select iduser, name,  mail, sex, birthday from user, friend where user.iduser = \
    friend.friend and friend_iduser = %s' % request.session['user_now']
    r = search(conn, sql)
    friend = []
    for e in r:
        friend.append(dict(zip(felements, e)))
    sql = 'select iduser, name, '
    group = []
    sql = 'select user.iduser, name, user.mail, groupname from user, friend, \
    friend_group where user.iduser = friend.friend and friend.friend_iduser = %s \
    and friend.friend_idgroup = friend_group.idgroup' % request.session['user_now']
    r = search(conn, sql)
    conn.close()
    info = { 'friend': friend, 'friend_group': group }
    return render(request, 'friend.html', info)
def message(request):
    return render(request, 'message.html')
def user_update(request):
    pass
def add_user():
    pass
def edit_user_info():
    pass
def add_edu_expe():
    pass
def edit_edu_expe():
    pass
def add_work_expe():
    pass
def edit_work_expe():
    pass
def search_friend(request):
    elements = ['iduser', 'name', 'sex', 'birthday', 'addr', 'passwd', 'mail']
    to_search = request.GET['search']
    conn = connect_mysql()
    result = []
    sql = 'select * from user where mail like "%' + str(to_search) + '%"'
    r = search(conn, sql)
    result.extend(r)
    sql = 'select * from user where name like "%' + str(to_search) + '%"'
    r = search(conn, sql)
    result.extend(r)
    conn.close()
    mark = []
    List = []
    for e in result:
        if e[0] not in mark:
            mark.append(e[0])
            List.append(dict(zip(elements, e)))
    info = { 'List' : List}
    if len(List) == 0:
        return render(request, 'error.html')
    else:
        return render(request, 'friend_result.html', info)
def add_friend(request):
    friend = request.GET['friend']
    conn = connect_mysql()
    sql = 'insert into friend (friend_iduser, friend) values( %s, %s)'%  (request.session['user_now'], friend)
    r = other_action(conn, sql)
    conn.close()
    if r != 1:
        return render(request, 'error.html')
    else:
        return render(request, 'successful.html')
def delete_friend():
    return render(request, 'successful.html')

def friend_info(request):
    pinfo = {
        'name': request.GET['name'],
        'iduser': request.GET['iduser'],
        'mail': request.GET['mail'],
        'sex': request.GET['sex'],
        'birthday': request.GET['birthday']
    }
    sql = 'select idgroup, groupname from friend_group where friend_group.iduser=%s' % request.session['user_now']
    conn = connect_mysql()
    r = search(conn, sql)
    conn.close()
    List = []
    elements = ['id', 'group']
    for e in r:
        List.append(dict(zip(elements, e)))
    info = {'List' : List, 'info': pinfo }
    print(info)
    return render(request, 'friend_info.html', info)

def add_group(request):
    group =  request.GET['group_name']
    sql = 'insert into friend_group (groupname, iduser) values("%s", %s)' %(group, request.session['user_now'])
    print(sql)
    conn = connect_mysql()
    r = other_action(conn, sql)
    print(r)
    conn.close()
    return render(request, 'successful.html')
def add_friend_to_group(request):
    id = request.GET['id']
    friend = request.GET['friend']
    user_now = request.session['user_now']
    sql = 'update friend set friend_idgroup=%s where friend_iduser=%s and friend=%s' %(id, user_now, friend)
    conn = connect_mysql()
    r = other_action(conn, sql)
    print(r)
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')

def edit_group():
    pass
def delete_group():
    pass
def publish_diary():
    pass
def edit_diary():
    pass
def delete_diary():
    return render(request, 'successful.html')

def reply_diary():
    pass
def send_message():
    pass
def reply_message():
    pass