# import keras
import keras

# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# import miscellaneous modules
import cv2
import os
import numpy as np
import time

# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf

# our things we add
from flask import Flask
from flask import request
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from PIL import Image
import io

def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

# set the modified tf session as backend in keras
keras.backend.tensorflow_backend.set_session(get_session())

# loading model
model_path = os.path.join('..','..','..','..','..','..', 'data', 'converted_resnet50_pascal_50.h5')
model = models.load_model(model_path, backbone_name='resnet50')
print('loaded')
print(model.summary())
graph = tf.get_default_graph()
labels_to_names = {0: '0', 1: '1', 2: '2', 3: '3-4', 4: '5-7', 5: '8'}

# application confige
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/get_bruise_age', methods=['POST'])
def get_bruise_age():
  print('innn')
  if 'file' not in request.files:
    return 'error1'
  file = request.files['file']
  if file.filename == '' or not file:
    return 'error2'

  blob = request.files['file'].read()
  img = Image.open(io.BytesIO(blob))
  filename = secure_filename(file.filename)

  # maybe remove ?
  img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), "JPEG")

  img_np = np.asarray(img.convert('RGB'))

  print('----------')
  print('first option')
  print(img_np)
  print('----------')
  print('second option')
  image = img_np[:, :, ::-1].copy()
  print(image)
# they are not the same
  print('----------')
  image = read_image_bgr(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  print('third option')
  print(image)

  image = img_np

  # preprocess image for network
  image = preprocess_image(image)
  # process image
  start = time.time()
  with graph.as_default():
    boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
    print('----------')
    print("processing time: ", time.time() - start)
    print('----------')

    # correct for image scale
    boxes /= scale

    # visualize detections
    for box, score, label in zip(boxes[0], scores[0], labels[0]):
        print('score: ' + str(score) + 'lable: ' + str(label))
        
  age_range = 0.2
  return 'age_range: ' + str(age_range)

if __name__ == '__main__':
  host = os.environ.get('IP', '0.0.0.0')
  port = int(os.environ.get('PORT', 8008))
  app.run(host=host, port=port)
