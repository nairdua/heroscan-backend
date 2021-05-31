from flask import *
from predict import *
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    return 'Prediction URL'
