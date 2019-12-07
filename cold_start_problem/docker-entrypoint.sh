#!/bin/bash -e

case "$1" in
  build)
    pipenv install --deploy
    ;;
  train_als)
    pipenv run python train_als.py
    ;;
  train_cold_start)
    pipenv run python train_cold_start.py
    ;;
  jupyter)
    pipenv run jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root
    ;;
  *)
    exec "$@"
esac
