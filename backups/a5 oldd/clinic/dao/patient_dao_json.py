from json import loads, load, dumps
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder
import os


class PatientDAOJSON(PatientDAO):
    def __init__(self, patients, autosave = False):
        ''' Construct a PatientDAOJSON class '''
        if autosave == True:
            self.patients = self.load_patients(autosave)
        if autosave == False:
            self.patients = {}

        self.autosave = autosave
        
    def load_patients(self,autosave):
        ''' loads patient from json file '''
        if autosave is False:
            return
        
        patient_dict = {}
        
        check_file = os.path.isfile("clinic/patients.json") # checks if the json file exists 

        if check_file == False:
            return patient_dict
            

        with open("clinic/patients.json", 'r') as file:

            for patient_json in file: # decodes the json file, gets the patients data, and assigns the patients to their phn
                patient = loads(patient_json, cls=PatientDecoder)
                patient_dict[patient.phn] = patient
                
            file.close()

        return patient_dict
    

    def search_patient(self, key):
        '''gets the patient assigned to a phn/ key'''
        return self.patients.get(key)
        
    def save_patients(self):
        ''' saves the patients data to a json '''

        file = open("clinic/patients.json","w")
        for phn in self.patients: # for each patient - will encode, create a string, and save the string to the json
                patient_str = dumps(self.patients[phn], cls=PatientEncoder)
                file.write("%s\n" % patient_str)

        file.close()

    def create_patient(self, patient):
        ''' Assigns the newly created patient to its phn '''

        self.patients[patient.phn] = patient

        if self.autosave == True:
            self.save_patients()
        return True
    
    def retrieve_patients(self, search_string):
        ''' Returns a list of all patients with the search string in their name as a list'''

        retrieved_patients = []
        for patient in self.patients.values(): # goes through each patient and checks if search string in patient.name
            if search_string in patient.name:
                retrieved_patients.append(patient) # adds to list of returning patients
        return retrieved_patients
    
    def update_patient(self, key, patient):
        ''' Takes in a patient and a key and reassigns the patient to the key'''

        self.patients.pop(key) # removes the previous patient and its phn
        self.patients[patient.phn] = patient
        self.save_patients() # will resave the patients 
        return True
    
    
    def delete_patient(self, key):
        ''' Pops the patient out of the dictionary of patients'''
        self.patients.pop(key)
        self.save_patients()
        return True
    
    def list_patients(self):
        ''' List all patients '''
        patients_list = []
        for patient in self.patients.values(): # adds each patient
            patients_list.append(patient)
        return patients_list