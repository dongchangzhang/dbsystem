#!/usr/bin/env python3
'''
db exp3
'''
import time
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

        if not sign_up(request, info):
            print("-----------------2")

            return render(request, 'error.html')
    user_name = request.session['user_name']
    info = {'user_name': user_name}

    return render(request, 'user.html', info)


def sign_in(request, mail, passwd):
    sql = 'select passwd, iduser, name from user where mail = "' + mail + '"'
    conn = connect_mysql()

    r = search(conn, sql)
    conn.close()
    if len(r) == 0 or passwd != r[0][0]:
        return False
    elif passwd == r[0][0]:
        request.session['user_now'] = r[0][1]
        request.session['user_name'] = r[0][2]

        return True
    else:
        return False



def sign_up(request, info):
    decorate(db_user_decorate, info)
    sql = gen_insert_sql('user', db_user, info)
    conn = connect_mysql()
    r = other_action(conn, sql)
    sql = 'select iduser, name from user where mail = ' + info[-1]
    r = search(conn, sql)
    request.session['user_now'] = r[0][0]
    request.session['user_name'] = r[0][1]
    conn.close()
    return True


def personal(request):
    sql = 'select * from user where iduser = ' + \
        str(request.session['user_now'])
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
    sql = 'select * from edu_expe where edu_iduser = ' + \
        str(request.session['user_now'])
    elements = ['idedu', 'level', 'start',
                'end', 'school', 'degree', 'user_now']
    conn = connect_mysql()
    r = search(conn, sql)
    info = {}
    List = []
    for e in r:
        e = list(e)
        e[2] = str(e[2]).replace('-', '')
        e[3] = str(e[3]).replace('-', '')
        List.append(dict(zip(elements, e)))
    info['List'] = List
    print(len(List))

    return render(request, 'edu.html', info)


def edu_insert(request):
    info = []
    info.append(request.POST['level'])
    info.append(str(request.POST['start']).replace('-', ''))
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


def edu_update(request):
    sql = "update edu_expe set edu_level='%s', edu_start_time=%s, edu_end_time=%s, edu_schoolname='%s', edu_degree = '%s' where idedu_expe=%s and edu_iduser=%s" % (
        request.POST['level'], request.POST['start'], request.POST['end'], request.POST[
            'school'], request.POST['degree'], request.POST['idedu'], request.session['user_now']
    )
    conn = connect_mysql()
    r = other_action(conn, sql)

    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')


def work(request):
    sql = 'select * from work_expe where work_iduser = ' + \
        str(request.session['user_now'])
    elements = ['idwork', 'place', 'start', 'end',  'job', 'user_now']
    conn = connect_mysql()
    r = search(conn, sql)
    info = {}
    List = []
    for e in r:
        e = list(e)
        e[2] = str(e[2]).replace('-', '')
        e[3] = str(e[3]).replace('-', '')
        List.append(dict(zip(elements, e)))
    info['List'] = List
    print()

    return render(request, 'work.html', info)


def work_insert(request):
    info = []
    info.append(request.POST['place'])
    info.append(str(request.POST['start']).replace('-', ''))
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


def work_update(request):
    sql = "update work_expe set work_place='%s', work_start_time=%s, work_end_time=%s, work_job = '%s' where idwork_expe=%s and work_iduser=%s" % (
        request.POST['place'], request.POST['start'], request.POST['end'], request.POST[
            'job'], request.POST['idwork'], request.session['user_now']
    )
    conn = connect_mysql()
    r = other_action(conn, sql)
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')

# 嵌套查询 查询朋友的和自己的日志


def diary(request):
    sql = 'select DISTINCT iddiary, diary_name, diary_touch, diary_iduser, diary_content, iduser, name  from diary_view, friend where diary_view.iduser in ( \
        select friend from friend where friend_iduser=%s) union select DISTINCT iddiary, diary_name, diary_touch, diary_iduser, diary_content, \
        iduser, name  from diary_view where diary_view.iduser = %s' % (
        request.session['user_now'], request.session['user_now']
    )
    print(sql)
    conn = connect_mysql()
    r = search(conn, sql)
    print(r)
    delement = ['iddiary', 'diary_name', 'diary_touch',
                'diary_iduser', 'diary_content', 'iduser', 'name']
    diarys = []
    for e in r:
        diarys.append(dict(zip(delement, e)))
    info = {'diarys': diarys, 'iduser': request.session['user_now']}
    conn.close()
    return render(request, 'diary.html', info)


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
    group = {}
    sql = 'select user.iduser, name, user.mail, groupname, sex, birthday from user, friend, \
    friend_group where user.iduser = friend.friend and friend.friend_iduser = %s and friend.friend_idgroup = friend_group.idgroup' % request.session['user_now']
    r = search(conn, sql)
    gelements = ['id', 'name', 'mail', 'groupname', 'sex', 'birthday']
    for e in r:
        if e[3] not in group:
            group[e[3]] = [dict(zip(gelements, e))]
        else:
            group[e[3]].append(dict(zip(gelements, e)))
    sql = 'select '
    conn.close()
    info = {'friend': friend, 'friend_group': group}
    return render(request, 'friend.html', info)


def message(request):
    sql = 'select name, mail, idmessage_reply, message_iduser, message_content, message_to_who, message_time from user, message_reply where \
    message_to_who = %s and message_iduser = user.iduser' % request.session['user_now']
    print(sql)
    conn = connect_mysql()
    r = search(conn, sql)
    melements = ['name', 'mal', 'idmessage_reply', 'message_iduser',
                 'message_content', 'message_to_who', 'message_time']
    msgs = []
    for e in r:
        msgs.append(dict(zip(melements, e)))
    info = {'msgs': msgs}
    return render(request, 'message.html', info)


