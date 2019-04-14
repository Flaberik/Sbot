import sqlite3

global connect
global cursor

connect = sqlite3.connect("mdb.db", check_same_thread=False) # или :memory: чтобы сохранить в RAM
cursor = connect.cursor()

def set_token(token):
    try:
        cursor.execute("INSERT INTO bot (token, def) VALUES ('" + token + "', 'False')")
        connect.commit()
    except sqlite3.IntegrityError:
     pass


def upd_info_bot(token, id, first_name, username):
    print()
    print(token)
    print(id)
    print(first_name)
    print(username)

    cursor.execute("UPDATE bot SET id = '" + str(id) + "', first_name = '" + first_name + "', username = '" + username + "' WHERE token ='" + token + "'")
    connect.commit()

def get_bots_():
    cursor.execute("SELECT * FROM bot")
    return cursor.fetchall()

def get_bots():
    cursor.execute("SELECT * FROM bot")
    bots = cursor.fetchall()
    for row in bots:
        print('id: ' + str(row[0]),' first_name: ' + str(row[1]) + ' username: ' + str(row[2]) + ' token: ' + str(row[3]) + ' status: ' + str(row[4]))

def set_status_bot(id, token):
    status = 'True'
    if(str(id) != "-1" and str(token) == "-1"):
        bots = cursor.execute("SELECT * FROM bot WHERE id = '"+str(id)+"'")
        for row in bots:
            if(str(row[4]) == 'False'):
                status = 'True'
            else:
                status = 'False'

        cursor.execute("UPDATE bot SET def = '"+str(status)+"' WHERE id = '"+str(id)+"'")
        connect.commit()
    if(str(token) != "-1" and str(id) == "-1"):
        bots = cursor.execute("SELECT * FROM bot WHERE id = '"+str(token)+"'")
        for row in bots:
            if(str(row[4]) == 'False'):
                status = 'True'
            else:
                status = 'False'

        cursor.execute("UPDATE bot SET def = '"+str(status)+"' WHERE token = '"+str(token)+"'")
        connect.commit()


def update_groups(id_chat, name, type):
    try:
        cursor.execute("INSERT INTO chats (id_chat, name, type) VALUES ('"+str(id_chat)+"', '"+str(name)+"', '"+str(type)+"')")
        connect.commit()
    except sqlite3.IntegrityError:
        pass

def set_message(message):
    cursor.execute("UPDATE messages SET message = '"+str(message)+"'")
    connect.commit()

def get_message():
    return cursor.execute("SELECT * FROM messages")


def set_time(t):
    cursor.execute("INSERT INTO times (time) VALUES ('" + t + "')")
    connect.commit()

def get_times():
    times_ = cursor.execute("SELECT * FROM times")
    for row in times_:
        print('id: ' + str(row[0]) + ' time: ' + str(row[1]))

def get_times_():
    times_ = cursor.execute("SELECT * FROM times")
    ret = []
    for arr in times_:
        ret.append(arr[0])


    return ret

def del_time(id):
    cursor.execute("DELETE FROM times WHERE id = '" + str(id) + "'")
    connect.commit()


def get_groups():
    result = cursor.execute("SELECT * FROM chats")
    ret = []
    for item in result:
        ret.append(item)
    return ret
