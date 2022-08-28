FROM python:3

RUN pip install flask
RUN mkdir ./stuff
ADD app ./app

ENTRYPOINT [ "sh", "-c" ]
CMD ["flask run --host=0.0.0.0"]