def user_update(request):
    sql = "update user set name='%s', sex='%s', birthday=%s, addr='%s', passwd='%s', mail='%s' where iduser = %s" % (
        request.POST['name'], request.POST['sex'], request.POST['birthday'], request.POST['addr'],
        request.POST['passwd'], request.POST['mail'], request.session['user_now']
    )
    conn = connect_mysql()
    r = other_action(conn, sql)
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')


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
    info = {'List': List}
    if len(List) == 0:
        return render(request, 'error.html')
    else:
        return render(request, 'friend_result.html', info)


def add_friend(request):
    friend = request.GET['friend']
    conn = connect_mysql()
    sql = 'insert into friend (friend_iduser, friend) values( %s, %s)' % (
        request.session['user_now'], friend)
    r = other_action(conn, sql)
    conn.close()
    if r != 1:
        return render(request, 'error.html')
    else:
        return render(request, 'successful.html')


def delete_friend(request):
    friend = request.GET['friend']
    sql = 'delete from friend where friend_iduser= %s and friend=%s' % (
        request.session['user_now'], friend)
    conn = connect_mysql()
    r = other_action(conn, sql)
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')


def friend_info(request):
    '''
    get friend info from GET and show it on the page
    '''
    pinfo = {
        'name': request.GET['name'],
        'iduser': request.GET['iduser'],
        'mail': request.GET['mail'],
        'sex': request.GET['sex'],
        'birthday': request.GET['birthday']
    }
    sql = 'select idgroup, groupname from friend_group where friend_group.iduser=%s' % request.session[
        'user_now']
    conn = connect_mysql()
    r = search(conn, sql)
    List = []
    elements = ['id', 'group']
    for e in r:
        List.append(dict(zip(elements, e)))
    sql = 'select groupname from friend, friend_group where friend.friend_idgroup = \
     friend_group.idgroup and friend.friend_iduser = %s and friend.friend = %s' % (
        request.session['user_now'], request.GET['iduser'])
    r = search(conn, sql)
    if len(r) > 0 and len(r[0]) > 0:
        r = r[0][0]
    else:
        r = None
    info = {'List': List, 'info': pinfo, 'last_group': r}
    conn.close()
    return render(request, 'friend_info.html', info)


def add_group(request):
    group = request.GET['group_name']
    sql = 'insert into friend_group (groupname, iduser) values("%s", %s)' % (
        group, request.session['user_now'])
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
    sql = 'update friend set friend_idgroup=%s where friend_iduser=%s and friend=%s' % (
        id, user_now, friend)
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


def publish_diary(request):
    localtime = time.localtime(time.time())
    dtime = time.strftime("%Y-%m-%d %H:%M", localtime)
    title = request.POST['title']
    content = request.POST['content']
    sql = 'insert into diary(diary_name, diary_touch, diary_iduser, diary_content) values("%s", "%s", %s, "%s")' % (
        title, dtime, request.session['user_now'], content
    )
    conn = connect_mysql()
    r = other_action(conn, sql)
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')


def edit_diary():
    pass


def delete_diary(request):
    id = request.GET['id']
    print(id)
    sql = 'delete from diary where iddiary=%s' % id
    conn = connect_mysql()
    r = other_action(conn, sql)
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')

# 视图


def reply_diary(request):
    id = request.GET['id']
    sql = 'select DISTINCT iddiary, diary_name, diary_touch, diary_iduser, diary_content, iduser, name  from diary_view where iddiary = %s' % id
    conn = connect_mysql()
    r = search(conn, sql)
    delement = ['iddiary', 'diary_name', 'diary_touch',
                'diary_iduser', 'diary_content', 'iduser', 'name']
    info = {'diary': dict(zip(delement, r[0]))}
    sql = 'select * from diary_reply_view where reply_diary=%s' % id
    r = search(conn, sql)
    relement = ['content', 'time', 'name']
    reply = []
    for e in r:
        reply.append(dict(zip(relement, e)))
    conn.close()
    info['replys'] = reply
    return render(request, 'diary_reply.html', info)


def diary_reply(request):
    id = request.POST['id']
    content = request.POST['content']
    localtime = time.localtime(time.time())
    ftime = time.strftime("%Y-%m-%d %H:%M", localtime)
    sql = 'insert into diary_reply (reply_diary, reply_content, reply_time, reply_user) values(%s, "%s", "%s", %s)' % (
        id, content, ftime, request.session['user_now']
    )
    conn = connect_mysql()
    r = other_action(conn, sql)
    conn.close()
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')


def send_message(request):
    msg = request.POST['msg']
    to_who = request.POST['to_who']
    localtime = time.localtime(time.time())
    ftime = time.strftime("%Y-%m-%d %H:%M", localtime)

    sql = 'insert into message_reply(message_iduser, message_content, message_to_who, message_time) values (%s, "%s", %s,"%s")' % (
        request.session['user_now'], msg, to_who, ftime
    )
    print(sql)
    conn = connect_mysql()
    r = other_action(conn, sql)
    if r == 1:
        return render(request, 'successful.html')
    else:
        return render(request, 'error.html')


def cal(request):
    # 分组查询
    sql = 'select name, count(*) as times \
    from friend, user \
    where user.iduser = friend.friend_iduser \
    group by friend_iduser'
    conn = connect_mysql()
    r = search(conn, sql)
    celements = ['name', 'times']
    List = []
    for e in r:
        List.append(dict(zip(celements, e)))
    info = { 'List': List}
    return render(request, 'cal.html', info)
