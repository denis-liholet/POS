FROM python:3.8-slim-buster
WORKDIR /POS
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
#COPY ./POS/ /core/src/
#COPY ./requirements.txt /core/requirements.txt
#WORKDIR /core/
#RUN python -m pip install -U pip
#RUN python -m pip install -r requirements.txt
#ENV FLASK_APP=POS/start.py
#CMD flask run --host=0.0.0.0 --port=$PORT