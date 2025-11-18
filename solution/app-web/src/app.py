from flask import Flask
from flask import render_template
from flask import request
import requests
import os

app = Flask (__name__, template_folder='../templates', static_folder='../static')

UPLOAD_FOLDER = '../static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
        return render_template('index.html')

@app.route('/irisClassifier', methods=['GET', "POST"])
def irisClassifier():
        
        if request.method == 'GET':
            
            return render_template('irisClassifier.html')
        
        elif request.method == 'POST':
               
            #Get the input data from the form
            sepal_length = float(request.form['sepal_length'])
            sepal_width = float(request.form['sepal_width'])
            petal_length = float(request.form['petal_length'])
            petal_width = float(request.form['petal_width'])

            #Call the API to get the prediction with a PUT request
            url = 'http://127.0.0.1:8080/api/models/irisClassifier'
            data = {
                  'sepal_length':sepal_length,
                  'sepal_width': sepal_width,
                  'petal_length': petal_length,
                  'petal_width': petal_width
            }
            response = requests.put(url, json=data)

            if response.status_code == 200:
                prediction = response.json()['prediction']
            else:
                prediction = 'Error' + response.content.decode('utf-8')

            return render_template('irisClassifier_prediction.html',
                                   sepal_length=sepal_length,
                                   sepal_width=sepal_width,
                                   petal_length=petal_length,
                                   petal_width=petal_width,
                                   prediction=prediction)

@app.route('/shapesClassifier', methods=['GET', 'POST'])
def shapesClassifier():
     
     if request.method == 'GET':
          
        return render_template('shapesClassifier.html')
     
     elif request.method == 'POST':

        #GET the input data from the form
        file = request.files['image']                     # changed 'images' -> 'image'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        #Call the API to get the prediction with a PUT request
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        url = 'http://127.0.0.1:8080/api/models/shapesClassifier'
        with open(image_path, 'rb') as f:                  # use context manager to auto-close
            files = {'image': f}                          # changed key to 'image'
            response = requests.put(url, files=files)

        if response.status_code == 200:
            prediction = response.json().get('prediction')
        else:
            prediction = 'Error ' + response.content.decode('utf-8')

        return render_template('shapesClassifier_prediction.html',
                               file_name=file.filename,
                               prediction=prediction)
