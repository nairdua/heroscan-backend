import pickle
from PIL import Image
from mtcnn.mtcnn import MTCNN
from numpy import asarray, expand_dims
from matplotlib import pyplot
import tensorflow as tf
from tensorflow import keras

SK_MODEL_PATH = 'modelheroscan.pkl'
TF_MODEL_PATH = 'saved_model/my_model/'
LABEL_PATH = 'labelheroscan.pkl'

class Predictor:
    def extract_face(self, filename, required_size=(160, 160)):
        '''Extract a single face from input file'''
        image = Image.open(filename)
        image = image.convert('RGB')
        pixels = asarray(image)

        # detect faces
        detector = MTCNN()
        results = detector.detect_faces(pixels)

        # extract bounding box from 1st face
        x1, y1, width, height = results[0]['box']

        # bugfix
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        # extract face
        face = pixels[y1:y2, x1:x2]

        # resize pixels to model size
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        return face_array

    def get_embedding(self, model, face_pixels):
        '''Get embed for face'''
        face_pixels = face_pixels.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        samples = expand_dims(face_pixels, axis=0)
        yhat = model.predict(samples)
        return yhat[0]

    def predict(self, image):
        '''get prediction from input image'''
        image = self.extract_face(image)
        tf_model = tf.keras.models.load_model(TF_MODEL_PATH)

        # put image into tensorflow model
        face_emb = self.get_embedding(tf_model, image)
        samples = expand_dims(face_emb, axis=0)

        sk_model = pickle.load(open(SK_MODEL_PATH, 'rb'))
        label = pickle.load(open(LABEL_PATH, 'rb'))

        # pipe TF result to SK model
        yhat_class = sk_model.predict(samples)

        # results
        class_index = yhat_class[0]
        predict_names = label.inverse_transform(yhat_class)
        result = predict_names[0]
        return result
