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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
# Solves Cross Origin Resource Sharing (CORS)
CORS(app)

# Used for validation
EXPECTED = {
  # TODO: Define constraints on data if needed
}


# This method is used for loading the needed data.
def load_data():
    # Fetch data from csv file.
    # TODO: fetch data from csv
    data = pd.read_csv('', sep=";")

    # Only take the needed column(s)
    df = data[[
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
        'HAS_PARODONTITIS',
        # 'NOICE_MODIFIED',
        # 'STUDENT_ERROR'
    ]]

    # Creating train and test sets
    train_dataset = df.sample(frac=0.7, random_state=0)
    test_dataset = df.drop(train_dataset.index)

    # Separate the value that we want to predict (label)
    train_features = train_dataset.copy()
    test_features = test_dataset.copy()

    train_labels = train_features.pop('HAS_PARODONTITIS')
    test_labels = test_features.pop('HAS_PARODONTITIS')

    return (train_labels, train_features), (test_labels, test_features)


# The setup method is used for setting everything up that we need to work with
def setup():
    # Load neural network
    # TODO: Get model from wandb or from a directory
    _model = load_model("./exported-h5/model_20221013182825.h5")

    # Load training data
    (_, train_features), _ = load_data()

    # Load SHAP (Explain ability AI)
    _shap_explainer = shap.KernelExplainer(_model, train_features[:100])

    return _model, _shap_explainer


(model, shap_explainer) = setup()

@app.route('/api/predict/parodontitis', methods=['POST'])
def predict():
    content = request.json
    errors = []

    # TODO: Validate for errors using EXPECTED constraints

    if len(errors) < 1:
        # Predict
        x = np.zeros((1, 9))

        x[0, 0] = content['TREATING_PROVIDER_DENTIST']
        x[0, 1] = content['TREATING_PROVIDER_FACULTY']
        x[0, 2] = content['TREATING_PROVIDER_STUDENT']
        x[0, 3] = content['PROCEDURE_A']
        x[0, 4] = content['PROCEDURE_B']
        x[0, 5] = content['BLEEDING_ON_PROBING']
        x[0, 6] = content['NR_OF_POCKET']
        x[0, 7] = content['NR_OF_FURCATION']
        x[0, 8] = content['NR_OF_MOBILITY']
        x[0, 9] = content['TOTAL_LOSS_OF_ATTACHMENT_LEVEL']

        # Prediction
        prediction = model.predict(x)
        volume = float(prediction[0])

        # Explanation
        shap_values = shap_explainer.shap_values(x)
        shap_plot = shap.force_plot(
            shap_explainer.expected_value,
            shap_values[0],
            x,
            matplotlib=True,
            feature_names=[],# TODO define feature names
            show=False,
            plot_cmap=['#77dd77', '#f99191']
        )

        # Encode shap img into base64,
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches="tight")
        shap_img = base64.b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")

        # Request response
        response = {
            "id": str(uuid.uuid4()),
            "volume": volume,
            "shap-img": shap_img,
            "errors": errors
        }
    else:
        # Return errors
        response = {"id": str(uuid.uuid4()), "errors": errors}

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)