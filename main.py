import os
import urllib.request
import tempfile
from pathlib import Path

from flask import *
from werkzeug.utils import secure_filename

from predict import Predictor

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 # 8 MB

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS 

@app.route('/')
def hello():
    return "Hello, world!"

@app.route('/api/predict/', methods=['POST'])
def predict():
    predictor = Predictor()
    '''Predicts which hero is in the uploaded image.'''
    if request.method == 'POST':
        # Verify file is in POST request
        if 'file' not in request.files:
            response = jsonify({'message': 'Request contains no \'file\' part.'})
            response.status_code = 400
            return response

        image = request.files['file']
        
        if image and allowed_file(image.filename):
            # Create temporary dir
            with tempfile.TemporaryDirectory(dir=UPLOAD_FOLDER) as temp_dir:
                # Make temp file for prediction
                with tempfile.TemporaryFile(dir=temp_dir) as temp_file:
                    image.save(temp_file)

                    # Prediction logic
                    result = predictor.predict(temp_file)

                # Cleanup
                # temp_file.close()

            # Return result as JSON response
            return jsonify(result)
