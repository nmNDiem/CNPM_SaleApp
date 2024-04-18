from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from saleapp import app, db
from saleapp.models import Category, Product


class MyCategoryView(ModelView):
    column_list = ['id', 'name', 'products']


class MyProductView(ModelView):
    column_list = ['id', 'name', 'price', 'category_id']
    column_labels = {
        'id': 'Mã sản phẩm',
        'name': 'Tên sản phẩm',
        'price': 'Giá',
        'category_id': 'Loại sản phẩm'
    }
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name', 'price', 'category_id']
    can_export = True


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


admin = Admin(app, name='E-commerce Website', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê'))

