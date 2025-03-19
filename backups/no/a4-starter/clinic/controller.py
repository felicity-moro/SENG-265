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
    
    def __init__(self, autosave = False):
        self.__logged_in = False
        self.__user_library = self.get_users()
        self.__patients = {}
        self.__all_notes = {}
        self.__cur_patient = None  
        self.autosave = autosave      
        self.__patient_dao = PatientDAOJSON(self.__patients)

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

    def login(self, username:str, password:str) -> bool:
        if self.__logged_in:
            raise DuplicateLoginException
        
        key = self.__user_library.get(username)
        if key:
            if key == self.get_password_hash(password):
                self.__logged_in = True
                return True
            else:
                raise InvalidLoginException
        else:
            raise InvalidLoginException
        
    def logout(self) -> bool:
        if not self.__logged_in:
            raise InvalidLogoutException
        
        else:
            self.__logged_in = False
            self.__cur_patient = None
            return True
        
    def create_patient(self, PHN:int, name:str, bday:str, phone_num:str, email:str, address:str) -> Patient:
        if not self.__logged_in:
            raise IllegalAccessException
        
        if not self.PHN_in_sys(PHN):
            new_patient = Patient(PHN,name,bday,phone_num,email,address)
            self.__patients[PHN] = new_patient
            return self.__patient_dao.create_patient(new_patient)
        else:
            raise IllegalOperationException
         
    def search_patient(self, PHN:int) -> Patient:
        if (not self.__logged_in):
            raise IllegalAccessException
        if (len(self.__patients) == 0):
            raise IllegalOperationException
        
        return self.__patient_dao.search_patient(PHN)
    
    def retrieve_patients(self, to_find:str) -> list[Patient]:
        if not self.__logged_in:
            raise IllegalAccessException
        
        return self.__patient_dao.retrieve_patients(to_find)

    def update_patient_dict(self, in_sys_PHN: int, new_patient: Patient, update:bool) -> bool: 
        if self.__patients.get(in_sys_PHN):
            self.__patients.pop(in_sys_PHN)
        else:
            return False

        if update:
            self.__patients[new_patient.PHN] = new_patient

        return True

    def PHN_in_sys(self,PHN) -> bool:
        if PHN in self.__patients.keys():
            return True
        else:
            return False

    def update_patient(self, old_PHN:int, new_PHN:int, name:str, bday:str, phone_num:str, email:str, address:str)->bool:  
        if not self.__logged_in:
            raise IllegalAccessException
         
        if (self.PHN_in_sys(new_PHN) and (new_PHN is not old_PHN)) or (self.__cur_patient is not None and self.__cur_patient == old_PHN):
            raise IllegalOperationException

        patient = self.search_patient(old_PHN)
        replacement_patient = Patient(new_PHN,name,bday,phone_num,email,address)
        if patient:
            patient.update_info(new_PHN, name, bday, phone_num, email, address)
            return self.update_patient_dict(old_PHN,patient,True)
        else:
           raise IllegalOperationException
        
    def delete_patient(self, PHN:int) -> bool:
        if not self.__logged_in:
            raise IllegalAccessException

        if self.__cur_patient is not None and self.__cur_patient == PHN:
            raise IllegalOperationException
        
        if self.__patients.get(PHN) is None:
            raise IllegalOperationException
        
        try:
            return self.update_patient_dict(PHN,None,False)
        except IllegalOperationException as exc:
            raise IllegalOperationException
    
    def list_patients(self) -> list[Patient]:
        if not self.__logged_in:
            raise IllegalAccessException
        else:
            patients = list(self.__patients.values())
            return patients

    def set_current_patient(self,PHN:int):
        if not self.__logged_in:
            raise IllegalAccessException
            
        if not self.PHN_in_sys(PHN):
            raise IllegalAccessException
        
        self.unset_current_patient()
        self.__cur_patient = PHN
    
    def unset_current_patient(self):
        if not self.__logged_in:
            raise IllegalAccessException
        if self.__cur_patient is None:
            raise NoCurrentPatientException
        
        self.__cur_patient = None

    def get_current_patient(self) -> Patient:
        if not self.__logged_in:
            raise IllegalAccessException

        
        if self.__cur_patient is not None:
            return self.__patients.get(self.__cur_patient)
        else:
            raise NoCurrentPatientException
        
    def create_note(self, text:str) -> Note:
        if not self.__logged_in:
            raise IllegalAccessException
        
        if self.__cur_patient is None :
            raise NoCurrentPatientException
        
        return self.__patients[self.__cur_patient].create_note(text)
    
    def search_note(self, code:int) -> Note:
        if not self.__logged_in:
            raise IllegalAccessException
        
        if self.__cur_patient is None :
            raise NoCurrentPatientException
        
        return self.__patients[self.__cur_patient].return_note(code)
    
    def retrieve_notes(self, search_str: str) -> list[Note]:
        if not self.__logged_in:
            raise IllegalAccessException
        
        if self.__cur_patient is None :
            raise NoCurrentPatientException
        
        return self.__patients[self.__cur_patient].in_text(search_str)
    
    def update_note(self, code:int, new_text:str) -> bool:
        if not self.__logged_in:
            raise IllegalAccessException
        
        if self.__cur_patient is None :
            raise NoCurrentPatientException
        
        return self.__patients[self.__cur_patient].update_note(code, new_text)
    
    def delete_note(self, code:int) -> bool:
        if not self.__logged_in:
            raise IllegalAccessException
        
        if self.__cur_patient is None :
            raise NoCurrentPatientException
        
        return self.__patients[self.__cur_patient].delete_note(code)
    
    def list_notes(self) -> list[Note]:
        if not self.__logged_in:
            raise IllegalAccessException
        
        if self.__cur_patient is None :
            raise NoCurrentPatientException
        
        return self.__patients[self.__cur_patient].list_notes()

        