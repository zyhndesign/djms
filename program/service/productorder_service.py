# coding:utf-8

import datetime
import sqlalchemy as sqla
from sqlalchemy_utils.batch import batch_fetch
from copy import copy

from ..model import ProductOrder, ProductOrderItem, OutStockItem, InStock
from ..core import BaseService, db


class ProductOrderService(BaseService):
    __model__ = ProductOrder

    def add_product_order(self, **kwargs):
        product_order = ProductOrder()
        product_order.order_no = kwargs.get('order_no')
        product_order.source = kwargs.get('source')
        product_order.date_submitted = datetime.datetime.strptime(kwargs.get('date_submitted'), '%Y-%m-%d')
        product_order.memo = kwargs.get('memo')

        self.save(product_order)
        return product_order

    def get_product_order_items(self, product_order_id):
        product_order = self.get_or_404(product_order_id)
        return product_order.items

    def set_product_order_status(self, product_order_id, status, memo=None):
        product_order = self.get_or_404(product_order_id)
        product_order.status = status
        if memo:
            product_order.memo = memo
        if status == -1:
            product_order_item_id_subquery = db.session.query(ProductOrderItem.id).filter(
                ProductOrderItem.product_order_id == product_order_id).subquery()
            db.session.execute(OutStockItem.__table__.delete().where(
                OutStockItem.product_order_item_id.in_(product_order_item_id_subquery)))
        self.save(product_order)

    def add_product_order_item(self, product_order_id, **kwargs):
        product_order = self.get_or_404(product_order_id)
        product_order_item = ProductOrderItem()
        product_order_item.product_id = kwargs.get("product_id")
        product_order_item.quantity = kwargs.get('quantity')
        product_order_item.unit_price = float(kwargs['unit_price']) if kwargs.get('unit_price') else 0
        product_order_item.amount = float(kwargs['amount']) if kwargs.get('amount') else 0
        product_order_item.date_delivered = datetime.datetime.strptime(kwargs.get('date_delivered'), '%Y-%m-%d')
        product_order_item.memo = kwargs.get("memo")
        product_order.items.append(product_order_item)

        self.save(product_order)
        return product_order_item

    def remove_product_order_item(self, product_order_id, item_id):
        product_order_item = ProductOrderItem.query.get_or_404(item_id)
        db.session.execute(OutStockItem.__table__.delete().where(OutStockItem.product_order_item_id == item_id))
        db.session.delete(product_order_item)

    def add_product_order_item_outstock(self, product_order_id, item_id, date_outstock, serial_no_list):
        product_order = ProductOrder.query.get_or_404(product_order_id)
        product_order_item = ProductOrderItem.query.get_or_404(item_id)
        invalid_serial_no = copy(serial_no_list)
        duplicate_serial_no = []
        data = db.session.execute(
            sqla.select([InStock.serial_no]).
            where(sqla.and_(InStock.serial_no.in_(invalid_serial_no),
                            InStock.product_id == product_order_item.product_id))).fetchall()
        for row in data:
            if row[0] in invalid_serial_no:
                invalid_serial_no.remove(row[0])

        data = db.session.execute(
            sqla.select([OutStockItem.serial_no]).where(OutStockItem.serial_no.in_(serial_no_list))).fetchall()
        for row in data:
            duplicate_serial_no.append(row[0])

        if len(invalid_serial_no) == 0 and len(duplicate_serial_no) == 0:
            if product_order.status == 0:
                for serial_no in serial_no_list:
                    outstock_item = OutStockItem(product_order_item_id=item_id, serial_no=serial_no,
                                                 date_outstock=date_outstock)
                    product_order_item.outstock_items.append(outstock_item)

        return invalid_serial_no, duplicate_serial_no

    def remove_product_order_item_outstock(self, product_order_id, item_id, serial_no):
        product_order_item = ProductOrderItem.query.get_or_404(item_id)
        db.session.execute(OutStockItem.__table__.delete().
                           where(sqla.and_(OutStockItem.product_order_item_id == item_id,
                                           OutStockItem.serial_no.in_(serial_no.split(',')))))

    def paginate(self, filters=[], offset=0, limit=10):
        count, data = self.paginate_by(filters=filters,
                                       order_by=ProductOrder.date_submitted.desc(), offset=offset, limit=limit)

        return count, data










