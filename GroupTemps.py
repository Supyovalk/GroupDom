import dbconn
from flask import Flask, render_template,request,redirect,url_for
def CreateTemplateCharacterHome(conn: dbconn.Dbconn):
    rowdata = conn.execute("Select * from characters order by random() limit 10;")
    print(rowdata)
    conn.close()
    return render_template('CharacterHome.html', posts=rowdata)
