FROM python:3.10.6
RUN  apt-get -y upgrade
RUN pip install -- pip


COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


COPY ./nears_server /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh","/entrypoint.sh"]
