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
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
# TODO: REMOVE DEBUG=True BEFORE PRODUCTION. ONLY ADDED AT THIS STAGE IN COMPLIANCE WITH TAUGHT MATERIAL PROVIDED BY CODE INSTITUTE