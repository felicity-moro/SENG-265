from patient_dao import PatientDAO

class PatientDAOJSON(PatientDAO):
    def __init__(self, patients):
        self.patients = patients 
        
    def search_patient(self, key):
        pass
    
    def create_patient(self, patient):
        pass
    
    def retrieve_patients(self, search_string):
        pass
    
    def update_patient(self, key, patient):
        pass
    
    def delete_patient(self, key):
        pass
    
    def list_patients(self):
        pass