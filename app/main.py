from flask import Flask
import os
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

if __name__ == '__main__':
  host = os.environ.get('IP', '0.0.0.0')
  port = int(os.environ.get('PORT', 8008))
  app.run(host=host, port=port)
  #app.run()