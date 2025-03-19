from dao.patient_dao import PatientDAO
class PatientDAOJSON(PatientDAO):
    
    def __init__(self, patients:dict):
        self.patients = patients
        
    def search_patient(self, key):
        return self.patients.get(key)
    
    def create_patient(self, patient):
        patient[patient.PHN] = patient
        return patient
    
    def retrieve_patients(self, search_string):
        list_patients = self.__patients.values()
        retrieved = []

        if len(self.__patients) == 0:
            return retrieved

        for patient in list_patients:
            if search_string in patient.name:
                retrieved.append(patient)
        
        return retrieved  
    
    def retrieve_patients(self, search_string):
        return None
    
    def update_patient(self, key, patient):
        return None
   
    def delete_patient(self, key):
        return None
   
    def list_patients(self):
        return None
        
    '''  
    
    def update_patient(self, key, patient):

        patient = self.search_patient(key)
        if patient:
            patient.update_info(new_PHN, name, bday, phone_num, email, address)
            return self.update_patient_dict(old_PHN,patient,True)
        else:
           raise IllegalOperationException
        
    def delete_patient(self, key):
        
    def list_patients(self):
        '''