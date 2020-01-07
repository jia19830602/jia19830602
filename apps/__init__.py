from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import configs

main_app = Flask(__name__, static_folder='.', static_url_path='')  #
CORS(main_app)  # 全域跨域請求

# main_app.secret_key = ''
# main_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# main_app.config['SQLALCHEMY_DATABASE_URI'] = configs.SQLALCHEMY_DATABASE_URI

# line_db = SQLAlchemy(main_app)
# main_app.debug = True

from apps import routes
