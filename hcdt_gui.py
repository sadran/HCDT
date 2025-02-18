from hcdt import Clinic
import yaml
import tkinter as tk
from tkinter import ttk

class HCDTApp():
    def __init__(self, clinic, data_config, model_config):
        self.clinic = clinic
        self.data_config = data_config
        self.model_config = model_config
        self.root = tk.Tk()
        self.root.geometry("1200x800")
        self.root.title("Healthcare Digital Twin")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        # Create a canvas and a scrollbar
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.main_frame = self.scrollable_frame

        # Variables
        self.patient_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.model_var = tk.StringVar()

        self.patient_var.set("Please select the patient ID")
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.model_var.set('No model selected' if self.clinic.get_model() is None else self.clinic.get_model())
        

        # Patient IDs dropdown
        self.patient_dropdown = self.label_dropdown("Patient IDs:", self.patient_var,["Please select the patient ID"] + clinic.get_patient_ids(), 0)
        # Patient Demographics
        self.label_entry("First name:", self.first_name_var, 1)
        self.label_entry("Last name:", self.last_name_var, 2)
        self.label_entry("Age:", self.age_var, 3)
        self.label_entry("Gender:", self.gender_var, 4)
        # Patient EHR
        self.conditions_table = self.label_table("Conditions:", data_config['ehr_tables']['conditions']['features'], 5)
        self.medications_table = self.label_table("Medications:", data_config['ehr_tables']['medications']['features'], 6)
        self.encounters_table = self.label_table("Encounters:", data_config['ehr_tables']['encounters']['features'], 7)
        self.procedures_table = self.label_table("Procedures:", data_config['ehr_tables']['procedures']['features'], 8)
        self.observations_table = self.label_table("Observations:", data_config['ehr_tables']['observations']['features'], 9)
        
        self.patient_dropdown.bind("<<ComboboxSelected>>", self.__on_patient_selected)

        self.model_dropdown = self.label_dropdown("Assistant Model:", self.model_var, ["No model selected"] + list(model_config.keys()), 10)
        self.model_dropdown.bind("<<ComboboxSelected>>", self.__on_model_selected)

        self.diagnosis_textbox = self.button_textbox("Diagnose Patient", self.__on_diagnose_button_pressed, 11)
        self.summary_textbox = self.button_textbox("Summarize Patient", self.__on_summarize_button_pressed, 12)

    def mainloop(self):
        self.root.mainloop()

    # patient dropdown       
    def label_dropdown(self, label_text, dropdown_variable, dropdown_values, grid_row, pad=(10, 10)):
        tk.Label(self.main_frame, text=label_text).grid(row=grid_row, column=0, sticky="e", padx=pad[0], pady=pad[1])
        dropdown = ttk.Combobox(self.main_frame, textvariable = dropdown_variable, values = dropdown_values)
        dropdown.grid(row=grid_row, column=1, sticky="ew", padx=pad[0], pady=pad[1])
        dropdown.current
        return dropdown

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
    def button_textbox(self, button_text, button_command, grid_row, textbox_height=20, pad=(10, 10)):
        tk.Button(self.main_frame, text=button_text, command=button_command).grid(row=grid_row, column=0, sticky="new", padx=pad[0], pady=pad[1])
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
            self.__update_table(self.conditions_table, patient.conditions, self.data_config['ehr_tables']['conditions']['features'])
            self.__update_table(self.medications_table, patient.medications, self.data_config['ehr_tables']['medications']['features'])
            self.__update_table(self.encounters_table, patient.encounters, self.data_config['ehr_tables']['encounters']['features'])
            self.__update_table(self.procedures_table, patient.procedures, self.data_config['ehr_tables']['procedures']['features'])
            self.__update_table(self.observations_table, patient.observations, self.data_config['ehr_tables']['observations']['features'])
            self.diagnosis_textbox.delete("1.0", "end")
            self.summary_textbox.delete("1.0", "end")
        else:
            self.first_name_var.set("")
            self.last_name_var.set("")
            self.age_var.set("")
            self.gender_var.set("")
            self.__update_table(self.conditions_table, [], self.data_config['ehr_tables']['conditions']['features'])
            self.__update_table(self.medications_table, [], self.data_config['ehr_tables']['medications']['features'])
            self.__update_table(self.encounters_table, [], self.data_config['ehr_tables']['encounters']['features'])
            self.__update_table(self.procedures_table, [], self.data_config['ehr_tables']['procedures']['features'])
            self.__update_table(self.observations_table, [], self.data_config['ehr_tables']['observations']['features'])
            self.diagnosis_textbox.delete("1.0", "end")
            self.summary_textbox.delete("1.0", "end")
    
    # Update the model when a model is selected
    def __on_model_selected(self, event):
        selected_model = self.model_var.get()
        if selected_model != "No model selected":
            self.clinic.set_model(self.model_config[selected_model])
            self.diagnosis_textbox.delete("1.0", "end")
            self.summary_textbox.delete("1.0", "end")
        else:
            self.clinic.set_model(None)
            self.diagnosis_textbox.delete("1.0", "end")
            self.summary_textbox.delete("1.0", "end")

    # Update the table with the data
    def __update_table(conditions_table, table, data, features):
            for row in table.get_children():
                table.delete(row)
            for item in data:
                table.insert("", "end", values=[item[feature] for feature in features])  
    
    # Button event handlers
    def __on_diagnose_button_pressed(self):
        if self.patient_var.get() == "Please select the patient ID":
            response = "Please select a patient ID"
        elif self.model_var.get() == "No model selected":
            response = "Please select a model"
        else:
            response = self.clinic.diagnose_patient(self.patient_var.get())
        self.diagnosis_textbox.delete("1.0", "end")
        self.diagnosis_textbox.insert("1.0", response)

    def __on_summarize_button_pressed(self):
        if self.patient_var.get() == "Please select the patient ID":
            response = "Please select a patient ID"
        elif self.model_var.get() == "No model selected":
            response = "Please select a model"
        else:
            response = self.clinic.summarize_patient(self.patient_var.get())
        self.summary_textbox.delete("1.0", "end")
        self.summary_textbox.insert("1.0", response)
                
    

def main():
    # Load data configuration
    with open("configs/data_config.yaml", "r") as file:
        data_config = yaml.safe_load(file)
    
    # Load models configuration
    with open("configs/model_config.yaml", "r") as file:
        model_config = yaml.safe_load(file)

    # Make a clinic instance
    clinic = Clinic()
    # Load data to the clinic
    clinic.load_data(data_config)
    # Set the model for the clinic
    #clinic.set_model(model_config['medllama'])
    # Create the GUI
    app = HCDTApp(clinic, data_config, model_config)
   
    # Run the GUI
    app.mainloop()

if __name__ == "__main__":
    main()