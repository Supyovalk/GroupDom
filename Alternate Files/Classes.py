class db: #connector to database
    def __init__(self,db_name):
        pass
        #connect to db and save connection
class hlink:
    def __init__(self,name,link):
        this.name=name
        this.link=link
class databox:
    def tohtml(self):
        pass
class groupbox(databox):
    def __init__(self,name,id):
        this.name=name
        this.id=id
        #this.connections=[hlink1,hlink2].....