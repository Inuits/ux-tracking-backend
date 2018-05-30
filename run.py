import logging
from logging.handlers import RotatingFileHandler

from flask_cors import CORS

from app import app

if __name__ == '__main__':
    handler = RotatingFileHandler('debug.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True)
    app.run(debug=True, ssl_context=('./cert.pem', './key.pem'))
