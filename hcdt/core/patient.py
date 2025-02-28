from datetime import date
import pandas as pd

class Patient:
    def __init__(self, id, first_name, last_name, gender, birth_date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = birth_date

        self.conditions = []
        self.medications = []
        self.encounters = []
        self.procedures = []
        self.observations = []
        self.allergies = []
        self.immunizations = []
        self.careplans = []
        self.devices = []
        self.imaging_studies = []
    
    @property
    def age(self): 
        today = date.today()
        birth_date = date.fromisoformat(self.birth_date)
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    
    def add_condition(self, condition):
        self.conditions.append(condition)
    
    def add_medication(self, medication):
        self.medications.append(medication)
    
    def add_encounter(self, encounter):
        self.encounters.append(encounter)
    
    def add_procedure(self, procedure):
        self.procedures.append(procedure)

    def add_observation(self, observation):
        self.observations.append(observation)

    def add_allergy(self, allergy):
        self.allergies.append(allergy)
    
    def add_immunization(self, immunization):
        self.immunizations.append(immunization)
    
    def add_careplan(self, careplan):
        self.careplans.append(careplan)
    
    def add_device(self, device):
        self.devices.append(device)
    
    def add_imaging_study(self, imaging_study):
        self.imaging_studies.append(imaging_study)

    def __repr__(self):
        return f"""Patient:\n
        gender={self.gender}\n
        age={self.age},\n
        conditions={self.conditions},\n
        medications={self.medications},\n
        encounters={self.encounters},\n
        procedures={self.procedures},\n
        observations={self.observations}\n
        allergies={self.allergies}\n
        immunizations={self.immunizations}\n
        careplans={self.careplans}\n
        devices={self.devices}\n
        imaging_studies={self.imaging_studies}"""

        