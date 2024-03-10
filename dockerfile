FROM ubuntu:24.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev python3-tabulate python3-numpy python3-pandas


WORKDIR /

COPY tic_tac_toe.py /


CMD ["python3", "tic_tac_toe.py"]