from note import Note
import datetime

class PatientRecord():
    
    def __init__(self):
        self.autocounter = 0
        self.actualamm = 0
        self.record = {}

    def __eq__(self, other)-> bool:
        return (self.autocounter == other.autocounter) and (self.record == other.record) and (self.actualamm == other.actualamm)
    
    def create_note(self,text:str) -> Note:
        self.autocounter += 1
        self.actualamm += 1
        
        new_note = Note(self.autocounter,text)
        self.record[self.autocounter] = new_note
        return new_note
    
    def return_note(self, code:int) -> Note:
        return self.record.get(code)
    
    def in_text(self, search_str:str) -> list[Note]:

        notes = []
        
        for note in list(self.record.values()):
            if note.in_text(search_str):
                notes.append(note)
        
        return notes
    
    def code_in_sys(self, code:int) -> bool:
        return code in self.record
    
    def delete_code(self, code:int, update: bool)-> bool:
        a = 14
        
    def update_note(self, code:int, new_text:str) -> bool:
        if self.actualamm == 0 or not self.code_in_sys(code):
            return False
        
        return self.record[code].update(new_text)
    
    def delete_note(self, code:int) -> bool:
        if self.actualamm == 0 or not self.code_in_sys(code):
            return False
        
        self.record.pop(code)
        self.actualamm -= 1
        return True
    
    def list_notes(self) -> list[Note]:
        if self.actualamm == 0:
            return []
        
        records = []

        for code in range(self.autocounter, 0, -1):
            note = self.record.get(code)
            if note:
                records.append(note)

        return records

