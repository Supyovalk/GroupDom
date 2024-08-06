class CharacterSheet:
    def __init__(self, name ,medias,groups,picture=None):
        self.name=name
        self.medias=medias
        self.groups=groups
        self.picture=picture
class ChatacterPage: #used to represent a character page
    #id,Chatactersheet,HtmlPage,comments
    def __init__(self, comments):
        self.comments=comments
    def show(self): #show the page
        return None #unimplemented

