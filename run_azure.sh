export FLASK_APP=server/app.py
gunicorn --bind=0.0.0.0 --timeout 600 --chdir server app:app