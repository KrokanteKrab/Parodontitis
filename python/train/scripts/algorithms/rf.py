from keras.layers import Normalization

import pandas as pd
import numpy as np

import wandb
import optuna
from optuna.integration.wandb import WeightsAndBiasesCallback

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
import os


class RF:
    def __init__(self, config, random_state=1, test_size=0.3):
        # Load environment variables from .env file
        load_dotenv()
        wandb_key = os.getenv(f"WANDB_KEY_{config['user'].upper()}")

        wandb.login(key=wandb_key, relogin=True)
        sweep_id = os.getenv('RF_SWEEP_ID')

        # Load data & Field selection
        df = pd.read_csv('../data/generated/patients-v6.csv')
        x = df[[
            'AGE_RANGE_20',
            'AGE_RANGE_40',
            'AGE_RANGE_60',
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
        ]]
        y = df[[
            'HAS_PARODONTITIS'
        ]]

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

        # TODO: Normalization on RF
        # normalizer = Normalization(axis=-1)
        # normalizer.adapt(np.array(x_train))

        def wandb_train(trial):
            wandb.init(resume=True)

            params = {
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 2, 4),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 5, 10),
                "max_depth": trial.suggest_int("max_depth", None, 10, 20, 30),
                "n_estimators": trial.suggest_int("n_estimators", 10, 50, 100, 200)
            }

            clf = RandomForestClassifier(**params)
            clf.fit(x_train, y_train)
            pred = clf.predict(x_test)
            score = accuracy_score(y_test, pred)

            return score

            # # Create a Random Forest model
            # model = RandomForestClassifier()
            #
            # # Create a HyperparameterSearchCV object and use it to fit the model
            # grid_search = GridSearchCV(model, param_grid, verbose=2)
            # grid_search.fit(x_train, y_train)
            #
            # # Evaluate the model on the test set
            # accuracy = grid_search.score(x_test, y_test)
            #
            # # Log the accuracy to Wandb
            # wandb.log({'test_accuracy': accuracy})
            #
            # # Save the best model to disk
            # grid_search.best_estimator_.save(f'models/{wandb.run.id}_model.pkl')
            #
            # wandb.log_artifact(f'models/{wandb.run.id}_model.pkl', name=f'{wandb.run.id}_model', type='model')

        # wandb.agent(sweep_id, wandb_train, project='parodontitis', count=iterations)
        wandb_kwargs = {
            "project": "parodontitis"
        }
        wandbc = WeightsAndBiasesCallback(metric_name="accuracy", wandb_kwargs=wandb_kwargs)

        study = optuna.create_study(direction="maximize")
        study.optimize(wandb_train, n_trials=iterations, callbacks=[wandbc])

        print("Number of finished trials: ", len(study.trials))

        print("Best trial:")
        trial = study.best_trial

        print("  Value: ", trial.value)

        print("  Params: ")
        for key, value in trial.params.items():
            print("    {}: {}".format(key, value))
