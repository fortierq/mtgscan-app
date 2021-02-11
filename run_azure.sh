export FLASK_APP=mtgscan_app/app.py
gunicorn --bind=0.0.0.0 --timeout 600 --chdir mtgscan_app app:app