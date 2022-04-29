FROM python:3

RUN pip install flask

ENTRYPOINT [ "sh", "-c" ]
CMD ["flask run"]