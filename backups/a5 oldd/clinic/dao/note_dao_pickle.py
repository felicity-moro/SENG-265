from pickle import loads, load, dumps, dump
from clinic.dao.note_dao import NoteDAO
import datetime
from clinic.note import Note
import os

class NoteDAOPickle(NoteDAO):
    def __init__(self,phn,autosave = False):
        ''' Construct a NoteDAOPickle class '''
        self.phn = phn
        self.autosave = autosave
        self.notes = {}
        self.counter = 0
        self.filename = "clinic/records/"+str(self.phn)+".dat"

        if autosave:
            self.load_notes()
            self.counter = len(self.notes)

    def load_notes(self):
        check_file = os.path.isfile(self.filename)
        if check_file is False:
            return

        with open(self.filename,'rb') as file:

            notes = load(file,fix_imports=True, encoding='ASCII', errors='strict', buffers=None)
            self.notes = notes

        file.close()
        
    def save_notes(self):
        
        file = open(self.filename,'wb')
        
        dump(self.notes,file,protocol=None, fix_imports=True, buffer_callback=None)
        file.close()
      

    def search_note(self, code):
        ''' Returns the note corrisponding to its code '''
        return self.notes.get(code)
    
    def create_note(self, text):
        ''' Creates a new note'''
        self.counter += 1 
        new_note = Note(self.counter,text) # assigns the note data
        self.notes[self.counter] = new_note # adds to list of notes

        self.save_notes()

        return new_note
    
    def retrieve_notes(self, search_string):
        ''' retrieve existing notes that include the search string '''
        retrieved_notes = []
        for note in self.notes: # looks through all notes and checks if each one contains 
            if search_string in self.notes[note].text:
                retrieved_notes.append(self.notes[note])
        return retrieved_notes
    
    def update_note(self, code, new_text):
        ''' Updates a note via its code to contain new text'''

        to_edit = self.notes.get(code)

        if to_edit:
            to_edit.text = new_text
            to_edit.timestamp = datetime.datetime.now() # updates last time it was updated 
            self.save_notes()
            return True

        return False
        
    def delete_note(self, code):
        ''' removes the note by its code if it exists '''
        
        if self.notes.get(code):
            self.notes.pop(code)
            self.save_notes()
            return True
        else:
            return False
        
    def list_notes(self):
        ''' list all notes '''
        notes_list = []
        
        if self.counter > 0:
            for code in range (self.counter,0,-1): # returns notes in reverse order 
                if self.notes.get(code):
                    notes_list.append(self.notes[code])

        return notes_list
