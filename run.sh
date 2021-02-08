trap "kill 0" EXIT # to kill all subprocesses when done

set -a
source prod.env # set environment variables
set +a

$REDIS & # run Redis as message broker

# celery -A mtgscan_app.app.celery worker --loglevel=DEBUG & # run Celery task queue

poetry run flask run # run Flask
