FROM python:3.8-slim-buster
WORKDIR /POS
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
#ENV FLASK_APP=start.py
CMD flask run --host=0.0.0.0 --port=$PORT