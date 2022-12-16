import pandas as pd
import xml.etree.ElementTree as ETree
from datetime import date, datetime


class PatientParser:
    def calculate_age(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def convert_xml_to_dataframe(self, xml_string=''):
        root = ETree.fromstring(xml_string)

        patient_items = []
        all_items = []

        for patient in root.iter('patient'):
            # Demographics
            demographics = patient.find('demoGraphics')
            patient_id = demographics.find('patientID').text

            # Gender
            sex = demographics.find('sex').text
            is_male = int(sex == 'man' if 1 else 0)
            is_female = int(sex == 'woman' if 1 else 0)

            # Age
            birth_date = demographics.find('birthdate').text
            age = self.calculate_age(datetime.strptime(birth_date, '%d-%m-%Y').date())

            # Medical visit
            medical_visits = patient.iter('medicalVisit')
            for medical_visit in medical_visits:
                visit_date = medical_visit.find('date').text

                patient_item = [
                    patient_id,
                    is_male,
                    is_female,
                    birth_date,
                    age,
                    visit_date,
                ]
                all_items.append(patient_item)

        df = pd.DataFrame(all_items, columns=[
            'PATIENT_ID',
            'GENDER_MALE',
            'GENDER_FEMALE',
            'BIRTH_DATE',
            'AGE',
            'VISIT_DATE',
        ])

        return df
