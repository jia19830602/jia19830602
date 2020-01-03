from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

main_app = Flask(__name__, static_folder='.', static_url_path='')  #
main_app.config['SQLALCHEMY_DATABASE_URI'] = ''

CORS(main_app)  # 全域跨域請求

line_db = SQLAlchemy(main_app)
# apps.debug = True

from apps import routes

