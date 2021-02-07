
export FLASK_ENV=development
export FLASK_APP=mtgscan_app/app.py
export SECRET_KEY=secret
set -a
source prod.env
set +a
poetry run flask run