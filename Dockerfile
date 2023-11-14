FROM python:latest
ARG BUILD_VERSION
ENV BUILD_VERSION ${BUILD_VERSION}
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
ADD . /backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic
