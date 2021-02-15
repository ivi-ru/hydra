FROM alpine:latest

COPY openapi /opt

WORKDIR /opt

RUN apk update && \
    apk add python3 py-pip && \
    pip3 install -r requirements.txt

ENTRYPOINT ["python3", "src/app.py"]
