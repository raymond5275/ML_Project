import json
from flask import request, Response
import joblib
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
import os

# Base directory of THIS file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def irisClassifier(body):
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
        return Response(json.dumps({"error": str(e)}), 500, mimetype="application/json")


def shapesClassifier():
    try:
        image = request.files.get("image")
        if image is None:
            return Response(json.dumps({'error': 'No image provided'}), status=400, mimetype='application/json')

        # Save to temp folder
        image_path = os.path.join(BASE_DIR, "temp", image.filename)
        image.save(image_path)

        # Load CNN model
        model_path = os.path.join(BASE_DIR, "ml_models", "shape_classifier_cnn.keras")
        model = load_model(model_path)

        img = load_img(image_path, target_size=(64, 64))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        predicted_class = int(np.argmax(prediction))

        labels = {0: "circle", 1: "square", 2: "star", 3: "triangle"}

        return Response(json.dumps({
            "prediction": labels[predicted_class]
        }), 200, mimetype="application/json")

    except Exception as e:
        return Response(json.dumps({'error': str(e)}),
                        status=500, mimetype='application/json')
