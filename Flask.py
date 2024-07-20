from flask import Flask, render_template,request,redirect,url_for
import GroupTemps
import dbconn

app =Flask(__name__)
@app.route("/")
def index():
    return render_template('Home.html')
@app.route("/character/")
def charactermainpage():
    conn = dbconn.Dbconn('DB.sqlite3')
    return GroupTemps.CreateTemplateCharacterHome(conn)
@app.route("/character/<string:link>",methods=['GET','DELETE'])
def characterpage(link):
    conn = dbconn.Dbconn('DB.sqlite3')
    c = conn.findcharacterbylink(link)
    print(request.method)
    if request.method=='GET':
        if not c.exists:
            return render_template('ErrorMissingCharacter.html',link=link)
        data=conn.getcharacterdata(c.name)
        return render_template('Characterpage.html',data=data,link=link,name=c.name )
@app.route("/special/deletecharacter/<string:link>",methods=['GET','POST'])
def removecharacter(link):
    conn = dbconn.Dbconn('DB.sqlite3')
    c = conn.findcharacterbylink(link)
    if c.exists:
        if(request.method=='GET'):
            return render_template('CharacterRemove.html',name=c.name,link=link)
        elif request.method=='POST':
                conn.removecharacter(c.id)
                return redirect('/character/')
    else:
        return render_template('ErrorMissingCharacter.html', link=link)
@app.route("/character/<string:link>/edit",methods=['GET','POST'])
def editcharacter(link):
    #XSS script bretch - needs fixing and telling in the program sumaary
    conn = dbconn.Dbconn('DB.sqlite3')
    c = conn.findcharacterbylink(link)
    if c.exists:
        if (request.method == 'GET'):
            data = conn.getcharacterdata(c.name)
            return render_template('CharacterEdit.html', name=c.name, data=data,link=link)
        if (request.method == 'POST'):
            conn = dbconn.Dbconn('DB.sqlite3')
            data = request.form["data"]
            print(data)
            #xss prevention
            if('<script>' in data or '</script>' in data):
                return render_template('ErrorXSS.html',link=link)
            try:
                conn.setcharacterdata(c.name, data)
            except:
                 print("Error!")
            print('Echaracter Post1')
            return redirect("/character/" + c.link)
    else:
        return render_template('ErrorMissingCharacter.html', link=link)
@app.route("/character/<string:link>/relations")
def characterlinks(link):
    conn=dbconn.Dbconn('DB.sqlite3')
    c=conn.findcharacterbylink(link)
    data=conn.getcharactercgrelation(c.id)
    print(data)
    return render_template('CharacterRelations.html',groups=data,name=c.name)
@app.route("/group/<string:link>/relations")
def grouplinks(link):
    conn=dbconn.Dbconn('DB.sqlite3')
    g=conn.findgroupbylink(link)
    data=conn.getgroupcgrelation(g.id)
    print(data)
    return render_template('GroupRelations.html',characters=data,name=g.name)
@app.route("/group/")
def groupmainpage():
    conn = dbconn.Dbconn('DB.sqlite3')
    rowdata = conn.conn.execute("Select * from groups order by random() limit 10;").fetchall()
    print(rowdata)
    conn.close()
    return render_template('GroupHome.html', posts=rowdata)
@app.route("/group/<string:link>")
def grouppage(link):
    conn = dbconn.Dbconn('DB.sqlite3')
    g = conn.findgroupbylink(link)
    if not (g.exists):
        return render_template('ErrorMissingGroup.html', link=link)
    data = conn.getgroupdata(g.name)
    return render_template('Grouppage.html', data=data, name=g.name,link=link)
