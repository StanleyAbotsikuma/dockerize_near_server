FROM nginx:1.19.0-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/letsencrypt/live && \
    mkdir -p /usr/share/nginx/html/.well-known/acme-challenge

VOLUME /etc/letsencrypt


RUN certbot certonly --standalone --preferred-challenges http -d 173.230.136.205