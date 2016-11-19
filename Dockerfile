FROM resin/raspberrypi3-python:3.5.1
ENV INITSYSTEM on
MAINTAINER Wachira Ndaiga
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python","manage.py"]
CMD ["runserver","-h","0.0.0.0"]