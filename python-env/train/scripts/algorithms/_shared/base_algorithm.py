from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Input, Dense, Normalization, Dropout
from keras.optimizers import Adam, SGD, RMSprop
from keras.losses import SparseCategoricalCrossentropy

import pandas as pd
import numpy as np

import wandb
from wandb.keras import WandbCallback

from dotenv import load_dotenv
import os
import sys

class Init:
    def __init__(self, config, random_state=1, test_size=0.3):
        # Load environment variables from .env file
        load_dotenv()
        wandb_key = os.getenv(f"WANDB_KEY_{config['user'].upper()}")

        # Load data & Field selection
        csv_path = '../_shared/data/synthetic-v2/data.csv'
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
        sweep_id = os.getenv(f"{config['algorithm'].upper()}_SWEEP_ID")

        self.config = {
            'sweep_id': sweep_id,
            'random_state': random_state,
            'test_size': test_size,
            'iterations': config['iterations'],
            'data': {
                'x': x,
                'y': y
            }
        }