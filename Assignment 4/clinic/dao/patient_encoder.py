from clinic.patient import Patient
from json import JSONEncoder

class PatientEncoder(JSONEncoder):

    def default(self, patient:Patient) ->dict:
        if isinstance(patient, Patient):
            return {"__type__": "Patient","phn":patient.phn,"name":patient.name, "birth_date":patient.birth_date, "phone":patient.phone, "email": patient.email, "address": patient.address,"autosave":patient.autosave }
        return super().default(patient) 
