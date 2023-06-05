FROM python:3.11.2-slim-buster
WORKDIR /code

COPY requirements/base.txt requirements/base.txt
COPY requirements/prod.txt requirements/prod.txt

RUN pip install -r requirements/prod.txt

COPY . .

RUN mkdir -p ./logs

CMD ["python3", "main.py"]
