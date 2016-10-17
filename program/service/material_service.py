# coding:utf-8

from ..model import Material
from ..core import BaseService


class MaterialService(BaseService):
    __model__ = Material

    def add_material(self, name, description):
        material = Material(name=name, description=description)
        return self.save(material)

    def all(self):
        materials = self.get_all(order_by=Material.name.asc())
        return materials

    def paginate(self):
        return self.paginate_by(order_by=Material.id.desc(), offset=None, limit=None)
        # return [material.asdict(only=['name', 'description']) for material in materials]

    def __repr__(self):
        return "MaterialService"



