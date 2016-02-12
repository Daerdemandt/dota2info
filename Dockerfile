FROM python:3-slim

LABEL DOTA2info

RUN pip install --upgrade pip

RUN pip install beautifulsoup4
