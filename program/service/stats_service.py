# coding:utf-8

import sqlalchemy as sqla
from sqlalchemy import sql

from ..model import MaterialInventory
from ..core import BaseService, db


class StatsService(BaseService):
    def material_stats(self):
        materials_inventory = MaterialInventory.query.options(db.joinedload("material")).all()
        data = [
            dict(name=mat_inventory.material.name, amount_in=mat_inventory.amount, amount_out=mat_inventory.amount_out)
            for mat_inventory in materials_inventory]

        return data

    def product_stats(self):
        sql_text = sql.text("""select product_in.product_id,product.name,product_in.amount as in_amount,product_out.amount as out_amount from
          (select count(id) as amount,product_id from in_stock where in_stock.deleted=FALSE group by product_id) as product_in inner join product on product_in.product_id=product.id
          inner join
          (select count(out_stock_item.serial_no) as amount,product_id from in_stock left join out_stock_item on  out_stock_item.serial_no=in_stock.serial_no group by in_stock.product_id)
          as product_out on product.id=product_out.product_id""")
        rows = db.session.execute(sql_text).fetchall()
        data = [dict(name=row[1], amount_in=row[2], amount_out=row[3]) for row in rows]
        return data



