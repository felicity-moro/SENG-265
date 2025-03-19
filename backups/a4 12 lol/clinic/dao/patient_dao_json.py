from json import loads, load, dumps
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder
import os


class PatientDAOJSON(PatientDAO):
    def __init__(self, patients, autosave = False):
        self.patients = self.load_patients(autosave)
        self.autosave = autosave
        
    def load_patients(self,autosave):
        if autosave is False:
            return
        
        patient_dict = {}
        
        
        check_file = os.path.isfile("clinic/patients.json")

        if check_file == False:
            return patient_dict
            

        with open("clinic/patients.json", 'r') as file:

            for patient_json in file:
                patient = loads(patient_json, cls=PatientDecoder)
                patient_dict[patient.phn] = patient
                print(patient)
            file.close()
            #print(patient)

        return patient_dict
    
        '''
        with open("clinic/user_data/patients.json","r") as file:

            for line in file:
                patient_dict = load(file, cls = PatientDecoder)
                cur_patient = PatientDecoder(patient_dict)
                self.patients[cur_patient.phn] = cur_patient
            
            file.close()

            '''

    def search_patient(self, key):
        return self.patients.get(key)
        
    def save_patients(self):
        file = open("clinic/patients.json","w")
        for phn in self.patients:
                patient_str = dumps(self.patients[phn], cls=PatientEncoder)
                file.write("%s\n" % patient_str)

        file.close()

    def create_patient(self, patient):

        self.patients[patient.phn] = patient

        if self.autosave == True:
            self.save_patients()
        return True
    
    def retrieve_patients(self, search_string):
        retrieved_patients = []
        for patient in self.patients.values():
            if search_string in patient.name:
                retrieved_patients.append(patient)
        return retrieved_patients
    
    def update_patient(self, key, patient):

        self.patients.pop(key)

        self.patients[patient.phn] = patient
        self.save_patients()
        return True
    
    
    def delete_patient(self, key):
        self.patients.pop(key)
        self.save_patients()
        return True
    
    def list_patients(self):
        patients_list = []
        for patient in self.patients.values():
            patients_list.append(patient)
        return patients_list