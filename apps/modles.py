# 模型( model )定義
from apps import line_db
from datetime import datetime


# class Product(line_db.Model):
#     __tablename__ = 'product'
#     pid = line_db.Column(line_db.Integer, primary_key=True)
#     name = line_db.Column(
#         line_db.String(30), unique=True, nullable=False)
#     price = line_db.Column(line_db.Integer, nullable=False)
#     img = line_db.Column(
#         line_db.String(100), unique=True, nullable=False)
#     description = line_db.Column(
#         line_db.String(255), nullable=False)
#     state = line_db.Column(
#         line_db.String(10), nullable=False)
#     insert_time = line_db.Column(line_db.DateTime, default=datetime.now)
#     update_time = line_db.Column(
#         line_db.DateTime, onupdate=datetime.now, default=datetime.now)'
