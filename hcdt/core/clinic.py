import pandas as pd
from .patient import Patient
from ..assistant_models import MODEL_NAMES_DICT

class Clinic():
    def __init__(self):
        self.__patients = {}
        self.__assistant_model = None
    
    ### Patient Management
    def get_patient(self, patient_id):
        if patient_id in self.__patients:
            return self.__patients[patient_id]
        else:
            return None

    def get_patient_ids(self):
        return list(self.__patients.keys())
    
    def get_patient_info(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.Series({
                'id': patient.id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'gender': patient.gender,
                'age': patient.age
            })
        else:
            return None
    
    def get_patient_conditions(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.conditions)
        else:
            return None
        
    def get_patient_medications(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.medications)
        else:
            return None
    
    def get_patient_encounters(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.encounters) 
        else:
            return None
    
    def get_patient_procedures(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.procedures)
        else:    
            return None
    
    def get_patient_observations(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.observations)
        else:    
            return None

    def get_patient_allergies(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.allergies)
        else:
            return None
    
    def get_patient_immunizations(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.immunizations)
        else:
            return None
    
    def get_patient_careplans(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.careplans)
        else:
            return None
    
    def get_patient_devices(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.devices)
        else:
            return None
    
    def get_patient_imaging_studies(self, patient_id):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            return pd.DataFrame(patient.imaging_studies)
        else:
            return None
                          
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
        self.__load_allergies_from_dataset(data_config)
        self.__load_immunizations_from_dataset(data_config)
        self.__load_careplans_from_dataset(data_config)
        self.__load_devices_from_dataset(data_config)
        self.__load_imaging_studies_from_dataset(data_config)

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
    
    def __load_allergies_from_dataset(self, data_config):
        # Load allergies in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['allergies']['csv_file']
        allergies_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' allergies
        for patient in self.__patients.values():
            if patient.id in allergies_df.index:
                patient_allergies = allergies_df.loc[patient.id]
                # Filter desired columns
                patient_allergies = patient_allergies[data_config['ehr_tables']['allergies']['features']]
                if isinstance(patient_allergies, pd.Series):
                    patient.add_allergy(patient_allergies.to_dict())
                else:
                    for _, row in patient_allergies.iterrows():
                        patient.add_allergy(row.to_dict())
    
    def __load_immunizations_from_dataset(self, data_config):
        # Load immunizations in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['immunizations']['csv_file']
        immunizations_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' immunizations
        for patient in self.__patients.values():
            if patient.id in immunizations_df.index:
                patient_immunizations = immunizations_df.loc[patient.id]
                # Filter desired columns
                patient_immunizations = patient_immunizations[data_config['ehr_tables']['immunizations']['features']]
                if isinstance(patient_immunizations, pd.Series):
                    patient.add_immunization(patient_immunizations.to_dict())
                else:
                    for _, row in patient_immunizations.iterrows():
                        patient.add_immunization(row.to_dict())
    
    def __load_careplans_from_dataset(self, data_config):
        # Load careplans in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['careplans']['csv_file']
        careplans_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' careplans
        for patient in self.__patients.values():
            if patient.id in careplans_df.index:
                patient_careplans = careplans_df.loc[patient.id]
                # Filter desired columns
                patient_careplans = patient_careplans[data_config['ehr_tables']['careplans']['features']]
                if isinstance(patient_careplans, pd.Series):
                    patient.add_careplan(patient_careplans.to_dict())
                else:
                    for _, row in patient_careplans.iterrows():
                        patient.add_careplan(row.to_dict())
    
    def __load_devices_from_dataset(self, data_config):
        # Load devices in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['devices']['csv_file']
        devices_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' devices
        for patient in self.__patients.values():
            if patient.id in devices_df.index:
                patient_devices = devices_df.loc[patient.id]
                # Filter desired columns
                patient_devices = patient_devices[data_config['ehr_tables']['devices']['features']]
                if isinstance(patient_devices, pd.Series):
                    patient.add_device(patient_devices.to_dict())
                else:
                    for _, row in patient_devices.iterrows():
                        patient.add_device(row.to_dict())
    
    def __load_imaging_studies_from_dataset(self, data_config):
        # Load imaging_studies in a DataFrame
        data_dir = data_config['data_directory']
        csv_file = data_config['ehr_tables']['imaging_studies']['csv_file']
        imaging_studies_df = pd.read_csv(f"{data_dir}/{csv_file}", index_col='PATIENT', header=0)
        # Add patients' imaging_studies
        for patient in self.__patients.values():
            if patient.id in imaging_studies_df.index:
                patient_imaging_studies = imaging_studies_df.loc[patient.id]
                # Filter desired columns
                patient_imaging_studies = patient_imaging_studies[data_config['ehr_tables']['imaging_studies']['features']]
                if isinstance(patient_imaging_studies, pd.Series):
                    patient.add_imaging_study(patient_imaging_studies.to_dict())
                else:
                    for _, row in patient_imaging_studies.iterrows():
                        patient.add_imaging_study(row.to_dict())
    
    ### Clinic's Functionalities
    def predict_disease_risk(self, patient_id):
        """Use LLM to analyze patient history and predict high-risk diseases."""
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]

            system_message = "You are a medical AI that predicts future disease risks based on patient EHR."
            user_message = f"Analyze the following patient history:\n"\
                            f"Conditions: {patient.conditions}\n"\
                            f"Medications: {patient.medications}\n"\
                            f"Predict high-risk diseases with probabilities."
            response_template = {
                "disease_risk": [
                    {
                        "disease": "str (predicted disease)",
                        "risk_probability": "float (0-1)",
                        "reasoning": "str (why this disease is likely based on patient data)"
                    }
                ]
            }
            prompt = self.__assistant_model.generate_prompt(system_message, user_message, response_template)
            response = self.__assistant_model.generate_response(prompt)
            return response
        return f"Patient {patient_id} not found."
    
    def check_medication_interactions(self, patient_id):
        """Use the LLM to check for medication interactions."""
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            meds = patient.medications
            if not meds:
                return {"message": "No medications currently prescribed."}
            if len(meds) < 2:
                return {"message": "Only one medication prescribed."}
            
            system_message = "You are a medical AI that checks for dangerous drug interactions."
            user_message = f"Check for interactions between these medications: {meds}.\n"\
                            f"Provide warnings and recommendations if necessary."
            response_template = {
                "interactions": [
                    {
                        "drug_pair": ["str (medication 1)", "str (medication 2)"],
                        "severity": "str (low, moderate, high)",
                        "warning": "str (interaction details and suggested action)"
                    }
                ]
            }
            prompt = self.__assistant_model.generate_prompt(system_message, user_message, response_template)
            response = self.__assistant_model.generate_response(prompt)
            return response
        return f"Patient {patient_id} not found."
    
    def suggest_diagnosis(self, patient_id):
        """Use the LLM assistant to suggest possible conditions based on symptoms."""
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]

            if not patient.observations:
                return {"error": "No recent symptoms recorded."}

            system_message = "You are a highly knowledgeable AI medical assistant."
            user_message = f"A patient presents the following symptoms: {patient.observations}.\n"\
                            f"Existing conditions: {patient.conditions}.\n"\
                            f"What are the most likely diagnoses? Provide a ranked list with reasoning."
            response_template = {
                "diagnoses": [
                    {
                        "condition": "str (diagnosed condition)",
                        "confidence": "float (probability 0-1)",
                        "explanation": "str (brief reasoning)"
                    }
                ]
            }
            prompt = self.__assistant_model.generate_prompt(system_message, user_message, response_template)
            response = self.__assistant_model.generate_response(prompt)
            return response
        return f"Patient {patient_id} not found."