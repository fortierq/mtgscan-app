set -a
source .env # set environment variables
set +a

redis-server # run Redis as message broker

python server/app.py # run Flask

redis-cli shutdown
