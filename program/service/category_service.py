# coding:utf-8

from ..model import Category
from ..core import BaseService


class CategoryService(BaseService):
    __model__ = Category

    def add_category(self, name, description):
        category = Category(name=name, description=description)
        return self.save(category)

    def all(self):
        return self.get_all(order_by=Category.name.asc())
        # return [category.asdict(only=['name', 'description']) for category in categories]

    def paginate(self):
        return self.paginate_by(order_by=Category.id.desc(), offset=None, limit=None)
        # return [category.asdict(only=['name', 'description']) for category in catgories]

    def __repr__(self):
        return "CategoryService"