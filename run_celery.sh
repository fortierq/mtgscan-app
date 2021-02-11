set -a
source .env # set environment variables
set +a

cd src
celery -A app.celery worker --loglevel=DEBUG
