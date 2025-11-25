from flask import Flask
from flask import render_template
from flask import request
import requests
import os

# Get the base directory (where app.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine template and static folders
# If templates/ and static/ are in parent directory, use ../ 
# Otherwise, look in same directory
if os.path.exists(os.path.join(BASE_DIR, '../templates')):
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, '../templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, '../static')
else:
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

# Upload folder inside static
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Use environment variable for API URL, fallback to localhost for local dev
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:8080')


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
            url = f'{API_BASE_URL}/models/irisClassifier'
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
                prediction = 'Error: ' + response.content.decode('utf-8')

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
        file = request.files['image']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        #Call the API to get the prediction with a PUT request
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        url = f'{API_BASE_URL}/models/shapesClassifier'
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.put(url, files=files)

        if response.status_code == 200:
            prediction = response.json().get('prediction')
        else:
            prediction = 'Error: ' + response.content.decode('utf-8')

        return render_template('shapesClassifier_prediction.html',
                               file_name=file.filename,
                               prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))