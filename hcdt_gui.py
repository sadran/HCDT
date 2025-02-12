from models.clinic import Clinic
import yaml
import tkinter as tk
from tkinter import ttk

class HCDTApp():
    def __init__(self, clinic, data_config):
        self.clinic = clinic
        self.data_config = data_config
        self.root = tk.Tk()
        self.root.title("Healthcare Digital Twin")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Variables
        self.patient_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")

        # Patient IDs dropdown
        self.label_dropdown("Patient IDs:", clinic.get_patient_ids(), 0)
        # Patient Demographics
        self.label_entry("First name:", self.first_name_var, 1)
        self.label_entry("Last name:", self.last_name_var, 2)
        self.label_entry("Age:", self.age_var, 3)
        self.label_entry("Gender:", self.gender_var, 4)
        # Patient EHR
        self.conditions_table = self.label_table("Conditions:", data_config['conditions']['features'], 5)
        self.medications_table = self.label_table("Medications:", data_config['medications']['features'], 6)
        self.encounters_table = self.label_table("Encounters:", data_config['encounters']['features'], 7)
        self.procedures_table = self.label_table("Procedures:", data_config['procedures']['features'], 8)
        self.observations_table = self.label_table("Observations:", data_config['observations']['features'], 9)
        
        self.patient_dropdown.bind("<<ComboboxSelected>>", self.__on_patient_selected)

        self.diagnosis_textbox = self.button_textbox("Diagnose Patient", self.__on_diagnose_button_pressed, 10)
        self.summary_textbox = self.button_textbox("Summarize Patient", self.__on_summarize_button_pressed, 11)

    def mainloop(self):
        self.root.mainloop()

    # patient dropdown       
    def label_dropdown(self, label_text, dropdown_values, grid_row, pad=(10, 10)):
        tk.Label(self.main_frame, text=label_text).grid(row=grid_row, column=0, sticky="e", padx=pad[0], pady=pad[1])
        self.patient_dropdown = ttk.Combobox(self.main_frame, textvariable=self.patient_var, values=["Please select the patient ID"] + dropdown_values)
        self.patient_dropdown.grid(row=grid_row, column=1, sticky="ew", padx=pad[0], pady=pad[1])
        self.patient_dropdown.current

    # label and entry field
    def label_entry(self, label_text, variable, grid_row, pad=(10, 5)):
        tk.Label(self.main_frame, text=label_text).grid(row=grid_row, column=0, sticky="e", padx=pad[0], pady=pad[1])
        tk.Entry(self.main_frame, textvariable=variable, state="readonly").grid(row=grid_row, column=1, sticky="ew", padx=pad[0], pady=pad[1])

    # label and table
    def label_table(self, label_text, columns, grid_row, pad=(10, 10), height=5):
        tk.Label(self.main_frame, text=label_text).grid(row=grid_row, column=0, sticky="en", padx=pad[0], pady=pad[1])
        table = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=height)
        for feature in columns:
            table.heading(feature, text=feature)
        table.grid(row=grid_row, column=1, sticky="ew", padx=pad[0], pady=pad[1])
        return table
    
    # button and textbox
    def button_textbox(self, button_text, button_command, grid_row, textbox_height=5, pad=(10, 10)):
        tk.Button(self.main_frame, text=button_text, command=button_command).grid(row=grid_row, column=0, sticky="ew", padx=pad[0], pady=pad[1])
        textbox = tk.Text(self.main_frame, height=textbox_height)
        textbox.grid(row=grid_row, column=1, sticky="ew", padx=pad[0], pady=pad[1])
        return textbox

    # Update the patient information fields when a patient is selected
    def __on_patient_selected(self, event):
        selected_id = self.patient_var.get()
        if selected_id != "Please select the patient ID":
            patient = self.clinic.get_patient(selected_id)
            self.first_name_var.set(patient.first_name)
            self.last_name_var.set(patient.last_name)
            self.age_var.set(patient.age)
            self.gender_var.set(patient.gender)
            self.__update_table(self.conditions_table, patient.conditions, self.data_config['conditions']['features'])
            self.__update_table(self.medications_table, patient.medications, self.data_config['medications']['features'])
            self.__update_table(self.encounters_table, patient.encounters, self.data_config['encounters']['features'])
            self.__update_table(self.procedures_table, patient.procedures, self.data_config['procedures']['features'])
            self.__update_table(self.observations_table, patient.observations, self.data_config['observations']['features'])
        else:
            self.first_name_var.set("")
            self.last_name_var.set("")
            self.age_var.set("")
            self.gender_var.set("")
            self.__update_table(self.conditions_table, [], self.data_config['conditions']['features'])
            self.__update_table(self.medications_table, [], self.data_config['medications']['features'])
            self.__update_table(self.encounters_table, [], self.data_config['encounters']['features'])
            self.__update_table(self.procedures_table, [], self.data_config['procedures']['features'])
            self.__update_table(self.observations_table, [], self.data_config['observations']['features'])
        
    # Update the table with the data
    def __update_table(conditions_table, table, data, features):
            for row in table.get_children():
                table.delete(row)
            for item in data:
                table.insert("", "end", values=[item[feature] for feature in features])  
    
    # Button event handlers
    def __on_diagnose_button_pressed(self):
        response = "He won't live so long !"
        self.diagnosis_textbox.delete("1.0", "end")
        self.diagnosis_textbox.insert("1.0", response)

    def __on_summarize_button_pressed(self):
        response = "He is dying !"
        self.summary_textbox.delete("1.0", "end")
        self.summary_textbox.insert("1.0", response)
                

def main():
    # Load data configuration
    with open("configs/data_config.yaml", "r") as file:
        data_config = yaml.safe_load(file)

    # Make a clinic instance
    clinic = Clinic()
    # Load data to the clinic
    clinic.load_data(data_config)

    app = HCDTApp(clinic, data_config)
   
    # Run the GUI
    app.mainloop()

if __name__ == "__main__":
    main()