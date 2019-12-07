import implicit
import numpy as np
from scipy.sparse import load_npz

if __name__ == '__main__':
    user_item_views_coo = load_npz('/srv/data/user_item_interactions.npz')
    print('Размерность матрицы с просмотрами', user_item_views_coo.shape)

    als_params = {'factors': 40, 'regularization': 0.1, 'num_threads': 3, 'iterations': 5}
    als_model = implicit.als.AlternatingLeastSquares(**als_params)
    als_model.fit(user_item_views_coo.T)
    als_factors = als_model.item_factors

    als_factors_filename = '/srv/data/fair_als_factors.npy'
    np.save(als_factors_filename, als_factors, allow_pickle=True)
    print('Сохранили факторы контента в', als_factors_filename)
