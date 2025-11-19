import connexion
import os

# Connexion App
app = connexion.App(__name__, specification_dir='.')
app.add_api('openapi.yaml')

# WSGI app for Gunicorn
application = app.app
