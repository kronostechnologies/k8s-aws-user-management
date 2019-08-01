FROM python:3.7.4-slim-buster
WORKDIR /code

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["/code/k8suser"]
