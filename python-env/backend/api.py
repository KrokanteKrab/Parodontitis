# ----------------------------------
# Krokante Krab 🦀 - 2022
#              by Iza, Leander, Tim en Youri
# ----------------------------------
import string
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

import sys

sys.path.insert(0, '../_shared')
from data_parser import DataParser

app = Flask(__name__)
# Solves Cross Origin Resource Sharing (CORS)
CORS(app)

PREDICTION_COLUMNS = [
    'AGE_RANGE_20',
    'AGE_RANGE_40',
    'AGE_RANGE_60',
    'TREATING_PROVIDER_DENTIST',
    'TREATING_PROVIDER_FACULTY',
    'TREATING_PROVIDER_STUDENT',
    'DDS_CODE_D4210',
    'DDS_CODE_D4211',
    'BLEEDING_ON_PROBING',
    'NR_OF_POCKET',
    'NR_OF_FURCATION',
    'NR_OF_MOBILITY',
    'TOTAL_LOSS_OF_ATTACHMENT_LEVEL'
]
RANDOM_STATE = 1


# This method is used for loading the needed data.
def load_data():
    # Fetch data from csv file.
    data = pd.read_csv('../_shared/data/synthetic-v2/data.csv')

    # Only take the needed column(s)
    X = data[PREDICTION_COLUMNS]

    y = data[[
        'HAS_PARODONTITIS'
    ]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=RANDOM_STATE)

    return (X_train, X_test), (y_train, y_test)


# The setup method is used for setting everything up that we need to work with
def setup():
    # TODO: Get best model after training
    # Load neural network
    _model = load_model("./model/model-best-synthetic-v2.h5")

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
    dataParser = DataParser()
    df = dataParser.convert_xml_to_dataframe(read_epd)

    df_prediction = df[PREDICTION_COLUMNS]

    # Predict
    x = np.zeros((len(df_prediction), len(PREDICTION_COLUMNS)))

    for i in range(len(df_prediction)):
        for j in range(len(PREDICTION_COLUMNS)):
            x[i, j] = df_prediction[PREDICTION_COLUMNS[j]][i]

    # Prediction
    predictions = model.predict(x)
    prediction_result = []

    for i in range(len(predictions)):
        prediction = {
            "has-not-parodontitis": float(predictions[i][0]),
            "has-parodontitis": float(predictions[i][1]),
            "show-shap": 0,
            "values": {
                "AGE_RANGE_20": x[i][0],
                "AGE_RANGE_40": x[i][1],
                "AGE_RANGE_60": x[i][2],
                "TREATING_PROVIDER_DENTIST": x[i][3],
                "TREATING_PROVIDER_FACULTY": x[i][4],
                "TREATING_PROVIDER_STUDENT": x[i][5],
                "DDS_CODE_D4210": x[i][6],
                "DDS_CODE_D4211": x[i][7],
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
        "PATIENT_ID": df['PATIENT_ID'][0],
        "GENDER_MALE": int(df['GENDER_MALE'][0]),
        "GENDER_FEMALE": int(df['GENDER_FEMALE'][0]),
        "BIRTH_DATE": df['BIRTH_DATE'][0]
    }

    visit_result = []
    for i in range(len(df)):
        visit = {
            "VISIT_DATE": df['VISIT_DATE'][i],
            "VISIT_AGE": int(df['VISIT_AGE'][i])
        }

        visit_result.append(visit)

    # Request response
    response = {
        "id": str(uuid.uuid4()),
        "predictions": prediction_result,
        "patient": patient_result,
        "visits": visit_result
    }

    return jsonify(response)


@app.route('/api/shap-img', methods=['POST'])
def shap_img():
    content = request.json

    # Predict
    x = np.zeros((1, 13))

    for i in range(len(PREDICTION_COLUMNS)):
        x[0, i] = content[PREDICTION_COLUMNS[i]]

    # Prediction
    prediction = model.predict(x)
    prediction = {
        "has-not-parodontitis": float(prediction[0][0]),
        "has-parodontitis": float(prediction[0][1])
    }

    aliases = string.ascii_uppercase[:len(PREDICTION_COLUMNS)]
    shap_values = shap_explainer.shap_values(x)
    if prediction["has-not-parodontitis"] > prediction["has-parodontitis"]:
        shap.force_plot(
            shap_explainer.expected_value[0], shap_values[0], x, matplotlib=True, show=False,
            plot_cmap=['#77dd77', '#f99191'], feature_names=aliases
        )
    else:
        shap.force_plot(
            shap_explainer.expected_value[1], shap_values[1], x, matplotlib=True, show=False,
            plot_cmap=['#77dd77', '#f99191'], feature_names=aliases
        )

    # Encode shap img into base64,
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight")
    shap_img = base64.b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")

    aliases_with_column_name = dict(zip(PREDICTION_COLUMNS, aliases))

    # Request response
    response = {
        "id": str(uuid.uuid4()),
        "shap-img": shap_img,
        "feature_aliases": aliases_with_column_name
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)