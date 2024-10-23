FROM python:3.11.1
COPY . /tests

RUN pip install -r ./tests/requirements.txt