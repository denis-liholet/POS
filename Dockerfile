FROM python:3.8-slim-buster
WORKDIR /POS
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD set FLASK_APP=run.py
CMD flask run --host=0.0.0.0 --port=$PORT