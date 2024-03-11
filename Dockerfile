FROM python:3.11 AS builder
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
RUN pip install --upgrade pip
RUN pip install virtualenv && virtualenv -p python3.11 virtual
RUN /bin/bash -c "source /virtual/bin/activate"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY diploma_backend .
ADD diploma-frontend diploma-frontend
RUN pip install diploma-frontend/dist/diploma-frontend-0.6.tar.gz
RUN python manage.py migrate
RUN python manage.py loaddata myapifixtures.json
