from flask import Flask, render_template, request
import dao

app = Flask(__name__)


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')

    products = dao.load_products(q, cate_id)
    return render_template('index.html', products=products)


@app.route('/products/<int:id>')
def details(id):
    product = dao.get_product_by_id(product_id=id)
    return render_template('product-details.html', product=product)


@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories()
    }


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
