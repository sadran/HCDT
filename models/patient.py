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

    def get_summary(self):
        return f"""Patient:\n
        gender={self.gender}\n
        age={self.age},\n
        conditions={self.conditions},\n
        medications={self.medications},\n
        encounters={self.encounters},\n
        procedures={self.procedures},\n
        observations={self.observations}\n"""

    def __repr__(self):
        return self.get_summary()
        