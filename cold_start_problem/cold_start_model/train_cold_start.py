import pickle as pkl
import logging

import numpy as np
from cold_content_model import ColdContentModel, seed_everything
from sklearn.feature_extraction.text import TfidfVectorizer


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    with open('/srv/data/cold_items.pkl', 'rb') as f:
        cold_items = pkl.load(f)
        logging.info('Загружаем датасет с тэгами')
        with open('/srv/data/tag_dataset.pkl', 'rb') as f:
            dataset = pkl.load(f)
            cold_item_features = []
            for item in cold_items:
                cold_item_features.append(dataset[item])
        target = np.load('/srv/data/fair_als_factors.npy')
        logging.info('Загрузили фичи ALS в количестве %d размерности %d' % target.shape)
        tags_dataset = []
        for i in range(target.shape[0]):
            tags_dataset.append(dataset[i])

    logging.info('Кодируем фичи при помощи TFIDF')
    tfidf_model = TfidfVectorizer(**{'norm': 'l2', 'min_df': 0, 'binary': True, 'use_idf': True, 'smooth_idf': False})
    x_train = tfidf_model.fit_transform(tags_dataset)

    logging.info('Обучаем модель холодного старта')
    seed_everything(42)
    cold_content_model = ColdContentModel(
        [x_train.shape[1], target.shape[1]],
        **{'n_epochs': 5, 'batch_size': 64, 'learning_rate': 1e-5, 'decay': 1e-05}
    )
    cold_content_model.fit(x_train, target)
    predicted = cold_content_model.model.predict(tfidf_model.transform(cold_item_features))
    nn_trained_factors_filename = '/srv/data/trained_als_factors.npy'
    np.save(nn_trained_factors_filename, predicted)
    logging.info(
        'Предсказали ALS-факторы холодного контента в количестве %d размерности %d в %s' %
        (predicted.shape + (nn_trained_factors_filename,))
    )
