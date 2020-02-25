#!/usr/bin/env python

import argparse
import os
import subprocess
from pathlib import Path

HOST_IP = "13.125.247.190"
HOST_NAME = "ubuntu"
TARGET = f"{HOST_NAME}@{HOST_IP}"
HOME = str(Path.home())
SSH_KEY = os.path.join(HOME, ".ssh", "gmarket_secret.pem")
PROJECT_FILE = os.path.join(HOME, "projects", "wps12th", "gmarket_price_checker")
DOCKER_IMAGE_TAG = "eqfwcev123/docker-gmarket-price-checker"
SECRETS = os.path.join(HOME, ".aws", "credentials")

parser = argparse.ArgumentParser()
parser.add_argument("cmd", type=str, nargs=argparse.REMAINDER, default='')
args = parser.parse_args()

# docker run --options
DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    # 컨테이너를 생성하면 기본적으로 외부와 통신이 불가능한 상태이다.
    # 외부와 통신을 위해서는 Container 를 외부로 노출할 Port 를 지정해야 한다.
    ('-p', '80:80'),
    ('-p', '443:443'),
    ('--name', 'gmarket_container'),
    ('-v', '/etc/letsencrypt:/etc/letsencrypt') # 폴더를 공유하는것. 컨테이너 밖에서도 사용하게 해주는 기능
]


# Local Host 에서 실행
def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()


# EC2 에서 실행
def ssh_run(cmd, ignore_error=False):
    run(f"ssh -o StrictHostKeyChecking=no -i {SSH_KEY} {TARGET} -C {cmd}", ignore_error=ignore_error)


# requirements.txt 생성, 이미지 생성, 이미지 Docker hub에 올리기
def local_build_push():
    run(f'poetry export -f requirements.txt > requirements.txt')
    run(f'docker build -t {DOCKER_IMAGE_TAG} .')  # Host Os 에서 Docker 이미지 생성
    run(f'docker push {DOCKER_IMAGE_TAG}')  # 생성한 Docker 이미지를 Docker hub로 전달


# 서버 초기설정
def server_init():
    ssh_run(f'sudo apt update')
    ssh_run(f'sudo DEBIAN_FRONTED=noninteractive apt -y dist-upgrade -y')
    ssh_run(f'sudo apt -y install docker.io')


# 실행중인 컨테이너 stop, pull, run
def server_pull_run():
    ssh_run(f'sudo docker stop gmarket_container', ignore_error=True)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE_TAG}')  # Docker hub 에있는 Docker 이미지를 EC2 내부로 가져온다
    # 가지고온 이미지를 실행
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE_TAG
    ))


# HOST --> EC2 --> Container 로 secrets.json 전달
def copy_secrets():
    # .aws/credentials 파일을 EC2 로 전달
    run(f'scp -i {SSH_KEY} {SECRETS} {TARGET}:/tmp', ignore_error=True)
    # HostOS 한테서 전달받은 .aws/credentials 파일을 EC2 --> Container로 전달
    ssh_run(f'sudo docker cp /tmp/credentials gmarket_container:/root/.aws')


# Container 에서 runserver
# 자동 실행중인 Nginx를 끄기 - 정적파일 모아주기 - supervisord로 gunicorn 이랑 Nginx 실행
def server_cmd():
    # Nginx를 설치하고 시스템을 재부팅 하면 Nginx가 자동으로 켜진다. 그 Nginx 를 끄고 우리의 supervisord 로 다시 실행할 것이다.
    ssh_run(f'sudo docker exec gmarket_container /usr/sbin/nginx -s stop', ignore_error=True)
    ssh_run(f'sudo docker exec gmarket_container python manage.py collectstatic --noinput')
    ssh_run(f'sudo docker exec gmarket_container supervisord -c /srv/gmarket_price_checker/.config/supervisord.conf -n')
    # supervisord 실행 명령어 :: supervisord -c [.conf파일 경로] -n(no daemon을 의미)


if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_secrets()
        server_cmd()
    except subprocess.CalledProcessError as e:
        print('docker-deploy-error')
        print(' cmd: ', e.cmd)
        print(' return code: ', e.returncode)
        print(' output: ', e.output)
        print(' stdout: ', e.stdout)
        print(' stderr: ', e.stderr)
