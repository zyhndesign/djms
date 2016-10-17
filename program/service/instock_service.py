# coding:utf-8

import datetime
import sqlalchemy as sqla

from ..model import InStock, ProductSequence, Product, OutStockItem
from ..core import BaseService, db


class InStockService(BaseService):
    __model__ = InStock

    def add_in_stock(self, product_id, quantity, date_instock_string):
        product = Product.query.get_or_404(product_id)
        product_sequence = ProductSequence.query.get(product_id)
        date_instock = datetime.datetime.strptime(date_instock_string, '%Y-%m-%d')
        if product_sequence is None:
            seq_start = 0
            product_sequence = ProductSequence(id=product_id, seq=quantity)
        else:
            seq_start = product_sequence.seq
            product_sequence.seq = product_sequence.seq + quantity

        def in_stock_gen():
            i = 0
            serial_no_fmt = product.serial_number + "{seq:0>8}"
            while i < quantity:
                i += 1
                yield dict(product_id=product_id, serial_no=serial_no_fmt.format(seq=seq_start + i),
                           date_instock=date_instock)

        self.save(product_sequence)
        db.session.execute(InStock.__table__.insert().values(list(in_stock_gen())))

    def remove_in_stock(self, instock_id):
        instock = self.get_or_404(instock_id)
        self.delete(instock)

    def paginate(self, filters, offset=0, limit=10):
        s_count = sqla.select([sqla.func.count(InStock.__table__.c.id)])
        s_data = sqla.select([InStock.__table__.c.id, InStock.__table__.c.serial_no, InStock.__table__.c.date_instock,
                              Product.__table__.c.name, OutStockItem.__table__.c.serial_no])
        s_joint = sqla.join(InStock.__table__, Product.__table__,
                            InStock.__table__.c.product_id == Product.__table__.c.id). \
            outerjoin(OutStockItem.__table__, InStock.__table__.c.serial_no == OutStockItem.__table__.c.serial_no)
        if filters:
            count = db.session.execute(s_count.select_from(s_joint).where(*filters)).scalar()
            if count > 0:
                data = db.session.execute(
                    s_data.select_from(s_joint).where(*filters).
                    order_by(InStock.date_instock.desc(), InStock.serial_no.asc()).
                    offset(offset).limit(limit)).fetchall()
            else:
                data = []
        else:
            count = db.session.execute(s_count.select_from(s_joint)).scalar()
            if count > 0:
                data = db.session.execute(
                    s_data.select_from(s_joint).
                    order_by(InStock.date_instock.desc(), InStock.serial_no.asc()).
                    offset(offset).limit(limit)).fetchall()
            else:
                data = []

        if data:
            data = [dict(id=row[0], serial_no=row[1], date_instock=row[2], product_name=row[3],
                         instock=False if row[4] else True) for row in data]

        return count, data




