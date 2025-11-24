import json
from flask import Response
import joblib
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from PIL import Image
import io
import os

# Base directory of THIS file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def irisClassifier(body):
    """
    Connexion automatically passes the request body as 'body' parameter
    based on x-body-name in openapi.yaml
    """
    try:
        print("⚡ irisClassifier called")
        print("Received JSON:", body)

        model_path = os.path.join(BASE_DIR, "ml_models", "iris_dtree_classifier.joblib")
        print("Model path:", model_path)

        model = joblib.load(model_path)
        print("Model loaded OK")

        features = pd.DataFrame([{
            'sepal_length': body['sepal_length'],
            'sepal_width': body['sepal_width'],
            'petal_length': body['petal_length'],
            'petal_width': body['petal_width']
        }])

        prediction = model.predict(features)
        print("Prediction:", prediction)

        return Response(
            json.dumps({"prediction": str(prediction[0])}),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        print("🔥 ERROR IN irisClassifier:", str(e))
        import traceback
        traceback.print_exc()
        return Response(json.dumps({"error": str(e)}), 500, mimetype="application/json")


def shapesClassifier(image):
    """
    Connexion automatically passes the uploaded file as 'image' parameter
    based on the parameter name in openapi.yaml
    
    The 'image' parameter is a FileStorage object from werkzeug
    """
    try:
        print("⚡ shapesClassifier called")
        print("Image received:", image)
        
        if image is None:
            return Response(
                json.dumps({'error': 'No image provided'}), 
                status=400, 
                mimetype='application/json'
            )

        # Read image bytes directly (no need to save to disk)
        img_bytes = image.read()
        print(f"Image size: {len(img_bytes)} bytes")
        
        # Open image with PIL
        img = Image.open(io.BytesIO(img_bytes))
        print(f"Image mode: {img.mode}, size: {img.size}")
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to target size
        img = img.resize((64, 64))
        
        # Convert to array and normalize
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        print(f"Image array shape: {img_array.shape}")

        # Load CNN model
        model_path = os.path.join(BASE_DIR, "ml_models", "shapes_classifier_crnn.keras")
        print("Model path:", model_path)
        
        model = load_model(model_path)
        print("Model loaded OK")

        # Predict
        prediction = model.predict(img_array)
        predicted_class = int(np.argmax(prediction))
        confidence = float(prediction[0][predicted_class])
        
        print(f"Prediction: class={predicted_class}, confidence={confidence}")

        labels = {0: "circle", 1: "square", 2: "star", 3: "triangle"}

        return Response(
            json.dumps({
                "prediction": labels.get(predicted_class, "unknown"),
                "confidence": confidence,
                "class_index": predicted_class
            }), 
            200, 
            mimetype="application/json"
        )

    except Exception as e:
        print("🔥 ERROR IN shapesClassifier:", str(e))
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'error': str(e)}),
            status=500, 
            mimetype='application/json'
        )