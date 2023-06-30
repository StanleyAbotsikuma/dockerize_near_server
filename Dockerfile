FROM python:3.10.5
RUN  apt-get -y upgrade
RUN apt-get install build-essential libffi-dev
RUN pip install -- pip


COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY ./nears_server /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh","/entrypoint.sh"]