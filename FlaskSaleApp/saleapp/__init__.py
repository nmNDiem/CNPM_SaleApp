from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '*#&(@#())@#('
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/mobiledb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4

db = SQLAlchemy(app)

login = LoginManager(app)

cloudinary.config(cloud_name='dgcezbyyd',
                  api_key='959814221454165',
                  api_secret='SCNdzcyfAjuekjMf2GjM0QqgKvY')
