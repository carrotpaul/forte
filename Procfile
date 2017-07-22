web: FLASK_APP=server/routes.py flask run
worker: celery -A worker worker --workdir=server/ --loglevel=info
