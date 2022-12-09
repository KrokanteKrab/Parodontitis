import xml.etree.ElementTree as ETree
from datetime import date, datetime

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def convert_xml_to_dataframe(path='../data/patient-complete.xml'):
    parse_tree = ETree.parse(path)
    root = parse_tree.getroot()

    patient_items = []
    all_items = []

    for patient in root.iter('patient'):
        # Demographics
        demographics = patient.find('demoGraphics')
        patient_id = demographics.find('patientID').text
        sex = demographics.find('sex').text
        birth_date = demographics.find('birthdate').text

        age = calculate_age(datetime.strptime(birth_date, '%d-%m-%Y').date())

        # TODO: might have to loop if there can be multiple medical visits or only take some of the data
        # Medical visit
        medical_visit = patient.find('medicalVisit')
        date = medical_visit.find('date').text
        treating_provider = medical_visit.find('treatingProvider').text
        # Periodontal charts
        periodontal_charts = medical_visit.find('periodontalCharts')
        bleeding_on_probing = int(periodontal_charts.find('bleedingOnProbing').text)
        nr_of_pocket = int(periodontal_charts.find('nrOfPocket').text)
        nr_of_furcation = int(periodontal_charts.find('nrOfFurcation').text)
        nr_of_mobility = int(periodontal_charts.find('nrOfMobility').text)
        total_loss_of_attachment_level = int(periodontal_charts.find('totalLossOfAttachmentLevel').text)

        patient_item = [
            patient_id, sex, birth_date,
            date, treating_provider,
            bleeding_on_probing, nr_of_pocket, nr_of_furcation, nr_of_mobility, total_loss_of_attachment_level
        ]
        all_items.append(patient_item)

    df = pd.DataFrame(all_items, columns=[
        'PATIENT_ID', 'SEX', 'BIRTH_DATE',
        'VISIT_DATE', 'TREATING_PROVIDER',
        'BLEEDING_ON_PROBING', 'NR_OF_POCKET', 'NR_OF_FURCATION', 'NR_OF_MOBILITY', 'TOTAL_LOSS_OF_ATTACHMENT_LEVEL'
    ])

    # TODO: Temporary way to add labels
    # df['HAS_PARODONTITIS'] = [True, False, False, True, True]
    # df['HAS_PARODONTITIS'] = [1, 0, 0, 1, 1]
    df['HAS_PARODONTITIS'] = [1]

    return df