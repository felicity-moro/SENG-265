import pickle
from clinic.dao.note_dao import NoteDAO
import datetime
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
    def __init__(self, notes, counter):
        self.notes = notes
        self.counter = counter

    def search_note(self, code):
        for note in self.notes:
            if note.code == code:
                return note
        return None
    
    def create_note(self, text):
        self.counter += 1
        new_note = Note(self.counter,text,datetime.datetime.now())
        self.notes[self.counter] = (new_note)
        return new_note
    
    def retrieve_notes(self, search_string):
		# retrieve existing notes
        retrieved_notes = []
        for note in self.notes:
            if search_string in note.text:
                retrieved_notes.append(note)
        return retrieved_notes
    
    def update_note(self, code, new_text):
        updated_note = None

		# first, search the note by code
        for note in self.notes:
            if note.code == code:
                updated_note = note
                break

		# note does not exist
        if not updated_note:
            return False

		# note exists, update fields
        updated_note.text = new_text
        updated_note.timestamp = datetime.datetime.now()
        return True
   
    def delete_note(self, code):
        note_to_delete_index = -1

		# first, search the note by code
        for i in range(len(self.notes)):
            if self.notes[i].code == code:
                note_to_delete_index = i
                break

		# note does not exist
        if note_to_delete_index == -1:
            return False

		# note exists, delete note
        self.notes.pop(note_to_delete_index)
        return True
    
    def list_notes(self):
		# list existing notes
        notes_list = []
        for i in range(-1, -len(self.notes)-1, -1):
            notes_list.append(self.notes[i])
        return notes_list
    