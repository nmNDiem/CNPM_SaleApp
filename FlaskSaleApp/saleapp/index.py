import math
import re

import cloudinary.uploader
from flask import render_template, request, redirect
import dao
from saleapp import app, admin, login
from flask_login import login_user, current_user, logout_user


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')
    page = request.args.get('page')

    products = dao.load_products(q=q, cate_id=cate_id, page=page)
    pages = math.ceil(dao.count_products() / app.config['PAGE_SIZE'])

    return render_template('index.html', products=products, pages=pages)


@app.route('/products/<int:id>')
def details(id):
    product = dao.get_product_by_id(product_id=id)

    return render_template('product-details.html', product=product)


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect('/')

    err_message = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user)
            return redirect('/')
        else:
            err_message = 'Tên đăng nhập hoặc mật khẩu không đúng!'

    return render_template('login.html', err_message=err_message)


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_message = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            avatar = request.files.get('avatar')
            avatar_path = None
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

            dao.add_user(name=request.form.get('name'),
                         avatar=avatar_path,
                         username=request.form.get('username'),
                         password=password)

            return redirect('/login')
        else:
            err_message = 'Mật khẩu không khớp!'

    return render_template('register.html', err_message=err_message)


@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/')


@app.route('/admin-login', methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)

    if u:
        login_user(user=u)

    return redirect('/admin')


@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories()
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
