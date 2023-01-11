import pickle

import pandas as pd
import wandb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import Normalizer



class RF:
    @staticmethod
    def train(base):
        base_config = base.get_config()
        x_train, x_test, y_train, y_test = base.split_data()

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

        wandb.agent(base_config['sweep_id'], wandb_train, project='parodontitis', count=base_config['iterations'])
