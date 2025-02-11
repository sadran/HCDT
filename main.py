
from models.clinic import Clinic
import yaml
import pandas as pd 

def main():
    # Load data configuration
    with open("configs/data_config.yaml", "r") as file:
        data_config = yaml.safe_load(file)

    # Make a clinic instance
    clinic = Clinic(data_config)

    prompt = clinic.generate_diagnosis_prompt(patient_id='1d604da9-9a81-4ba9-80c2-de3375d59b40')
    print(prompt)
    clinic.diagnose(prompt)


if __name__ == "__main__":
    main()