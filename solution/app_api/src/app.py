import connexion
import os

# Determine the directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create connexion app with correct spec directory
app = connexion.App(__name__, specification_dir=BASE_DIR)

# Load the OpenAPI file using absolute path
app.add_api(os.path.join(BASE_DIR, "openapi.yaml"))

# WSGI app for gunicorn
application = app.app
