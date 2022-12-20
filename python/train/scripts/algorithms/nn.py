from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Input, Dense, Normalization, Dropout
from keras.optimizers import Adam, SGD
from keras.losses import SparseCategoricalCrossentropy

import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import wandb
from wandb.keras import WandbCallback

from dotenv import load_dotenv
import os


class NN:
    def __init__(self, config, random_state=1, test_size=0.3):
        # Load environment variables from .env file
        load_dotenv()
        wandb_key = os.getenv(f"WANDB_KEY_{config['user'].upper()}")

        wandb.login(key=wandb_key, relogin=True)
        sweep_id = os.getenv('NN_SWEEP_ID')

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

        normalizer = Normalization(axis=-1)
        normalizer.adapt(np.array(x_train))

        def wandb_train():
            wandb.init(resume=True)
            config = wandb.config

            batch_size = config.batch_size
            epochs = config.epochs
            learning_rate = config.learning_rate
            nodes = config.nodes
            optimizer = config.optimizer
            layers = config.layers
            dropout = config.dropout

            if config.optimizer == 'adam':
                optimizer = Adam(lr=learning_rate)
            elif config.optimizer == 'sgd':
                optimizer = SGD(lr=learning_rate)

            model = Sequential()

            model.add(Input(shape=(x_train.shape[1],)))
            model.add(normalizer)

            for i in range(layers):
                model.add(Dense(nodes, activation='relu'))
                model.add(Dropout(dropout))

            model.add(Dense(2, activation='softmax'))

            model.compile(
                optimizer=optimizer,
                loss=SparseCategoricalCrossentropy(),
                metrics=['accuracy']
            )

            model.fit(
                x_train, y_train, epochs=epochs, batch_size=batch_size,
                callbacks=[WandbCallback()], validation_data=(x_test, y_test)
            )

            model.save(f'models/{wandb.run.id}_model.h5')
            wandb.log_artifact(f'models/{wandb.run.id}_model.h5', name=f'{wandb.run.id}_model', type='model')

        wandb.agent(sweep_id, wandb_train, project='parodontitis', count=iterations)
