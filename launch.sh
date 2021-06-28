
export FLASK_APP=mtgscan_app/app.py
set -a
source .env
set +a
poetry run flask run