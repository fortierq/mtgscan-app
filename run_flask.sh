set -a
source prod.env # set environment variables
set +a

redis-server # run Redis as message broker

poetry run python mtgscan_app/app.py # run Flask

redis-cli shutdown
