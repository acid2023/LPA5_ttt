FROM python:3.11-slim

RUN apt-get update 

RUN pip install tabulate numpy

WORKDIR /

COPY tic_tac_toe.py /


CMD ["python3", "tic_tac_toe.py"]