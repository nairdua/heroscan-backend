import os
import urllib.request
from pathlib import Path

from flask import *
from werkzeug.utils import secure_filename

from predict import Predictor

UPLOAD_FOLDER = '/tmp/heroscan'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 # 8 MB

 # Create temp upload dir
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS 

@app.route('/')
def hello():
    return "Hello, world!"

@app.route('/api/predict/', methods=['POST'])
def predict():
    predictor = Predictor()
    response = {}
    '''Predicts which hero is in the uploaded image.'''
    if request.method == 'POST':
        # Verify file is in POST request
        if 'file' not in request.files:
            response = jsonify({'message': 'Request contains no \'file\' part.'})
            response.status_code = 400
            return response
        image = request.files['file']
        if image and allowed_file(image.filename):
            # Make temp file for prediction
            filename = secure_filename(image.filename)
            temp_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(temp_file)

            # Prediction logic
            result = predictor.predict(image)

            # Cleanup
            os.remove(temp_file)

            # Return result as JSON response
            return jsonify(result)
