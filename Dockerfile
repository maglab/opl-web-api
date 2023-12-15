FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
ADD . /backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
