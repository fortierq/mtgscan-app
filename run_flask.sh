trap "kill 0" EXIT # to kill all subprocesses when done

set -a
source prod.env # set environment variables
set +a

$REDIS & # run Redis as message broker

poetry run python mtgscan_app/app.py # run Flask
