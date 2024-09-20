FROM python:3.10.9-slim

RUN apt-get update && apt-get clean

COPY requirements/app.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /code /code/data /code/app
COPY src/app /code/app

WORKDIR /code/app

CMD  /usr/local/bin/python -m streamlit run main.py --theme.textColor="#544b3d" --theme.primaryColor="#D17B0F" --theme.secondaryBackgroundColor="#AEC5EB" --server.address=0.0.0.0 --server.port=8080
