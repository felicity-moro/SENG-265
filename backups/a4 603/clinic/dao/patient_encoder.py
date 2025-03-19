from clinic.patient import Patient
from json import JSONEncoder

class PatientEncoder(JSONEncoder):

    def default(self, patient:Patient) ->dict:
        return {"__type__": "Patient","__phn__":patient.phn,"__name__":patient.name, "__birth_date__":patient.birth_date, "__phone__":patient.phone, "__email__": patient.email, "__address__": patient.address} 
