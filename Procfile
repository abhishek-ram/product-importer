release: python manage.py migrate
web: gunicorn product_importer.wsgi
worker: celery -A product_importer worker -l info
