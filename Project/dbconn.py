import sqlite3
import os
from shutil import rmtree
class Character():
    def __init__(self,id,name,link,exists=True):
        self.id=id
        self.name=name
        self.link=link
        self.exists=exists
class Group():
    def __init__(self,id,name,link,exists=True):
        self.id=id
        self.name=name
        self.link=link
        self.exists=exists
class Dbconn():
    def __init__(self,filename):
        self.conn= sqlite3.connect(filename)
        self.execute('CREATE table if not exists characters (cid integer PRIMARY key AUTOINCREMENT, cname text NOT NULL, link text NOT NULL);')
        self.execute( 'CREATE table if not exists groups (gid integer PRIMARY KEY autoincrement, gname text NOT NULL, link text NOT NULL);')
        self.execute('''CREATE table if not exists cgrelations (characterid integer , groupid integer ,
        FOREIGN KEY (characterid) REFERENCES characters(cid),FOREIGN KEY (groupid) REFERENCES groups(gid));''')
        self.execute( 'CREATE table if not exists media (did integer primary key autoincrement,dname text not null);')
    def close(self):
        self.conn.close()

    def execute(self,query): #execute query and return the query
        try:
            cur = self.conn.execute(query)
            self.conn.commit()
            return list(cur)
        except BaseException as e:
            print('error!: %s'%(str(e)))
            return []
    def notexistexecute(self, query,
                        cquery) -> bool :  # will execute the query if the search query cquery is empty (Output is whatever it was made)
        try:
            cur = self.conn.cursor()
            cur.execute(cquery)
            r = cur.fetchone()
            if r == None:
                self.conn.execute(query)
                self.conn.commit()
                return True
            return False
        except BaseException as e:
            print('error!: %s' % (str(e)))
            return False
    #general search
    def findcharacterbyname(self, name):
        list = self.execute("select cid,link from characters where cname='" + str(name) + "';")

        if (len(list) == 0):
            return Character(-1,name,"",False)
        return Character(list[0][0],name,list[0][1])
    def findcharacterbycid(self, cid):
        list = self.execute("select cname,link from characters where cid=" + str(cid) + ";")
        if (len(list) == 0):
            return Character(cid,"","",False)
        return Character( cid, list[0][0],list[0][1])
    def findcharacterbylink(self,link:str):
        list = self.execute("select cid,cname from characters where link='" + link + "';")
        if (len(list) == 0):
            return Character(-1, "", link, False)
        return Character(list[0][0], list[0][1], link)
    def findgroupbyname(self,name):
        list = self.execute("select gid,link from groups where gname='" + str(name) + "';")
        if (len(list) == 0):
            return Group(-1, name, "", False)
        return Group(list[0][0], name, list[0][1])
    def findgroupbygid(self,gid):
        list = self.execute("select gname,link from groups where gid='" + str(gid) + "';")
        if (len(list) == 0):
            return Group(gid, "","",False)
        return Group(gid,list[0][0],list[0][1])
    def findgroupbylink(self,link):
        list = self.execute("select gid,gname from groups where link='" + link + "';")
        if (len(list) == 0):
            return Group(-1, "",link,False)
        return Group(list[0][0],list[0][1],link)
    #character
    def insertcharacter(self, name, filestr):
        c = self.findcharacterbyname(name)
        if (c.exists):
            print("Error:Character already exists.")
            return False
        link=name.replace(" ","_")
        status = self.notexistexecute("INSERT INTO characters (cname,link) values ('" + name + "','"+link+"');",
                                 "select cname from characters where cname='" + name + "';")
        cur_dir = os.path.dirname(__file__)
        rel_path = "CharacterData\\" + name
        abs_file_path = os.path.join(cur_dir, rel_path)
        try:
            os.mkdir(abs_file_path)
        except:
            print("mkdir error")
        abs_file_path = os.path.join(cur_dir, "CharacterData\\" + name + "\\Data.txt")
        print(abs_file_path)
        with open(abs_file_path, 'w') as file:
            file.write(filestr)
        return status
    def getcharacterdata(self, name):
        c = self.findcharacterbyname(name)
        if (c.exists):
            cur_dir = os.path.dirname(__file__)
            abs_file_path = os.path.join(cur_dir, "CharacterData\\" + name + "\\Data.txt")
            data = ""
            with open(abs_file_path, 'r') as file:
                data = file.read()
            return data
        else:
            return ("[Character isnt in the database]")
    def setcharacterdata(self, name, filestr)->bool:
        c = self.findcharacterbyname(name)
        print(filestr)
        if (c.exists):
            cur_dir = os.path.dirname(__file__)
            abs_file_path = os.path.join(cur_dir, "CharacterData\\" + name + "\\Data.txt")
            with open(abs_file_path, 'w') as file:
                file.write(filestr.replace("\n"," "))
            return True
        else:
            return False
    def removecharacter(self, id) -> bool:
        c = self.findcharacterbycid(id)
        if (c.id):
            #erase cgrelations
            print("[Deleting character]")
            self.execute("Delete from characters where cid=" + str(c.id) + ";")
            self.execute("Delete from cgrealtions where characterid=" + str(c.id) + ";")
            cur_dir = os.path.dirname(__file__)
            rmtree(os.path.join(cur_dir, "CharacterData\\" + c.name))
            return True
        else:
            print("[Tried to remove non-exisitng character]")
            return False
    #cg Table
    def cgexists(self,cid,gid):
        query="select (characterid) from cgrelations where characterid=" + str(cid) + " And groupid=" + str(gid) + ";"
        cur = self.conn.cursor()
        cur.execute(query)
        r = cur.fetchone()
        print (r)
        return r != None
    def addcgrelation(self,cid,gid):
        return self.notexistexecute("insert into cgrelations (characterid,groupid) values("+str(cid)+","+str(gid)+");","select * from cgrelations where characterid="+str(cid)+" And groupid="+str(gid)+";")
    def getcharactercgrelation(self,cid):
        query="SELECT groups.gid,groups.gname,groups.link from cgrelations INNER JOIN groups ON groups.gid=cgrelations.groupid and cgrelations.characterid = "+str(cid)+";"
        data = self.execute(query)
        return data
    def getgroupcgrelation(self, gid):
        query = "SELECT characters.cid,characters.cname,characters.link from cgrelations INNER JOIN characters ON characters.cid=cgrelations.characterid and cgrelations.groupid = " + str(
            gid) + ";"
        data = self.execute(query)
        return data
    def removecgrelation (self, cid,gid):
        return self.notexistexecute(
            "Delete cgrelations (characterid,groupid) values(" + str(cid) + "," + str(gid) + ");",
            "select (cid) from cgrelations where characterid=" + str(cid) + " And groupid=" + str(gid) + ";")
    #Group
    def insertgroup(self,gname,filestr):
        g = self.findgroupbyname(gname)
        if (g.exists):
            print("[AddGroup failed Group already exists.]")
            return False
        link=g.name.replace(" ","_")
        status = self.notexistexecute("INSERT INTO groups (gname,link) values ('" + gname + "','"+link+"');",
                                      "select * from groups where gname ='" + gname + "';")
        cur_dir = os.path.dirname(__file__)
        rel_path = "GroupData\\" + gname
        abs_file_path = os.path.join(cur_dir, rel_path)
        try:
            os.mkdir(abs_file_path)
        except:
            print("mkdir error")
        abs_file_path = os.path.join(cur_dir, "GroupData\\" + gname + "\\Data.txt")
        with open(abs_file_path, 'w') as file:
            file.write(filestr)
        return status
    def removegroup(self,id) -> bool:
        g = self.findgroupbygid(id)
        if (g.exists):
            self.execute("Delete from groups where gid=" + str(g.id) + ";")
            self.execute("Delete from cgrealtions where groupid=" + str(g.id) + ";")
            cur_dir = os.path.dirname(__file__)
            rmtree(os.path.join(cur_dir, "GroupData\\" + g.name))
            return True
        else:
            print("Error:Tried to remove non-existing group")
            return False
    def getgroupdata(self, name):
        g = self.findgroupbyname(name)
        if (g.exists):
            cur_dir = os.path.dirname(__file__)
            abs_file_path = os.path.join(cur_dir, "GroupData\\" + name + "\\Data.txt")
            data = ""
            with open(abs_file_path, 'r') as file:
                data = file.read()
            return data
        else:
            return ("[Group isnt in the database]")
    def setgroupdata(self,name,filestr):
        g = self.findgroupbyname(name)
        if (g.exists):
            cur_dir = os.path.dirname(__file__)
            abs_file_path = os.path.join(cur_dir, "GroupData\\" + name + "\\Data.txt")
            with open(abs_file_path, 'w') as file:
                file.write(filestr.replace("\n"," "))
            return True
        else:
            return False