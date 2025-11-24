import connexion
from flask import jsonify

# Create Connexion app (OpenAPI)
app = connexion.App(__name__, specification_dir='.')
app.add_api('openapi.yaml')

# Optional home route
flask_app = app.app

@flask_app.route("/")
def home():
    return jsonify({"status": "ML API running", "endpoints": ["/models/irisClassifier", "/models/shapesClassifier"]})

# Gunicorn will load this
application = app.app
