set -a
source .env # set environment variables
set +a

cd server
celery -A app.celery worker --loglevel=DEBUG
