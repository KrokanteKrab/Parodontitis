from keras.models import Sequential
from keras.layers import Input, Dense, Normalization, Dropout
from keras.optimizers import Adam, SGD, RMSprop
from keras.losses import SparseCategoricalCrossentropy
import numpy as np
import wandb
from wandb.keras import WandbCallback


class NN:
    @staticmethod
    def train(base):
        base_config = base.get_config()
        x_train, x_test, y_train, y_test = base.split_data()

        normalizer = Normalization(axis=-1)
        normalizer.adapt(np.array(x_train))

        def wandb_train():
            wandb.init(resume=True)
            config = wandb.config

            batch_size = config.batch_size
            epochs = config.epochs
            learning_rate = config.learning_rate
            nodes = config.nodes
            layers = config.layers
            dropout = config.dropout

            optimizers = {
                'adam': Adam,
                'sgd': SGD,
                'rmsprop': RMSprop
            }

            optimizer = optimizers[config.optimizer](lr=learning_rate)

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

        wandb.agent(base_config['sweep_id'], wandb_train, project='parodontitis', count=base_config['iterations'])

