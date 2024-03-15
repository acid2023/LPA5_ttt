FROM python:3.11-slim

RUN apt-get update 
COPY requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /

COPY tic_tac_toe.py / 


CMD ["python3", "tic_tac_toe.py"]