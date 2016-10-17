# coding:utf-8

from sqlalchemy_utils.batch import batch_fetch
from ..model import Product
from ..core import BaseService


class ProductService(BaseService):
    __model__ = Product

    def add_product(self, category_id, materials_id, **kwargs):
        product = Product()
        product.name = kwargs.get('name')
        product.drawing = kwargs.get('drawing')
        product.attachment = kwargs.get('attachment')
        product.man_hours = float(kwargs.get('man_hours'))
        product.serial_number = kwargs.get('serial_number')
        product.price = float(kwargs.get('price'))
        product.reed = int(kwargs.get('reed'))
        product.memo = kwargs.get('memo')
        product.category_id = category_id
        product.materials_id = materials_id
        return self.save(product)

    def update_product(self, product_id, category_id, materials_id, **kwargs):
        product = self.get_or_404(product_id)
        product.name = kwargs.get('name')
        product.drawing = kwargs.get('drawing')
        product.attachment = kwargs.get('attachment')
        product.man_hours = float(kwargs.get('man_hours'))
        product.serial_number = kwargs.get('serial_number')
        product.price = float(kwargs.get('price'))
        product.reed = int(kwargs.get('reed'))
        product.memo = kwargs.get('memo')
        product.category_id = category_id
        product.materials_id = [] if materials_id is None else materials_id
        return self.save(product)

    def all(self):
        products = self.get_all(order_by=Product.name.asc())
        if products:
            batch_fetch(products, Product.category, Product.materials)
        return products

        # return [product.asdict(exclude=["deleted", "created", "updated"],
        # include=["category_name", "materials_name"]) for product in products]

    def paginate(self, filters=[], offset=0, limit=10):
        count, data = self.paginate_by(filters=filters, order_by=Product.id.desc(), offset=offset, limit=limit)
        if data:
            batch_fetch(data, Product.category, Product.materials)
        return count, data


