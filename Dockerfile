# Pull base image
FROM python:2.7

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

COPY . /code/
RUN pip install -r requirements.txt
CMD [ "ls", "-l"]