@app.route("/addcharacter",methods=['GET','POST'])
def addcharacter():
    if request.method=='GET':
        return render_template('CharacterAdd.html')
    elif request.method=='POST':
        conn = dbconn.Dbconn('DB.sqlite3')
        data = request.form["data"]
        name = request.form["name"]
        c = conn.findcharacterbyname(name)
        if not c.exists:
            conn.insertcharacter(name, data)
            data = conn.getcharacterdata(name)
            return redirect('/character/' + c.link)
        else:
            return render_template('ErrorExistingCharacter.html', name=name)
@app.route("/addgroup",methods=['GET','POST'])
def addgroup():
    if request.method == 'GET':
        return render_template('GroupAdd.html')
    elif request.method=='POST':
        conn = dbconn.Dbconn('DB.sqlite3')
        data,name = request.form["data"], request.form["name"]
        g = conn.findgroupbyname(name)
        if not g.exists:
            conn.insertgroup(name, data)
            data = conn.getgroupdata(name)
            return redirect('/group/' + g.link)
        return render_template('ErrorExistingGroup.html', name=name)
    return "ERROR!"
@app.route("/group/<string:link>/edit",methods=['GET','POST'])
def editgroup(link):
    # XSS script bretch - needs fixing and telling in the program sumaary
    conn = dbconn.Dbconn('DB.sqlite3')
    g = conn.findgroupbylink(link)
    if g.exists:
        if (request.method == 'GET'):
            data = conn.getgroupdata(g.name)
            return render_template('GroupEdit.html', name=g.name, data=data, link=link)
        if (request.method == 'POST'):
            conn = dbconn.Dbconn('DB.sqlite3')
            data = request.form["data"]
            print("EditGroupData:"+data)
            # xss prevention
            if ('<script>' in data or '</script>' in data):
                return render_template('ErrorXSS.html', link=link)
            try:
                conn.setgroupdata(g.name, data)
            except:
                print("Error!")
            print('Echaracter Post1')
            return redirect("/group/" + g.link)
    else:
        return render_template('ErrorMissingGroup.html', link=link)
@app.route("/special/deletegroup/<string:link>",methods=['GET','POST'])
def removegroup(link):
    conn = dbconn.Dbconn('DB.sqlite3')
    g = conn.findgroupbylink(link)
    if g.exists:
        if (request.method == 'GET'):
            return render_template('GroupRemove.html', name=g.name, link=link)
        elif request.method == 'POST':
            conn.removegroup(g.id)
            return redirect('/group/')
    else:
        return render_template('ErrorMissingCharacter.html', link=link)
@app.route("/special/relationadd",methods=["GET","POST"])
def addcgrelation():
    if (request.method == 'GET'):
        return render_template('CGRelationAdd.html')
    elif request.method == 'POST':
        conn=dbconn.Dbconn('DB.sqlite3')
        character,group=request.form["Character"],request.form["Group"]
        print(character,group)
        c,g=conn.findcharacterbyname(character),conn.findgroupbyname(group)
        print(c,g)
        if not c.exists:
            return render_template('ErrorMissingCharacter.html',link=character.replace(" ","_"))
        if not g.exists:
            return render_template('ErrorMissingGroup.html',link=group.replace(" ","_"))
        if conn.cgexists(c.id,g.id):
            return "CGRELATION EXISTS"
        conn.addcgrelation(c.id,g.id)
        return redirect("/")
@app.route("/search/",methods=["GET","POST"])
def searchpageroot():
     conn=dbconn.Dbconn('DB.sqlite3')
     name=request.form["InputSearch"]
     print(name)
     link=name.replace(" ","_")
     return redirect("/search/"+link)
@app.route("/search/<string:link>")
def searchpage(link):
    name = link.replace("_", " ")
    conn = dbconn.Dbconn('DB.sqlite3')
    cdata = conn.execute('select * from characters where cname like "' + name + '%" COLLATE NOCASE;')
    gdata = conn.execute('select * from groups where gname like "' + name + '%" COLLATE NOCASE;')
    print(cdata)
    print(gdata)
    return render_template("SearchPage.html",cdata=cdata,gdata=gdata)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)