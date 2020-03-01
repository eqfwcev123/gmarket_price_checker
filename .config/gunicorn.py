daemon = False
chdir = '/srv/gmarket_price_checker/app'
bind = 'unix:/run/gmarket.sock'
accessing = '/var/log/gunicorn/gmarket-access.log'
errorlog = '/var/log/gunicorn/gmarket-error.log'
capture_output = True