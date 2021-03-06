FROM    python:3.7-slim

# 기본설정
RUN     apt -y update && apt -y dist-upgrade && apt -y autoremove
RUN     apt-get install vim -y
RUN     apt -y install nginx

# .aws credentials 파일 전달
RUN     mkdir /root/.aws
COPY    ./requirements.txt /tmp/

# 장고 애플리케이션 내부의 requirements설치
RUN     pip install -r /tmp/requirements.txt

# 장고 프로젝트 복사 및 프로젝트 내부로 들어가기
COPY    . /srv/gmarket_price_checker
WORKDIR /srv/gmarket_price_checker/app

# sites-enabled/defualt 파일은 welcome to nginx 파일이다
RUN     rm /etc/nginx/sites-enabled/default
# nginx 설정 파일을 복사. /etc/nginx/sites-enabled 로 전달
RUN     cp /srv/gmarket_price_checker/.config/gmarket.nginx /etc/nginx/sites-enabled/

CMD     /bin/bash
