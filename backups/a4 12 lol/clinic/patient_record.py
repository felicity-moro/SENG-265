import datetime
from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle
from pickle import dump, load

class PatientRecord():
	''' class that represents a patient's medical record '''

	def __init__(self,phn,autosave = False):
		''' construct a patient record '''
		self.autosave = autosave
		self.phn = phn
		self.noteDAO = NoteDAOPickle(autosave,self.phn)
		self.notes = {}

	def search_note(self, code):
		''' search a note in the patient's record '''
		return self.noteDAO.search_note(code)

	def create_note(self, text):
		''' create a note in the patient's record '''
		return self.noteDAO.create_note(text)

	def retrieve_notes(self, search_string):
		''' retrieve notes in the patient's record that satisfy a search string '''
		return self.noteDAO.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' update a note from the patient's record '''
		return self.noteDAO.update_note(code, new_text)

	def delete_note(self, code):
		''' delete a note from the patient's record '''
		return self.noteDAO.delete_note(code)

	def list_notes(self):
		''' list all notes from the patient's record from the 
			more recently added to the least recently added'''
		return self.noteDAO.list_notes()
