import connexion
from flask import jsonify
from flask_cors import CORS
import os
import sys

print("=" * 60)
print("🚀 STARTUP - ML API")
print("=" * 60)
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
print("=" * 60)

# Create Connexion app (Flask-based)
app = connexion.FlaskApp(
    __name__, 
    specification_dir='.',
    options={
        "swagger_ui": True,
        "serve_spec": True
    }
)

# Enable CORS
CORS(app.app)

# Test imports
print("\n📦 Testing imports...")
try:
    from models import irisClassifier, shapesClassifier
    print("✅ Successfully imported: irisClassifier")
    print("✅ Successfully imported: shapesClassifier")
except Exception as e:
    print(f"❌ Import FAILED: {e}")
    import traceback
    traceback.print_exc()

# Check for model files
print("\n🤖 Checking model files...")
model_files = [
    'ml_models/iris_dtree_classifier.joblib',
    'ml_models/r_shapes_classifier_crnn.keras'
]
for model_file in model_files:
    if os.path.exists(model_file):
        print(f"✅ Found: {model_file}")
    else:
        print(f"❌ Missing: {model_file}")

# Load API specification
print("\n📋 Loading OpenAPI specification...")
try:
    app.add_api(
        'openapi.yaml',
        strict_validation=True,
        validate_responses=True
    )
    print("✅ OpenAPI spec loaded successfully")
except Exception as e:
    print(f"❌ Failed to load OpenAPI spec: {e}")
    import traceback
    traceback.print_exc()
    raise

# Get Flask app
flask_app = app.app

# Print registered routes
print("\n🛣️  Registered routes:")
for rule in flask_app.url_map.iter_rules():
    methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    print(f"  [{methods:6}] {rule.rule}")
print("=" * 60)

# Home route
@flask_app.route("/")
def home():
    return jsonify({
        "status": "ML API running",
        "version": "1.0.0",
        "endpoints": [
            {
                "path": "/models/irisClassifier",
                "method": "PUT",
                "description": "Predict Iris species from measurements"
            },
            {
                "path": "/models/shapesClassifier", 
                "method": "PUT",
                "description": "Predict shape from image"
            }
        ],
        "docs": "/ui"
    })

# Health check
@flask_app.route("/health")
def health():
    model_status = {
        "iris": os.path.exists('ml_models/iris_dtree_classifier.joblib'),
        "shapes": os.path.exists('ml_models/r_shapes_classifier_crnn.keras')
    }
    return jsonify({
        "status": "healthy",
        "models": model_status,
        "all_models_ready": all(model_status.values())
    })

# Error handlers
@flask_app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Not Found",
        "message": str(e),
        "hint": "Check the endpoint path and HTTP method. Use /ui to see API docs."
    }), 404

@flask_app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal Server Error",
        "message": str(e)
    }), 500

# For Gunicorn
application = app.app

if __name__ == "__main__":
    # For local development
    app.run(host="0.0.0.0", port=8080, debug=True)