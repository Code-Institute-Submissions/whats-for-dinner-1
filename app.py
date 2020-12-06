#  Copyright (c) 2020. Bryan S Mullen. All rights reserved.
import os
from flask import Flask
if os.path.exists('env.py'):
    import env

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
