from pickle import dump, load
from clinic.dao.note_dao import NoteDAO
import datetime
from clinic.note import Note
import os

class NoteDAOPickle(NoteDAO):
    def __init__(self,autosave, phn):
        self.phn = phn
        self.notes = {}
        self.counter = 0
        self.autosave = autosave
        

    def load_notes(self):

        check_file = os.path.isfile("clinic/records/"+ "clinic/records/"+str(self.phn)+".dat")

        if check_file == False:
            return

        with open(("clinic/records/"+str(self.phn)+".dat"),'wb') as file:
            notes_list = load(file)
            for note in notes_list:
                self.notes[note.counter] = note
        file.close()

    def save_notes(self):
        with open(("clinic/records/"+str(self.phn)+".dat"),'wb') as file:

            note_lst = []

            for note in self.notes:
                note_lst.append(self.notes[note])

            dump(note_lst,file)
        file.close()

    def search_note(self, code):
        return self.notes.get(code)
    
    def create_note(self, text):
        self.counter += 1
        new_note = Note(self.counter,text)
        self.notes[self.counter] = new_note
        return new_note
    
    def retrieve_notes(self, search_string):
		# retrieve existing notes
        retrieved_notes = []
        for note in self.notes:
            if search_string in self.notes[note].text:
                retrieved_notes.append(self.notes[note])
        return retrieved_notes
    
    def update_note(self, code, new_text):
        to_edit = self.notes.get(code)

        if to_edit:
            to_edit.text = new_text
            to_edit.timestamp = datetime.datetime.now()
            return True
        return False
        
    def delete_note(self, code):
        
        if self.notes.get(code):
            self.notes.pop(code)
            return True
        else:
            return False
        
    def list_notes(self):
		# list existing notes
        notes_list = []
        
        if self.counter > 0:
            for code in range (self.counter,0,-1):
                if self.notes.get(code):
                    notes_list.append(self.notes[code])

        return notes_list
