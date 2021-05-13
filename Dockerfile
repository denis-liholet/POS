FROM python:3.7
COPY ./pos/ /core/pos/
COPY ./requirements.txt /core/requirements.txt
WORKDIR /core/
RUN python -m pip install -U pip
RUN python -m pip install -r requirements.txt
ENV FLASK_APP=src/app.py
CMD flask run --host=0.0.0.0 --port=$PORT
