FROM python:3-slim

RUN pip install --upgrade pip

RUN pip install beautifulsoup4

RUN pip install konf

COPY . /src

WORKDIR /src

CMD python3 main.py

