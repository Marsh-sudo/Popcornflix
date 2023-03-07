FROM python:3.10

#means Python will not try to write .pyc files
ENV PYTHONDONTWRIEBYTECODE 1
#ensures our console output is not buffered by Docker 
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
# RUN apt-get update \
#     && apt-get install postgresql-dev gcc python3-dev musl-dev

WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt

EXPOSE 8000

# runs the production server
ENTRYPOINT ["python3"]
CMD ["manage.py","runserver", "0.0.0.0:8000"]
