from flask import redirect
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from flask_login import logout_user, current_user

from saleapp import app, db
from saleapp.models import Category, Product, UserRole, User


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyCategoryView(AuthenticatedView):
    column_list = ['id', 'name', 'products']
    column_editable_list = ['name']


class MyProductView(AuthenticatedView):
    column_list = ['id', 'name', 'price', 'category_id']
    column_labels = {
        'id': 'Mã sản phẩm',
        'name': 'Tên sản phẩm',
        'price': 'Giá',
        'category_id': 'Loại sản phẩm'
    }
    column_editable_list = ['name', 'price']
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name', 'price', 'category_id']
    can_export = True


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, name='E-commerce Website', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name="Đăng xuất"))
