#!/usr/bin/env python
# poetry export
# docker build
# docker stop
# docker run(bash, background mode)
# docker cp secrets.json
# ./docker-run-secrets.py <cmd>
#   뒤에 <cmd>내용을
#
import os
import subprocess
import argparse
from pathlib import Path

HOME = str(Path.home())
CREDENTIALS = os.path.join(HOME, '.aws', 'credentials')
parser = argparse.ArgumentParser()
parser.add_argument('cmd', type=str, nargs=argparse.REMAINDER, default='')
args = parser.parse_args()
DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    # background로 실행하는 옵션 추가
    ('-d', ''),
    ('-p', '8100:8000'),
    ('--name', 'gmarket_container'),
]
DOCKER_IMAGE_TAG = 'eqfwcev123/docker-gmarket-price-checker'
subprocess.run(f'poetry export -f requirements.txt > requirements.txt', shell=True)
subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile_local .', shell=True)
subprocess.run(f'sudo docker stop gmarket_container', shell=True)
# secrets.json이 없는 상태로 docker run으로 bash를 실행 -> background로 들어감
subprocess.run('sudo docker run {options} {tag} /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)
# secrets.json을 전송
# subprocess.run('sudo docker cp secrets.json gmarket_container:/srv/gmarket_price_checker', shell=True)

# .aws/credentials 파일을 EC2 로 전달
# subprocess.run(f'scp -i {SSH_KEY} {SECRETS} {TARGET}:/tmp', ignore_error=True)
# HostOS 한테서 전달받은 .aws/credentials 파일을 EC2 --> Container로 전달
subprocess.run(f'sudo docker cp {CREDENTIALS} gmarket_container:/root/.aws', shell=True)
# collectstatic 을 subprocess.run()을 사용해서 실행
subprocess.run('docker exec gmarket_container python manage.py collectstatic --noinput', shell=True)
# bash실행
# subprocess.run('docker exec -it Aad /bin/bash', shell=True)
subprocess.run('docker exec -it gmarket_container supervisord -c /srv/gmarket_price_checker/.config/supervisord.conf -n', shell=True)