from flask import Flask
from flask import request
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
import numpy as np

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
    print(1)
    return 'error1'
  file = request.files['file']
  if file.filename == '' or not file:
    print(2)
    return 'error2'
  #blob = request.files['file'].read()
  img = np.asarray(file.convert('RGB'))
  print('----------')
  print(img)

#   img2 = img[:, :, ::-1].copy()
#   print('----------')
#   print(img2)

  #filename = secure_filename(file.filename)
  filename = file.filename
  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  img_np = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename), -1)
  print('----------')
  print(img_np)
  age_range = 0.2
  return 'age_range: ' + str(age_range)

if __name__ == '__main__':
  host = os.environ.get('IP', '0.0.0.0')
  port = int(os.environ.get('PORT', 8008))
  app.run(host=host, port=port)
  #app.run()
