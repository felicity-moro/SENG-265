import datetime

class Note():
    def __init__(self, code:int, text:str):
        self.code = code
        self.text = text
        self.timestamp = datetime.datetime.now()

    def __eq__(self,other) -> bool:
        return (self.code == other.code) and (self.text == other.text)
    
    def __str__(self):
        return f'code : {self.code}, text : "{self.text}"'
    
    def in_text(self, search_str:str) -> bool:
        if search_str in self.text:
            return True
        else:
            return False
        
    def update(self, new_text:str) -> bool:
        self.text = new_text
        self.timestamp = datetime.datetime.now()
        return True