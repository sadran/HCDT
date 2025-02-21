import pandas as pd
from .patient import Patient
from ..assistant_models import MODEL_NAMES_DICT

class Clinic():
    def __init__(self):
        self.__patients = {}
        self.__assistant_model = None
    
    ### Patient Management
    def get_patient(self, patient_id):
        return self.__patients[patient_id]

    def get_patient_ids(self):
        return list(self.__patients.keys())
    
    def get_patient_info(self, patient_id):
        patient = self.__patients[patient_id]
        return pd.Series({
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'gender': patient.gender,
            'age': patient.age
        })
    
    def get_patient_conditions(self, patient_id):
        patient = self.__patients[patient_id]
        return pd.DataFrame(patient.conditions)
    
    def get_patient_medications(self, patient_id):
        patient = self.__patients[patient_id]
        return pd.DataFrame(patient.medications)
    
    def get_patient_encounters(self, patient_id):
        patient = self.__patients[patient_id]
        return pd.DataFrame(patient.encounters)
    
    def get_patient_procedures(self, patient_id):
        patient = self.__patients[patient_id]
        return pd.DataFrame(patient.procedures)
    
    def get_patient_observations(self, patient_id):
        patient = self.__patients[patient_id]
        return pd.DataFrame(patient.observations)
                            
    ### Model Assistant Management
    @staticmethod
    def get_available_assistant_model_names():
        return list(MODEL_NAMES_DICT.keys())
    
    def set_assistant_model(self, model_config):
        if model_config is None:
            self.__assistant_model = None
        else:
            model_name = model_config['model_name']
            if model_name in MODEL_NAMES_DICT:
                self.__assistant_model = MODEL_NAMES_DICT[model_name](model_config)
            else:
                print(f"Model {model_name} not found.")

    def get_assistant_model_name(self):
        if self.__assistant_model is None:
            return None
        return self.__assistant_model.model_name
    
    ### Loading Dataset
    def load_dataset(self, data_config):
        self.__load_patients_from_dataset(data_config)
        self.__load_conditions_from_dataset(data_config)
        self.__load_encounters_from_dataset(data_config)
        self.__load_medications_from_dataset(data_config)
        self.__load_procedures_from_dataset(data_config)
        self.__load_observations_from_dataset(data_config)

    def __load_patients_from_dataset(self, data_config):
        # Load patients' data in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['patients']['csv_file']
        patients_df = pd.read_csv(f"{data_dir}/{csv_file}", header=0)
        # Initialize Patient objects
        for _, row in patients_df.iterrows():
            patient = Patient(id=row['Id'], first_name=row['FIRST'], last_name=row['LAST'], 
                              gender=row['GENDER'], birth_date=row['BIRTHDATE'])
            self.__patients[row['Id']] = patient

    def __load_conditions_from_dataset(self, data_config):
        # Load conditions in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['conditions']['csv_file']
        conditions_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' conditions
        for patient in self.__patients.values():
            if patient.id in conditions_df.index:
                patient_conditions = conditions_df.loc[patient.id]
                # Filter desired columns
                patient_conditions = patient_conditions[data_config['ehr_tables']['conditions']['features']]
                if isinstance(patient_conditions, pd.Series):
                    patient.add_condition(patient_conditions.to_dict())
                else:
                    for _, row in patient_conditions.iterrows():
                        patient.add_condition(row.to_dict())
 
    def __load_medications_from_dataset(self, data_config):
        # Load medications in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['medications']['csv_file']
        medications_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' medications
        for patient in self.__patients.values():
            if patient.id in medications_df.index:
                patient_medications = medications_df.loc[patient.id]
                # Filter desired columns
                patient_medications = patient_medications[data_config['ehr_tables']['medications']['features']]
                if isinstance(patient_medications, pd.Series):
                    patient.add_medication(patient_medications.to_dict())
                else:
                    for _, row in patient_medications.iterrows():
                        patient.add_medication(row.to_dict())
    
    def __load_encounters_from_dataset(self, data_config):
        # Load encounters in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['encounters']['csv_file']
        encounters_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' encounters
        for patient in self.__patients.values():
            if patient.id in encounters_df.index:
                patient_encounters = encounters_df.loc[patient.id]
                # Filter desired columns
                patient_encounters = patient_encounters[data_config['ehr_tables']['encounters']['features']]
                if isinstance(patient_encounters, pd.Series):
                    patient.add_encounter(patient_encounters.to_dict())
                else:
                    for _, row in patient_encounters.iterrows():
                        patient.add_encounter(row.to_dict())
    
    def __load_procedures_from_dataset(self, data_config):
        # Load procedures in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['procedures']['csv_file']
        procedures_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' procedures
        for patient in self.__patients.values():
            if patient.id in procedures_df.index:
                patient_procedures = procedures_df.loc[patient.id]
                # Filter desired columns
                patient_procedures = patient_procedures[data_config['ehr_tables']['procedures']['features']]
                if isinstance(patient_procedures, pd.Series):
                    patient.add_procedure(patient_procedures.to_dict())
                else:
                    for _, row in patient_procedures.iterrows():
                        patient.add_procedure(row.to_dict())
    
    def __load_observations_from_dataset(self, data_config):
        # Load observations in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['observations']['csv_file']
        observations_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' observations
        for patient in self.__patients.values():
            if patient.id in observations_df.index:
                patient_observations = observations_df.loc[patient.id]
                # Filter desired columns
                patient_observations = patient_observations[data_config['ehr_tables']['observations']['features']]
                if isinstance(patient_observations, pd.Series):
                    patient.add_observation(patient_observations.to_dict())
                else:
                    for _, row in patient_observations.iterrows():
                        patient.add_observation(row.to_dict())
    
    ### Clinic's Functionalities
    # Diagnose a patient
    def diagnose_patient(self, patient_id):
        patient = self.__patients[patient_id]
        prompt = self.__assistant_model.generate_diagnose_prompt(patient)
        return self.__assistant_model.generate_response(prompt)
    # Summarize a patient
    def summarize_patient(self, patient_id):
        patient = self.__patients[patient_id]
        prompt = self.__assistant_model.generate_summary_prompt(patient)
        return self.__assistant_model.generate_response(prompt)
    