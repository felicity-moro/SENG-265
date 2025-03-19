from patient import Patient
from patient_record import PatientRecord
from note import Note

class Controller():
    
    def __init__(self):
        self.__logged_in = False
        self.__user_library = {"user": "clinic2024"}
        self.__patients = {}
        self.__all_notes = {}
        self.__cur_patient = None        

    def login(self, username:str, password:str) -> bool:
        if self.__logged_in:
            return False
        
        key = self.__user_library.get(username)
        if key:
            if key is password:
                self.__logged_in = True
                return True
            else:
                return False
        else:
            return False
        
    def logout(self) -> bool:
        if not self.__logged_in:
            return False
        
        else:
            self.__logged_in = False
            self.__cur_patient = None
            return True
        
    def create_patient(self, PHN:int, name:str, bday:str, phone_num:str, email:str, address:str) -> Patient:
        if not self.__logged_in:
            return None
        
        if not self.PHN_in_sys(PHN):
            new_patient = Patient(PHN,name,bday,phone_num,email,address)
            self.__patients[PHN] = new_patient
            return new_patient
        else:
            return None
         
    def search_patient(self, PHN:int) -> Patient:
        if (not self.__logged_in) or (len(self.__patients) == 0):
            return None
        
        return self.__patients.get(PHN)
    
    def retrieve_patients(self, to_find:str) -> list[Patient]:
        if not self.__logged_in:
            return None
        
        list_patients = self.__patients.values()
        retrieved = []

        if len(self.__patients) == 0:
            return retrieved

        for patient in list_patients:
            if to_find in patient.name:
                retrieved.append(patient)
        
        return retrieved

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
            return None
         
        if (self.PHN_in_sys(new_PHN) and (new_PHN is not old_PHN)) or (self.__cur_patient is not None and self.__cur_patient == old_PHN):
            return False

        patient = self.search_patient(old_PHN)
        if patient:
            patient.update_info(new_PHN, name, bday, phone_num, email, address)
            return self.update_patient_dict(old_PHN,patient,True)
        else:
            return False
        
    def delete_patient(self, PHN:int) -> bool:
        if not self.__logged_in:
            return None
        
        if self.__cur_patient is not None and self.__cur_patient == PHN:
            return False
        
        return self.update_patient_dict(PHN,None,False)
    
    def list_patients(self) -> list[Patient]:
        if not self.__logged_in:
            return None
        else:
            patients = list(self.__patients.values())
            return patients

    def set_current_patient(self,PHN:int):
        if not self.__logged_in or not self.PHN_in_sys(PHN):
            return
        
        self.unset_current_patient()
        self.__cur_patient = PHN
    
    def unset_current_patient(self):
        if not self.__logged_in or self.__cur_patient is None:
            return
        
        self.__cur_patient = None

    def get_current_patient(self) -> Patient:
        if not self.__logged_in:
            return
        
        if self.__cur_patient is not None:
            return self.__patients.get(self.__cur_patient)
        else:
            return None
        
    def create_note(self, text:str) -> Note:
        if not self.__logged_in or self.__cur_patient is None :
            return None
        
        return self.__patients[self.__cur_patient].create_note(text)
    
    def search_note(self, code:int) -> Note:
        if not self.__logged_in or self.__cur_patient is None :
            return None
        
        return self.__patients[self.__cur_patient].return_note(code)
    
    def retrieve_notes(self, search_str: str) -> list[Note]:
        if not self.__logged_in or self.__cur_patient is None :
            return None
        
        return self.__patients[self.__cur_patient].in_text(search_str)
    
    def update_note(self, code:int, new_text:str) -> bool:
        if not self.__logged_in:
            return None
        if self.__cur_patient is None:
            return False
        
        return self.__patients[self.__cur_patient].update_note(code, new_text)
    
    def delete_note(self, code:int) -> bool:
        if not self.__logged_in:
            return None
        if self.__cur_patient is None:
            return False
        
        return self.__patients[self.__cur_patient].delete_note(code)
    
    def list_notes(self) -> list[Note]:
        if not self.__logged_in:
            return None
        if self.__cur_patient is None:
            return None
        
        return self.__patients[self.__cur_patient].list_notes()

        