from .patient import Patient
from .chatgpt import ChatGPTModel
import pandas as pd

class Clinic():
    def __init__(self, data_config):
        self.__patients = {}
        self.__assistant_model = ChatGPTModel(model="gpt-4")
        self.data_config = data_config

        # Initializing the clinic
        self.__load_patients()
        self.__load_conditions()
        self.__load_encounters()
        self.__load_medications()
        self.__load_procedures()
        self.__load_observations()
    
    def get_patient(self, patient_id):
        return self.__patients[patient_id]

    def generate_diagnosis_prompt(self, patient_id):
        patient_summary = self.__patients[patient_id].get_summary()

        prompt = [{"role": "system", "content": "You are a medical AI diagnosing patients based on EHR."}]
        prompt += [{"role": "user", 
                     "content": f"Based on the following patient history, provide a diagnosis and potential treatment options:\n\n{patient_summary}"}]
        return prompt

    def diagnose(self, prompt):
        self.__assistant_model.diagnose(prompt)
        
    def __load_patients(self):
        # Load patients' data in a DataFrame
        data_dir = self.data_config['data_directory']
        csv_file = self.data_config['patients']['csv_file']
        patients_df = pd.read_csv(f"{data_dir}/{csv_file}", header=0)
        # Initialize Patient objects
        for _, row in patients_df.iterrows():
            patient = Patient(id=row['Id'], first_name=row['FIRST'], last_name=row['LAST'], 
                              gender=row['GENDER'], birth_date=row['BIRTHDATE'])
            self.__patients[row['Id']] = patient

    def __load_conditions(self):
        # Load conditions in a DataFrame
        data_dir = self.data_config['data_directory']
        csv_file = self.data_config['conditions']['csv_file']
        conditions_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' conditions
        for patient in self.__patients.values():
            if patient.id in conditions_df.index:
                patient_conditions = conditions_df.loc[patient.id]
                # Filter desired columns
                patient_conditions = patient_conditions[self.data_config['conditions']['features']]
                if isinstance(patient_conditions, pd.Series):
                    patient.add_condition(patient_conditions.to_dict())
                else:
                    for _, row in patient_conditions.iterrows():
                        patient.add_condition(row.to_dict())
 
    def __load_medications(self):
        # Load medications in a DataFrame
        data_dir = self.data_config['data_directory']
        csv_file = self.data_config['medications']['csv_file']
        medications_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' medications
        for patient in self.__patients.values():
            if patient.id in medications_df.index:
                patient_medications = medications_df.loc[patient.id]
                # Filter desired columns
                patient_medications = patient_medications[self.data_config['medications']['features']]
                if isinstance(patient_medications, pd.Series):
                    patient.add_medication(patient_medications.to_dict())
                else:
                    for _, row in patient_medications.iterrows():
                        patient.add_medication(row.to_dict())
    
    def __load_encounters(self):
        # Load encounters in a DataFrame
        data_dir = self.data_config['data_directory']
        csv_file = self.data_config['encounters']['csv_file']
        encounters_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' encounters
        for patient in self.__patients.values():
            if patient.id in encounters_df.index:
                patient_encounters = encounters_df.loc[patient.id]
                # Filter desired columns
                patient_encounters = patient_encounters[self.data_config['encounters']['features']]
                if isinstance(patient_encounters, pd.Series):
                    patient.add_encounter(patient_encounters.to_dict())
                else:
                    for _, row in patient_encounters.iterrows():
                        patient.add_encounter(row.to_dict())
    
    def __load_procedures(self):
        # Load procedures in a DataFrame
        data_dir = self.data_config['data_directory']
        csv_file = self.data_config['procedures']['csv_file']
        procedures_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' procedures
        for patient in self.__patients.values():
            if patient.id in procedures_df.index:
                patient_procedures = procedures_df.loc[patient.id]
                # Filter desired columns
                patient_procedures = patient_procedures[self.data_config['procedures']['features']]
                if isinstance(patient_procedures, pd.Series):
                    patient.add_procedure(patient_procedures.to_dict())
                else:
                    for _, row in patient_procedures.iterrows():
                        patient.add_procedure(row.to_dict())
    
    def __load_observations(self):
        # Load observations in a DataFrame
        data_dir = self.data_config['data_directory']
        csv_file = self.data_config['observations']['csv_file']
        observations_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' observations
        for patient in self.__patients.values():
            if patient.id in observations_df.index:
                patient_observations = observations_df.loc[patient.id]
                # Filter desired columns
                patient_observations = patient_observations[self.data_config['observations']['features']]
                if isinstance(patient_observations, pd.Series):
                    patient.add_observation(patient_observations.to_dict())
                else:
                    for _, row in patient_observations.iterrows():
                        patient.add_observation(row.to_dict())


   