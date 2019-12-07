import os
import random
from typing import Tuple, List, Union

import keras.backend as K
import numpy as np
from keras import optimizers
from keras.layers import Dense
from keras.models import Sequential
from scipy.sparse import csr_matrix
from tensorflow import set_random_seed


class WeightInitializer:
    def __call__(self, shape: Tuple[int, int]) -> K.variable:
        return self.custom_normal(shape)

    @staticmethod
    def custom_normal(shape: Tuple[int, int]) -> K.variable:
        return K.variable(np.random.normal(loc=0, scale=1 / (8 * np.sqrt(shape[0])), size=shape))


class ColdContentModel:
    """Класс для предсказания ALS векторов холодного контента с помощью нейросети"""

    def __init__(self, n_neurons: List[int], n_epochs: int, batch_size: int,
                 learning_rate: float, decay: float):
        """Класс для обучения нейросети
        """
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.decay = decay
        self.model = self._get_model(n_neurons)

    def fit(
            self,
            x_train: Union[np.ndarray, csr_matrix],
            y_train: np.ndarray,
            x_test: np.ndarray = None,
            y_test: np.ndarray = None
    ) -> None:
        validation_data = None
        if x_test is not None:
            validation_data = (x_test, y_test)

        self.model.fit(x_train, y_train, epochs=self.n_epochs, batch_size=self.batch_size, validation_data=validation_data, verbose=2)

    def _get_model(self, dims: List[int]) -> Sequential:
        model = Sequential()
        model.add(
            Dense(
                units=dims[1], activation='linear', input_dim=dims[0],
                kernel_initializer=WeightInitializer.custom_normal, bias_initializer='zeros'
            )
        )
        model.compile(
            loss=lambda y_true, y_pred: K.sum(K.square(y_pred - y_true), axis=-1),
            optimizer=optimizers.Adam(lr=self.learning_rate, decay=self.decay)
        )
        return model


def seed_everything(seed: int):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    set_random_seed(seed)
