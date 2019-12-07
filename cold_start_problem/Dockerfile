FROM ubuntu:18.04


RUN apt-get update && \
    apt-get install -y curl nano python3-pip python3.6 python3.6-dev && \
    update-alternatives --install /usr/bin/python3 python3.6 /usr/bin/python3.6 0 && \
    pip3 install pipenv

ENV \
    # Настройка pipenv
    PIPENV_VENV_IN_PROJECT=1 \
    PIPENV_CACHE_DIR=/srv/cold_start_model/.cache/pipenv \
    PIP_CACHE_DIR=/srv/cold_start_model/.cache/pip \
    PIPENV_TIMEOUT=9000 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

WORKDIR "/srv/cold_start_model"

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
