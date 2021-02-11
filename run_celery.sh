set -a
source .env # set environment variables
set +a

cd mtgscan_app
celery -A app.celery worker --loglevel=DEBUG
