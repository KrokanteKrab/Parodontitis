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

from scripts.prediction_parser import PredictionParser
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
    epd_xml = request.files['epd_xml']
    read_epd = epd_xml.read()
    prediction_parser = PredictionParser()
    prediction_data = prediction_parser.convert_xml_to_dataframe(read_epd)
    patient_parser = PatientParser()
    patient_data = patient_parser.convert_xml_to_dataframe(read_epd)
    errors = []

    if len(errors) < 1:
        # Predict
        x = np.zeros((len(prediction_data), len(COLUMNS)))

        for i in range(len(prediction_data)):
            for j in range(len(prediction_data.columns)):
                x[i, j] = prediction_data[COLUMNS[j]][i]

        # Prediction
        predictions = model.predict(x)
        prediction_result = []

        for i in range(len(predictions)):
            prediction = {
                "has-not-parodontitis": float(predictions[i][0]),
                "has-parodontitis": float(predictions[i][1]),
                "values": {
                    "AGE_RANGE_20": x[i][0],
                    "AGE_RANGE_40": x[i][1],
                    "AGE_RANGE_60": x[i][2],
                    "TREATING_PROVIDER_DENTIST": x[i][3],
                    "TREATING_PROVIDER_FACULTY": x[i][4],
                    "TREATING_PROVIDER_STUDENT": x[i][5],
                    "PROCEDURE_A": x[i][6],
                    "PROCEDURE_B": x[i][7],
                    "BLEEDING_ON_PROBING": x[i][8],
                    "NR_OF_POCKET": x[i][9],
                    "NR_OF_FURCATION": x[i][10],
                    "NR_OF_MOBILITY": x[i][11],
                    "TOTAL_LOSS_OF_ATTACHMENT_LEVEL": x[i][12]
                }
            }

            prediction_result.append(prediction)

        # Patient
        patient_result = {
            "PATIENT_ID": patient_data['PATIENT_ID'][0],
            "GENDER_MALE": int(patient_data['GENDER_MALE'][0]),
            "GENDER_FEMALE": int(patient_data['GENDER_FEMALE'][0]),
            "BIRTH_DATE": patient_data['BIRTH_DATE'][0],
            "AGE": int(patient_data['AGE'][0])
        }

        visit_result = []
        for i in range(len(patient_data)):
            visit = {
                "VISIT_DATE": patient_data['VISIT_DATE'][i]
            }

            visit_result.append(visit)

        # Request response
        response = {
            "id": str(uuid.uuid4()),
            "errors": errors,
            "predictions": prediction_result,
            "patient": patient_result,
            "visits": visit_result
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
