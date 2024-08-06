import sqlite3
def notexistexecute(conn,query,cquery): #will execute the query if the search query cquery is empty
    try:
        cur = conn.cursor()
        cur.execute(cquery)
        r = cur.fetchone()
        print(r)
        if r==None:
            conn.execute(query)
            conn.commit()
    except BaseException as e:
        print('error!: %s'%(str(e)))
        return []

def execute(conn,query):
    try:
        cur = conn.execute(query)
        conn.commit()
        return list(cur)
    except BaseException as e:
        print('error!: %s'%(str(e)))
        return []


conn = sqlite3.connect('DB')
def initdb():
    execute(conn,'CREATE table if not exists characters (cid integer PRIMARY key AUTOINCREMENT, cname text NOT NULL);')
    execute(conn,'CREATE table if not exists groups (gid integer PRIMARY KEY autoincrement, gname text NOT NULL);')
    execute(conn,'CREATE table if not exists cgrelations (characterid integer , groupid integer ,FOREIGN KEY (characterid) REFERENCES characters(cid),FOREIGN KEY (groupid) REFERENCES groups(gid));')
    execute(conn,'CREATE table if not exists media (did integer primary key autoincrement,dname text not null);')
def insertcharacter(conn,name):
    notexistexecute(conn,"INSERT INTO characters (cname) values ('"+name+"');","select cname from characters where cname='"+name+"';")
def selectall(conn,table):
    return execute(conn,"select * from "+table+";")
def selectbyvalue(conn,table,var,value,isstr):
    if isstr:
        subquery=var+ "='" +value+ "';"
    else:
        subquery = var + "=" + value + ";"
    query="select * from " + table + " where " + subquery
    print(query)
    return execute(conn,query)
def removebyvalue(conn,table,var,value,isstr):
    if isstr:
        subquery=var+ "='" +value+ "';"
    else:
        subquery = var + "=" + value + ";"
    query="Delete from "+table+" where "+subquery
    execute(conn, query)
removebyvalue(conn,'characters','cname','Shani',True)
print(selectall(conn,'characters'))
