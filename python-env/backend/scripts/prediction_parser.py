import pandas as pd
import xml.etree.ElementTree as ETree
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class PredictionParser:
    def calculate_age(self, birthdate, other_date=date.today()):
        return relativedelta(other_date, birthdate).years

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
            birth_date_formatted = datetime.strptime(birth_date, '%d-%m-%Y').date()
            age = self.calculate_age(birthdate=birth_date_formatted)
            age_range_20 = int(20 <= age < 40 if 1 else 0)
            age_range_40 = int(40 <= age < 60 if 1 else 0)
            age_range_60 = int(age >= 60 if 1 else 0)

            # Medical visit
            medical_visits = patient.iter('medicalVisit')
            for medical_visit in medical_visits:
                visit_date = medical_visit.find('date').text
                visit_date_formatted = datetime.strptime(visit_date, '%d-%m-%Y').date()
                visit_age = self.calculate_age(birthdate=birth_date_formatted, other_date=visit_date_formatted)

                age_range_20 = int(20 <= visit_age < 40 if 1 else 0)
                age_range_40 = int(40 <= visit_age < 60 if 1 else 0)
                age_range_60 = int(visit_age >= 60 if 1 else 0)

                # Treating provider
                treating_provider = medical_visit.find('treatingProvider').text
                treating_provider_dentist = int(treating_provider == 'dentist' if 1 else 0)
                treating_provider_faculty = int(treating_provider == 'faculty' if 1 else 0)
                treating_provider_student = int(treating_provider == 'student' if 1 else 0)

                # Periodontal chart
                periodontal_chart = medical_visit.find('periodontalChart')
                bleeding_on_probing = 0
                nr_of_pocket = 0
                nr_of_furcation = 0
                nr_of_mobility = 0
                total_loss_of_attachment_level = 0

                if periodontal_chart is not None:
                    bleeding_on_probing = int(periodontal_chart.find('bleedingOnProbing').text)
                    nr_of_pocket = int(periodontal_chart.find('nrOfPocket').text)
                    nr_of_furcation = int(periodontal_chart.find('nrOfFurcation').text)
                    nr_of_mobility = int(periodontal_chart.find('nrOfMobility').text)
                    total_loss_of_attachment_level = int(periodontal_chart.find('totalLossOfAttachmentLevel').text)

                # Procedures
                procedure_a = 0
                procedure_b = 0
                procedures = medical_visit.find('procedures')
                if procedures is not None:
                    for procedure in procedures.iter('procedure'):
                        cpt_code = procedure.find('cptCode').text.strip()
                        if cpt_code == 'A':
                            procedure_a = 1
                        if cpt_code == 'B':
                            procedure_b = 1

                patient_item = [
                    # patient_id,
                    # is_male,
                    # is_female,
                    # birth_date,
                    age_range_20,
                    age_range_40,
                    age_range_60,
                    # visit_date,
                    # visit_age,
                    treating_provider_dentist,
                    treating_provider_faculty,
                    treating_provider_student,
                    procedure_a,
                    procedure_b,
                    bleeding_on_probing,
                    nr_of_pocket,
                    nr_of_furcation,
                    nr_of_mobility,
                    total_loss_of_attachment_level,
                ]
                all_items.append(patient_item)

        df = pd.DataFrame(all_items, columns=[
            # 'PATIENT_ID',
            # 'GENDER_MALE',
            # 'GENDER_FEMALE',
            # 'BIRTH_DATE',
            'AGE_RANGE_20',
            'AGE_RANGE_40',
            'AGE_RANGE_60',
            # 'VISIT_DATE',
            # 'VISIT_AGE',
            'TREATING_PROVIDER_DENTIST',
            'TREATING_PROVIDER_FACULTY',
            'TREATING_PROVIDER_STUDENT',
            'PROCEDURE_A',
            'PROCEDURE_B',
            'BLEEDING_ON_PROBING',
            'NR_OF_POCKET',
            'NR_OF_FURCATION',
            'NR_OF_MOBILITY',
            'TOTAL_LOSS_OF_ATTACHMENT_LEVEL',
        ])

        return df
