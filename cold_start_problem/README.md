# Cold start problem

Этот репозиторий - прототип решения проблемы холодного старта контента с использованием Keras

## Подготовка данных и окружения

К репозиторию приложен файл [upstart.py](upstart.py), который выполняет роль "обёртки" вокруг docker-команд

Подготовка pipenv-окружения и сборка контейнера выполняется с помощью опции `build`

```shell script
python3 upstart.py -s build
```

Время заварить чаю - сборка может занимать длительное время, т.к. устанавливается большое количество зависимостей, в т.ч. "тяжёлые" пакеты keras, tensoflow

Синтетические данные в виде pkl-йлов приложены прямо в репозиторий, в директории `./cold_start_problem/data`

* `use_item_impressions.npz` - разреженная матрица взаинмодействий пользователь-контент, на которой обучаем ALS-рекомендатель
* `tag_dataset.pkl` - файл с редакторскими тэгами (закодированы в виде индексов)
* `cold_items.pkl` - файл с индексами "холодного" контента, по которому хотим предсказывать рекдакторские тэги

## Обучение модели

Чтобы обучить ALS, получить ALS-факторы контента в директории `./cold_start_problem/data`, выполните команду

```shell script
python3 upstart.py -s pipeline
```

По файлу с тэгами `./cold_start_problem/data/tag_dataset.pkl` и `./cold_start_problem/data/fair_als_factors.npy` будет сформирован выходной файл `./cold_start_problem/data/trained_als_factors.npy` с результатом работы нейросети.

Для упрощения исследовательского анализа датасета можно использовать [jupyter notebook](cold_start_model/cold_start_example.ipynb)


Чтобы запустить ноутбук, воспользуйтесь командой `jupyter`:

```shell script
python3 upstart.py -s jupyter
```

