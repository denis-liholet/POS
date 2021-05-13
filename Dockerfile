FROM python:3.8-slim-buster
WORKDIR /POS
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
#CMD python3 -m flask run --host=0.0.0.0 --port=$PORT
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "port=$PORT"]
#CMD python3 -m flask run --host=0.0.0.0
CMD flask run