from datetime import date

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

    def __repr__(self):
        return f"""Patient: 
        id={self.id}, 
        first_name={self.first_name}, 
        last_name={self.last_name},
        age={self.age},
        conditions=[{self.conditions}], 
        medications=[{self.medications}],
        encounters=[{self.encounters}],
        procedures=[{self.procedures}],
        observations=[{self.observations}]"""
        