FROM python:3.10.6
RUN  apt-get -y upgrade  && \
    apt-get install -y certbot && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -- pip


COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


COPY ./nears_server /app

WORKDIR /app

ENV PORT 8080
ENV HOST 0.0.0.0

COPY ./entrypoint.sh /
ENTRYPOINT ["sh","/entrypoint.sh"]
