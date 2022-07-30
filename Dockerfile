FROM ubuntu:latest
RUN apt update && apt upgrade && apt install python3.10 libsodium-dev python-nacl libffi-dev
RUN pip install -r requirements.txt 
CMD python lmao.py

