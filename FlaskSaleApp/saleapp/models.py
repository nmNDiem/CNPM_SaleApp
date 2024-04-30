from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from saleapp import db, app
from flask_login import UserMixin
from enum import Enum as RoleEnum
from datetime import datetime


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100))
    avatar = Column(String(100))
    username = Column(String(50), unique=True)
    password = Column(String(50))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Float, default=0)
    image = Column(String(200),
                   default="https://cdn.tgdd.vn/Products/Images/42/251192/iphone-14-pro-max-tim-thumb-600x600.jpg")
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    details = relationship('ReceiptDetails', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class Receipt(Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(Base):
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        c1 = Category(name='Mobile')
        c2 = Category(name='Tablet')
        c3 = Category(name='Laptop')

        db.session.add_all([c1, c2, c3])
        db.session.commit()

        import json

        with open('data/products.json', encoding='utf-8') as f:
            products = json.load(f)
            for p in products:
                prod = Product(**p)
                db.session.add(prod)

        db.session.commit()

        import hashlib

        u = User(name='admin',
                 username='admin',
                 avatar='https://cdn.tgdd.vn/Products/Images/42/251192/iphone-14-pro-max-tim-thumb-600x600.jpg',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)

        u2 = User(name='Nguoi Dung',
                  avatar= 'https://cdn.tgdd.vn/Products/Images/42/251192/iphone-14-pro-max-tim-thumb-600x600.jpg',
                  username='nguoidung',
                  password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                  user_role=UserRole.USER)

        db.session.add(u2)
        db.session.commit()
