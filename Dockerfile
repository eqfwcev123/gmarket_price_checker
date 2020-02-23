FROM    python:3.7-slim

RUN     apt -y update && apt -y dist-upgrade && apt -y autoremove
RUN     apt-get install vim -y
RUN     apt -y install nginx

RUN     mkdir /root/.aws
COPY    ./requirements.txt /tmp/

RUN     pip install -r /tmp/requirements.txt

COPY    . /srv/gmarket_price_checker
WORKDIR /srv/gmarket_price_checker/app

RUN     cp /srv/gmarket_price_checker/.config/gmarket.nginx /etc/nginx/sites-enabled/

CMD     /bin/bash
