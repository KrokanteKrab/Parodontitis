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
            is_male = int(sex == 'male' if 1 else 0)
            is_female = int(sex == 'female' if 1 else 0)

            # Age
            birth_date = demographics.find('birthdate').text
            age = self.calculate_age(datetime.strptime(birth_date, '%d-%m-%Y').date())
            age_range_20 = int(20 <= age < 40 if 1 else 0)
            age_range_40 = int(40 <= age < 60 if 1 else 0)
            age_range_60 = int(age >= 60 if 1 else 0)

            # TODO: might have to loop if there can be multiple medical visits or only take some of the data
            # Medical visit
            medical_visit = patient.find('medicalVisit')
            visit_date = medical_visit.find('date').text

            # Treating provider
            treating_provider = medical_visit.find('treatingProvider').text
            treating_provider_dentist = int(treating_provider == 'dentist' if 1 else 0)
            treating_provider_faculty = int(treating_provider == 'faculty' if 1 else 0)
            treating_provider_student = int(treating_provider == 'student' if 1 else 0)

            # Periodontal charts
            periodontal_charts = medical_visit.find('periodontalCharts')
            bleeding_on_probing = int(periodontal_charts.find('bleedingOnProbing').text)
            nr_of_pocket = int(periodontal_charts.find('nrOfPocket').text)
            nr_of_furcation = int(periodontal_charts.find('nrOfFurcation').text)
            nr_of_mobility = int(periodontal_charts.find('nrOfMobility').text)
            total_loss_of_attachment_level = int(periodontal_charts.find('totalLossOfAttachmentLevel').text)

            # Procedures
            procedure_a = 0
            procedure_b = 0
            procedures = medical_visit.find('procedures')
            for procedure in procedures.iter('procedure'):
                cpt_code = procedure.find('cptCode').text
                if cpt_code == 'A':
                    procedure_a = 1
                if cpt_code == 'B':
                    procedure_b = 1

            # Has Parodontitis
            has_parodontitis = int(patient.find('hasParodontitis').text)

            patient_item = [
                # patient_id,
                # is_male,
                # is_female,
                # birth_date,
                age_range_20,
                age_range_40,
                age_range_60,
                # visit_date,
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
                has_parodontitis
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
            'HAS_PARODONTITIS'
        ])

        return df
