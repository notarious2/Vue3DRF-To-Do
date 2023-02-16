FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD requirements.dev.txt /code/

# to fix issue with ruamel.yaml
RUN apk add --no-cache gcc musl-dev python3-dev

RUN pip install -r requirements.dev.txt

ADD . /code/