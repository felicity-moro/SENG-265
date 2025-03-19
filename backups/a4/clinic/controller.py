from patient import Patient
from patient_record import PatientRecord
from note import Note
from exception.invalid_login_exception import InvalidLoginException
from exception.duplicate_login_exception import DuplicateLoginException
from exception.invalid_logout_exception import InvalidLogoutException
from exception.illegal_access_exception import IllegalAccessException
from exception.illegal_operation_exception import IllegalOperationException
from exception.no_current_patient_exception import NoCurrentPatientException
import hashlib
from dao.patient_dao_json import PatientDAOJSON

class Controller():
	''' controller class that receives the system's operations '''

	def __init__(self, autosave = False):
		''' construct a controller class '''
		self.users = self.get_users()

		self.username = None
		self.password = None
		self.logged = False
		self.autosave = autosave
		self.patients = {}
		self.current_patient = None
		self.patientDAO = PatientDAOJSON(self.patients)

	def get_password_hash(self,password:str):
        # Learn a bit about password hashes by reading this code
		encoded_password = password.encode('utf-8')     # Convert the password to bytes
		hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
		hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
		return hex_dig

	def get_users(self):
		filer = open("users.txt","r")
		user_dict = {}
		for info in filer:
			line = info.strip()
			line = line.split(",")
			user_dict[line[0]] = line[1]
		
		return user_dict
	
	def login(self, username, password):
		if self.logged:
			raise DuplicateLoginException
		
		key = self.users.get(username)
		if key:
			if key == self.get_password_hash(password):
				self.logged = True
				return True
			else:
				raise InvalidLoginException
		else:
			raise InvalidLoginException

	def logout(self):
		''' user logs out from the system '''
		if not self.logged:
			raise InvalidLogoutException
        
		else:
			self.logged = False
			self.current_patient = None
			return True

	def search_patient(self, phn):
		''' user searches a patient '''
		# must be logged in to do operation
		if not self.logged:
			return None

		return self.patients.get(phn)

	def create_patient(self, phn, name, birth_date, phone, email, address):
		''' user creates a patient '''
		# must be logged in to do operation
		if not self.logged:
			return None

		# patient already exists, do not create them
		if self.patients.get(phn):
			return None

		# finally, create a new patient
		patient = Patient(phn, name, birth_date, phone, email, address)
		self.patients[phn] = patient
		return patient

	def retrieve_patients(self, name):
		''' user retrieves the patients that satisfy a search criterion '''
		# must be logged in to do operation
		if not self.logged:
			return None

		retrieved_patients = []
		for patient in self.patients.values():
			if name in patient.name:
				retrieved_patients.append(patient)
		return retrieved_patients

	def update_patient(self, original_phn, phn, name, birth_date, phone, email, address):
		''' user updates a patient '''
		# must be logged in to do operation
		if not self.logged:
			return False

		# first, search the patient by key
		patient = self.patients.get(original_phn)

		# patient does not exist, cannot update
		if not patient:
			return False

		# patient is current patient, cannot update
		if self.current_patient:
			if patient == self.current_patient:
				return False

		# patient exists, update fields
		patient.name = name
		patient.birth_date = birth_date
		patient.phone = phone
		patient.email = email
		patient.address = address

		# treat different keys as a separate case
		if original_phn != phn:
			if self.patients.get(phn):
				return False
			self.patients.pop(original_phn)
			patient.phn = phn
			self.patients[phn] = patient

		return True
			
	def delete_patient(self, phn):
		''' user deletes a patient '''
		# must be logged in to do operation
		if not self.logged:
			return False

		# first, search the patient by key
		patient = self.patients.get(phn)

		# patient does not exist, cannot delete
		if not patient:
			return False

		# patient is current patient, cannot delete
		if self.current_patient:
			if patient == self.current_patient:
				return False

		# patient exists, delete patient
		self.patients.pop(phn)
		return True

	def list_patients(self):
		''' user lists all patients '''
		# must be logged in to do operation
		if not self.logged:
			return None

		patients_list = []
		for patient in self.patients.values():
			patients_list.append(patient)
		return patients_list

	def set_current_patient(self, phn):
		''' user sets the current patient '''

		# must be logged in to do operation
		if not self.logged:
			return False

		# first, search the patient by key
		patient = self.patients.get(phn)

		# patient does not exist
		if not patient:
			return False

		# patient exists, set them to be the current patient
		self.current_patient = patient


	def get_current_patient(self):
		''' get the current patient '''
		# must be logged in to do operation
		if not self.logged:
			return None

		# return current patient
		return self.current_patient

	def unset_current_patient(self):
		''' unset the current patient '''

		# must be logged in to do operation
		if not self.logged:
			return None

		# unset current patient
		self.current_patient = None


	def search_note(self, code):
		''' user searches a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			return None

		# there must be a valid current patient
		if not self.current_patient:
			return None

		# search a new note with the given code and return it 
		return self.current_patient.search_note(code)

	def create_note(self, text):
		''' user creates a note in the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			return None

		# there must be a valid current patient
		if not self.current_patient:
			return None

		# create a new note and return it
		return self.current_patient.create_note(text)

	def retrieve_notes(self, search_string):
		''' user retrieves the notes from the current patient's record
			that satisfy a search string '''
		# must be logged in to do operation
		if not self.logged:
			return None

		# there must be a valid current patient
		if not self.current_patient:
			return None

		# return the found notes
		return self.current_patient.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' user updates a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			return None

		# there must be a valid current patient
		if not self.current_patient:
			return None

		# update note
		return self.current_patient.update_note(code, new_text)

	def delete_note(self, code):
		''' user deletes a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			return None

		# there must be a valid current patient
		if not self.current_patient:
			return None

		# delete note
		return self.current_patient.delete_note(code)

	def list_notes(self):
		''' user lists all notes from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			return None

		# there must be a valid current patient
		if not self.current_patient:
			return None

		return self.current_patient.list_notes()
