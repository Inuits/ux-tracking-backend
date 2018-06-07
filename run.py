import logging
from logging.handlers import RotatingFileHandler

from flask_cors import CORS

from app.app import app

if __name__ == '__main__':
    CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True)
    app.run(debug=True, ssl_context=('./keys/cert.pem', './keys/key.pem'))
