'''
   Classe responsavel por classicar os eventos que serão abordados e tradados 
'''


class Event:

    def __init__(self, topic, title, content, keywords):
        self.topic = topic
        self.title = title
        self.content = content
        self.keywords = keywords 


    def hashCode(self):
        pass

    def id(self):
        pass
    
