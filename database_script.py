import sqlite3

def dosomething(command):
    connection = sqlite3.connect("cryptx_db.db")
    cur = connection.cursor()
    # cur.execute(command)
    # connection.commit()
    connection.close()

def view_userinfo():
    connection = sqlite3.connect("cryptx_db.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM userinfo")
    rows = cur.fetchall()
    connection.close()
    return rows