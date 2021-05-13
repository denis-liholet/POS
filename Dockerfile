FROM python:3.7
COPY ./POS/ /core/src/
COPY ./requirements.txt /core/requirements.txt
WORKDIR /core/
RUN python -m pip install -U pip
RUN python -m pip install -r requirements.txt
ENV FLASK_APP=POS/start.py
CMD flask run --host=0.0.0.0 --port=$PORT