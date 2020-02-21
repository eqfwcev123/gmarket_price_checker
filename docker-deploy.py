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
PROJECT_FILE = os.path.join(HOME, "wps12th", "gmarket_price_checker")
DOCKER_IMAGE_TAG = "eqfwcev123/docker-gmarket-price-checker"

parser = argparse.ArgumentParser()
parser.add_argument("cmd", type=str, nargs=argparse.REMAINDER)
args = parser.parse_args()

# docker run --options
DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    ('-p', '80:8000'),
    ('-p', '443:443'),
    ('--name', 'gmarket_container'),
]

print(1)


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
    run(f'docker build -t {DOCKER_IMAGE_TAG} .')
    run(f'docker push {DOCKER_IMAGE_TAG}')


# 서버 초기설정
def server_init():
    print("server init 실행")
    ssh_run(f'sudo apt update')
    ssh_run(f'sudo DEBIAN_FRONTED=noninteractive apt -y dist-upgrade -y')
    ssh_run(f'sudo apt -y install docker.io')


# 실행중인 컨테이너 stop, pull, run
def server_pull_run():
    ssh_run(f'sudo docker stop gmarket_container', ignore_error=True)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE_TAG}')
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE_TAG
    ))


# HOST --> EC2 --> Container 로 secrets.json 전달
def copy_secrets():
    pass


# Container 에서 runserver
def server_cmd():
    pass


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
