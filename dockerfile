FROM python:3.9.16-alpine3.17

WORKDIR /usr/src/app

RUN apk add --update make cmake gcc g++ gfortran
RUN apk add --update python py-pip python-dev
RUN apk --no-cache add musl-dev linux-headers g++

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./data.py" ]