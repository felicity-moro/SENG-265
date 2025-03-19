from patient_record import PatientRecord
from note import Note

class Patient():

    def __init__(self, PHN: int, name: str, birth_date: str, phone: str, email:str, address: str):
        self.PHN = PHN
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.record = PatientRecord()

    def __eq__(self,other):
        return (self.PHN == other.PHN) and (self.name == other.name) and (self.birth_date == other.birth_date) and (self.email == other.email) and (self.phone == other.phone) and (self.address == other.address) and (self.record == other.record)
    
    def __str__(self):
        return f'patient name {self.name}'
    
    def update_info(self, new_PHN: int, name: str, birth_date: str, phone: str, email:str, address: str):
        self.PHN = new_PHN
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address

    def create_note(self, text:str) -> Note:
        return self.record.create_note(text)
    
    def return_note(self, code)-> Note:
        return self.record.return_note(code)
    
    def in_text(self, search_str:str)-> list[Note]:
        return self.record.in_text(search_str)
    
    def update_note(self, code:int, new_text:str) -> bool:
        return self.record.update_note(code,new_text)
    
    def delete_note(self, code:int) -> bool:
        return self.record.delete_note(code)
    
    def list_notes(self) -> list[Note]:
        return self.record.list_notes()