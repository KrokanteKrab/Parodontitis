# ---------------------------------
# Krokante Krab 🦀 - 2022
#              by Iza, Leander, Tim en Youri
# ---------------------------------
import uuid
import numpy as np
import shap
import base64

import pandas as pd

from flask import Flask, request, jsonify
from keras.models import load_model
from io import BytesIO
from flask_cors import CORS
from sklearn.model_selection import train_test_split

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from scripts.patient_parser import PatientParser

app = Flask(__name__)
# Solves Cross Origin Resource Sharing (CORS)
CORS(app)

# Used for validation
EXPECTED = {
    # TODO: Define constraints on data if needed
}

COLUMNS = [
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
    # 'NOICE_MODIFIED',
    # 'STUDENT_ERROR'
]
RANDOM_STATE = 1


# This method is used for loading the needed data.
def load_data():
    # Fetch data from csv file.
    data = pd.read_csv('./data/patients-v6.csv')

    # Only take the needed column(s)
    X = data[COLUMNS]

    y = data[[
        'HAS_PARODONTITIS'
    ]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=RANDOM_STATE)

    return (X_train, X_test), (y_train, y_test)


# The setup method is used for setting everything up that we need to work with
def setup():
    # Load neural network
    _model = load_model("./model/model-best-v2.h5")

    # Load training data
    (X_train, _), _ = load_data()

    # Load SHAP (Explain ability AI)
    _shap_explainer = shap.KernelExplainer(_model, X_train[:100])

    return _model, _shap_explainer


(model, shap_explainer) = setup()


@app.route('/', methods=['GET'])
def root():
    response = {
        "author": "Krokante Krab 🦀",
        "description": "API for parodontitis prediction",
        "version": "1.0.1"
    }
    return jsonify(response)


@app.route('/api/predict', methods=['POST'])
def predict():
    patient_xml = request.files['patient_xml']
    patient_parser = PatientParser()
    patients = patient_parser.convert_xml_to_dataframe(patient_xml.read())
    errors = []

    if len(errors) < 1:
        # Predict
        x = np.zeros((1, 13))

        for i in range(len(patients.columns)):
            x[0, i] = patients[patients.columns[i]][0]

        # Prediction
        prediction = model.predict(x)
        prediction = {
            "has-not-parodontitis": float(prediction[0][0]),
            "has-parodontitis": float(prediction[0][1]),
            "values": {
                "AGE_RANGE_20": x[0][0],
                "AGE_RANGE_40": x[0][1],
                "AGE_RANGE_60": x[0][2],
                "TREATING_PROVIDER_DENTIST": x[0][3],
                "TREATING_PROVIDER_FACULTY": x[0][4],
                "TREATING_PROVIDER_STUDENT": x[0][5],
                "PROCEDURE_A": x[0][6],
                "PROCEDURE_B": x[0][7],
                "BLEEDING_ON_PROBING": x[0][8],
                "NR_OF_POCKET": x[0][9],
                "NR_OF_FURCATION": x[0][10],
                "NR_OF_MOBILITY": x[0][11],
                "TOTAL_LOSS_OF_ATTACHMENT_LEVEL": x[0][12]
            }
        }

        # Request response
        response = {
            "id": str(uuid.uuid4()),
            "errors": errors,
            "prediction": prediction
        }
    else:
        # Return errors
        response = {"id": str(uuid.uuid4()), "errors": errors}

    return jsonify(response)


@app.route('/api/shap-img', methods=['POST'])
def shap_img():
    content = request.json
    errors = []

    if len(errors) < 1:
        # Predict
        x = np.zeros((1, 13))

        for i in range(len(COLUMNS)):
            x[0, i] = content[COLUMNS[i]]

        print(x)

        # Prediction
        prediction = model.predict(x)
        prediction = {
            "has-not-parodontitis": float(prediction[0][0]),
            "has-parodontitis": float(prediction[0][1])
        }

        shap_values = shap_explainer.shap_values(x)
        if prediction["has-not-parodontitis"] > prediction["has-parodontitis"]:
            shap.force_plot(
                shap_explainer.expected_value[0], shap_values[0], x, matplotlib=True, show=False,
                plot_cmap=['#77dd77', '#f99191'], feature_names=COLUMNS
            )
        else:
            shap.force_plot(
                shap_explainer.expected_value[1], shap_values[1], x, matplotlib=True, show=False,
                plot_cmap=['#77dd77', '#f99191'], feature_names=COLUMNS
            )

        # Encode shap img into base64,
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches="tight")
        shap_img = base64.b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")

        # Request response
        response = {
            "id": str(uuid.uuid4()),
            "shap-img": shap_img,
            "errors": errors,
        }

    else:
        # Return errors
        response = {"id": str(uuid.uuid4()), "errors": errors}

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
