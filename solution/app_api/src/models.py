import json
from flask import Response
from flask import request
import joblib
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np


 
def irisClassifier(body):
    try:
        # Load the model
        model = joblib.load('models/iris_dtree_classifier.joblib')

        # body already contains JSON data
        features = pd.DataFrame([{
            'sepal_length': body['sepal_length'],
            'sepal_width': body['sepal_width'],
            'petal_length': body['petal_length'],
            'petal_width': body['petal_width']
        }])

        # Perform classification
        prediction = model.predict(features)

        # Return JSON response
        return Response(json.dumps({
            'prediction': str(prediction[0])
        }), status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({
            'error': str(e)
        }), status=500, mimetype='application/json')
    
    
def preprocess_image(image_path, img_size=(64,64)):

    img = load_img(image_path, target_size = img_size)
    img_array = img_to_array(img)
    img_array = img_array/255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def shapesClassifier(image=None):

    try:

        # If no image was passed in as an arg, get it from the Flask request
        if image is None:
            image = request.files.get('image')
            if image is None:
                return Response(json.dumps({'error': 'No image provided'}), status=400, mimetype='application/json')

        #Save the image to a temporary location
        image_path = f'../temp/{image.filename}'
        image.save(image_path)
        
        #Load the model
        model = load_model('models/shape_classifier_cnn.keras')

        #Preprocess the image
        image_array = preprocess_image(image_path)

        #Perform classification using the loaded model
        prediction = model.predict(image_array)
        predicted_class = np.argmax(prediction, axis=1)[0]
        label_map = {0: 'circle', 1: 'square', 2: 'star', 3:'triangle'}
        predicted_label = label_map[predicted_class]

        #Return the prediction as a JSON response
        return Response(json.dumps({'prediction': predicted_label}), status=200, mimetype='application/json')
    
    except Exception as e:

        #Handle any exceptions that occur during the process
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')