from models.patient import Patient
import yaml
import pandas as pd 

def main():
    # Load data configuration
    with open("configs/data_config.yaml", "r") as file:
        data_config = yaml.safe_load(file)
    
    # Load datasets
    data_dir = data_config["data_directory"]
    patients_df = pd.read_csv(f"{data_dir}/patients.csv", header=0)
    conditions_df = pd.read_csv(f"{data_dir}/conditions.csv", index_col="PATIENT", header=0)
    medications_df = pd.read_csv(f"{data_dir}/medications.csv", index_col="PATIENT", header=0)
    encounters_df = pd.read_csv(f"{data_dir}/encounters.csv", index_col="PATIENT", header=0)
    procedures_df = pd.read_csv(f"{data_dir}/procedures.csv", index_col="PATIENT", header=0)
    observations_df = pd.read_csv(f"{data_dir}/observations.csv", index_col="PATIENT", header=0)

    # Create patient dictionary
    patients = {}

    # Initialize Patient objects
    for _, row in patients_df.iterrows():
        patient = Patient(id=row["Id"], first_name=row["FIRST"], last_name=row["LAST"], 
                          gender=row["GENDER"], birth_date=row["BIRTHDATE"])
        patients[row["Id"]] = patient

    print(list(patients.values())[0])


if __name__ == "__main__":
    main()