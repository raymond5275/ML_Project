import connexion
from flask import jsonify
import os

# Create Connexion app (OpenAPI)
app = connexion.App(__name__, specification_dir='.')

print("CURRENT WORKING DIR:", os.getcwd())
print("FILES IN CWD:", os.listdir("."))
print("FILES NEXT TO app.py:", os.listdir(os.path.dirname(os.path.abspath(__file__))))

# 🔥 IMPORT TEST — ADD THIS BLOCK HERE
try:
    from models import irisClassifier
    print("✔ Import OK: models.irisClassifier")
except Exception as e:
    print("🔥 Import FAILED:", e)

# Load API specification
app.add_api('openapi.yaml')

# Optional home route
flask_app = app.app

@flask_app.route("/")
def home():
    return jsonify({
        "status": "ML API running",
        "endpoints": [
            "/models/irisClassifier",
            "/models/shapesClassifier"
        ]
    })

# Gunicorn will load this
application = app.app
