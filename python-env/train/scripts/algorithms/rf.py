import pandas as pd
import wandb
import pickle

from sklearn.preprocessing import Normalizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
import os
import sys


class RF:
    def __init__(self, config, random_state=1, test_size=0.3):
        # Load environment variables from .env file
        load_dotenv()
        wandb_key = os.getenv(f"WANDB_KEY_{config['user'].upper()}")

        # Load data & Field selection
        csv_path = '../data/synthetic-v2/data.csv'
        if not os.path.exists(csv_path):
            sys.exit(f'[*] Could not find csv file at: {csv_path}')

        df = pd.read_csv(csv_path)
        x = df[[
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
            'TOTAL_LOSS_OF_ATTACHMENT_LEVEL',
        ]]
        y = df[[
            'HAS_PARODONTITIS'
        ]]

        wandb.login(key=wandb_key, relogin=True)
        sweep_id = os.getenv('RF_SWEEP_ID')

        self.nn_config = {
            'sweep_id': sweep_id,
            'random_state': random_state,
            'test_size': test_size,
            'iterations': config['iterations'],
            'data': {
                'x': x,
                'y': y
            }
        }

    def split_data(self):
        random_state = self.nn_config['random_state']
        test_size = self.nn_config['test_size']
        x = self.nn_config['data']['x']
        y = self.nn_config['data']['y']

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, stratify=y, random_state=random_state
        )

        return x_train, x_test, y_train, y_test

    def train(self):
        sweep_id = self.nn_config['sweep_id']
        iterations = self.nn_config['iterations']

        x_train, x_test, y_train, y_test = self.split_data()
        y_train = y_train.to_numpy().flatten()
        y_test = y_test.to_numpy().flatten()

        normalizer = Normalizer()
        normalizer.fit(x_train)
        x_train_normalized = normalizer.transform(x_train)
        x_train_normalized = pd.DataFrame(x_train_normalized, columns=x_train.columns)

        def wandb_train():
            # Initialize Wandb and set up a new run
            wandb.init(resume=True)
            config = wandb.config

            params = {
                "min_samples_leaf": int(config['min_samples_leaf']),
                "min_samples_split": int(config['min_samples_split']),
                "n_estimators": int(config['n_estimators']),
                "max_features": config['max_features'],
                "bootstrap": bool(config['bootstrap']),
                "criterion": config['criterion'],
                "n_jobs": int(config['n_jobs'])
            }

            # Define the model and the hyperparameters to tune
            model = RandomForestClassifier()
            model.set_params(**params)

            # Train the model
            model.fit(x_train_normalized, y_train)

            # Evaluate the model on the test set and log the metrics
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            wandb.log({
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
            })

            # Save the model to a file
            with open(f'models/{wandb.run.id}_model.pkl', 'wb') as f:
                pickle.dump(model, f)
            wandb.log_artifact(f'models/{wandb.run.id}_model.pkl', name=f'{wandb.run.id}_model', type='model')

        wandb.agent(sweep_id, wandb_train, project='parodontitis', count=iterations)
