# ---------------------------------
# Krokante Krab 🦀 - 2022
#              by Tim van den Enden
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
    "temperature": {"min": 0, "max": 100},
    # "energy": {"min": 0, "max": 10000},
    "flow": {"min": 0, "max": 10},
    "duration": {"min": 0, "max": 10000}
}


# This method is used for loading the needed data.
def load_data():
    # Fetch data from csv file.
    data = pd.read_csv('./data/water-usages.csv', sep=";")

    # Only take the needed column(s)
    # df = data[['volume', 'temperature', 'energy', 'flow', 'duration']]
    df = data[['volume', 'temperature', 'flow', 'duration']]

    # Creating train and test sets
    train_dataset = df.sample(frac=0.7, random_state=0)
    test_dataset = df.drop(train_dataset.index)

    # Separate the value that we want to predict (label)
    train_features = train_dataset.copy()
    test_features = test_dataset.copy()

    train_labels = train_features.pop('volume')
    test_labels = test_features.pop('volume')

    return (train_labels, train_features), (test_labels, test_features)


# The setup method is used for setting everything up that we need to work with
def setup():
    # Load neural network
    # _model = load_model("./exported-h5/model_20220930085928.h5")
    _model = load_model("./exported-h5/model_20221013182825.h5")

    # Load training data
    (_, train_features), _ = load_data()

    # Load SHAP (Explain ability AI)
    _shap_explainer = shap.KernelExplainer(_model, train_features[:100])

    return _model, _shap_explainer


(model, shap_explainer) = setup()


@app.route('/', methods=['GET'])
def root():
    response = {
        "author": "Tim van den Enden",
        "description": "API for AquaPredict",
        "version": "1.1.0"
    }
    return jsonify(response)


@app.route('/api/predict/water-usage-shower', methods=['POST'])
def predict():
    content = request.json
    errors = []

    # Check for valid input fields
    for name in content:
        if name in EXPECTED:
            expected_min = EXPECTED[name]['min']
            expected_max = EXPECTED[name]['max']
            value = float(content[name])
            if value < expected_min or value > expected_max:
                errors.append(
                    f"Out of bounds: {name}, has value of: {value}, but should be between {expected_min} and {expected_max}."
                )
        else:
            errors.append(f"Unexpected field: {name}.")

    # Check for missing input fields
    for name in EXPECTED:
        if name not in content:
            errors.append(f"Missing value: {name}.")

    if len(errors) < 1:
        # Predict
        # x = np.zeros((1, 4))
        x = np.zeros((1, 3))

        # x[0, 0] = content['temperature']
        # x[0, 1] = content['energy']
        # x[0, 2] = content['flow']
        # x[0, 3] = content['duration']

        x[0, 0] = content['temperature']
        x[0, 1] = content['flow']
        x[0, 2] = content['duration']

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
            # feature_names=['Temperature', 'Energy', 'Flow', 'Duration'],
            feature_names=['Temperature', 'Flow', 'Duration'],
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