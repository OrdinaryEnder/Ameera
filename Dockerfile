FROM ubuntu:latest
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && apt-get install python3.10 libsodium-dev libffi-dev python3-pip git -y 
RUN echo "Your need to edit .env before running"
RUN pip3 install -r requirements.txt 
CMD python lmao.py

