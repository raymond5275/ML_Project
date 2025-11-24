import connexion
from flask import jsonify

# Create Connexion app (OpenAPI)
app = connexion.App(__name__, specification_dir='.')

import os
print("CURRENT WORKING DIR:", os.getcwd())
print("FILES IN CWD:", os.listdir("."))
print("FILES NEXT TO app.py:", os.listdir(os.path.dirname(os.path.abspath(__file__))))

app.add_api('openapi.yaml')

# Optional home route
flask_app = app.app

@flask_app.route("/")
def home():
    return jsonify({"status": "ML API running", "endpoints": ["/models/irisClassifier", "/models/shapesClassifier"]})

# Gunicorn will load this
application = app.app
