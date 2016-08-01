# /usr/bin/env python

# SCRIPT NAME  : Flask_REST
# DESCRIPTION  : Simple RESTFUL EXAMPLE.
# AUTHOR       : kashyap raval (kashyap32raval@gmail.com)

from flask import Flask
import models
from courses import courses_api
from reviews import reviews_api
app=Flask(__name__)
app.register_blueprint(courses_api)
app.register_blueprint(reviews_api)

DEBUG=True
@app.route('/')
def home():
    return "HELLO"
if __name__ == '__main__':
    models.init()
    app.run(debug=True)
