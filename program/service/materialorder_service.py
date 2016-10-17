# coding:utf-8

import datetime
from sqlalchemy_utils.batch import batch_fetch
from decimal import Decimal

from ..model import MaterialOrder, MaterialInventory
from ..core import BaseService
from . import _helpers


class MaterialOrderService(BaseService):
    __model__ = MaterialOrder

    def add_material_order(self, sp_id, material_id, **kwargs):
        material_order = MaterialOrder()
        material_order.sp_id = sp_id
        material_order.material_id = material_id
        material_order.unit = kwargs.get('unit')
        material_order.amount_buy = float(kwargs['amount_buy']) if kwargs.get('amount_buy') else 0
        material_order.unit_price = float(kwargs['unit_price']) if kwargs.get('unit_price') else 0
        material_order.amount_price = float(kwargs['amount_price']) if kwargs.get('amount_price') else 0
        material_order.date_buy = datetime.datetime.strptime(kwargs.get('date_buy'), '%Y-%m-%d')
        material_order.memo = kwargs.get('memo')

        material_inventory = MaterialInventory.query.get(material_id)
        amount_buy_in_inventory_unit = _helpers.to_inventory_unit(material_order.amount_buy, material_order.unit)
        if material_inventory is None:

            material_inventory = MaterialInventory(material_id=material_order.material_id,
                                                   amount=amount_buy_in_inventory_unit, amount_out=0)

        else:
            material_inventory.amount += Decimal(str(amount_buy_in_inventory_unit))

        self.save(material_order)
        self.save(material_inventory)
        return material_order

    def remove_material_order(self, material_order_id):
        material_order = self.get_or_404(material_order_id)
        material_inventory = MaterialInventory.query.get_or_404(material_order.material_id)
        amount_buy_in_inventory_unit = _helpers.to_inventory_unit(material_order.amount_buy, material_order.unit)
        material_inventory.amount -= amount_buy_in_inventory_unit
        self.delete(material_order)
        self.save(material_inventory)

    def paginate(self, filters=[], offset=0, limit=10):
        count, data = self.paginate_by(filters=filters, order_by=MaterialOrder.date_buy.desc(), offset=offset,
                                       limit=limit)
        if data:
            batch_fetch(data, MaterialOrder.material, MaterialOrder.sp)
        return count, data


