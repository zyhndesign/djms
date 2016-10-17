# coding:utf-8

from datetime import date
from sqlalchemy_utils.models import Timestamp

from ..core import db, Deleted


class MaterialOrder(db.Model, Timestamp, Deleted):
    __tablename__ = "material_order"
    __dictfields__ = ["id", "sp_name", "material_name", "unit", "amount_buy", "unit_price", "amount_price", "date_buy",
                      "memo"]

    id = db.Column(db.Integer(), primary_key=True)
    sp_id = db.Column(db.Integer(), db.ForeignKey("service_provider.id"))  # 所属供应商
    sp = db.relationship("ServiceProvider", uselist=False, backref=db.backref("material_orders"))
    material_id = db.Column(db.Integer(), db.ForeignKey('material.id'))  # 原材料
    material = db.relationship("Material", uselist=False, backref=db.backref("material_orders"))
    unit = db.Column(db.String(32))  # 单位
    amount_buy = db.Column(db.Numeric(precision=8, scale=2))  # 购买数量
    unit_price = db.Column(db.Numeric(precision=8, scale=2))  # 单价
    amount_price = db.Column(db.Numeric(precision=8, scale=2))  # 金额
    date_buy = db.Column(db.Date(), nullable=False)  # 进货日期
    memo = db.Column(db.String(512), nullable=Timestamp)  # 备注

    @property
    def material_name(self):
        return self.material.name

    @property
    def sp_name(self):
        return self.sp.name

    def __eq__(self, other):
        if isinstance(other, MaterialOrder) and getattr(other, 'id') == self.id:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class MaterialInventory(db.Model):
    __tablename__ = "material_inventory"
    __dictfields__ = ["material_id", "material_name", "amount", "amount_out"]

    material_id = db.Column(db.Integer(), db.ForeignKey('material.id'), primary_key=True)  # 原材料
    material = db.relationship("Material", uselist=False, backref=db.backref("inventory"))
    amount = db.Column(db.Numeric(precision=9, scale=2), default=0.0, nullable=False)  # 当前的库存量
    amount_out = db.Column(db.Numeric(precision=9, scale=2), default=0.0, nullable=False)  # 支出量
    _version_id = db.Column(db.Integer(), nullable=False)

    __mapper_args__ = {
        "version_id_col": _version_id
    }

    @property
    def material_name(self):
        return self.material.name


class Task(db.Model, Timestamp, Deleted):
    __tablename__ = "task"
    __dictfields__ = ["id", "textile_worker_fullname", "product_name", "date_started", "quantity_expected",
                      "date_expected", "memo", "finished"]

    id = db.Column(db.Integer(), primary_key=True)
    textile_worker_id = db.Column(db.Integer(), db.ForeignKey("textile_worker.id"))  # 织娘
    textile_worker = db.relationship("TextileWorker", backref=db.backref("tasks", lazy="dynamic"))
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"))  # 产品
    product = db.relationship("Product")
    date_started = db.Column(db.Date(), nullable=False)  # 任务开始日期
    quantity_expected = db.Column(db.Integer(), nullable=False)  # 预计成品数量
    date_expected = db.Column(db.Date(), nullable=False)  # 预计完成时间
    memo = db.Column(db.String(512), nullable=True)  # 备注
    finished = db.Column(db.Boolean(), default=False)  # 是否完成
    _version_id = db.Column(db.Integer(), nullable=False)

    __mapper_args__ = {
        "version_id_col": _version_id
    }

    @property
    def textile_worker_fullname(self):
        return self.textile_worker.fullname

    @property
    def product_name(self):
        return self.product.name

    def __eq__(self, other):
        if isinstance(other, Task) and getattr(other, 'id') == self.id:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class TaskMaterial(db.Model):
    __tablename__ = "task_material"
    __dictfields__ = ["id", "amount", "unit", "material_name"]

    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Numeric(precision=8, scale=2))  # 消费量
    unit = db.Column(db.String(32))  # 单位
    task_id = db.Column(db.Integer(), db.ForeignKey("task.id"))
    task = db.relationship("Task", backref=db.backref("materials"))
    material_id = db.Column(db.Integer(), db.ForeignKey('material.id'))  # 原材料
    material = db.relationship("Material")

    @property
    def material_name(self):
        return self.material.name

    def __eq__(self, other):
        if isinstance(other, TaskMaterial) and getattr(other, 'id') == self.id:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class TaskResult(db.Model, Timestamp):
    __tablename__ = "task_result"
    __dictfields__ = ["id", "date_finished", "date_finished", "quantity_qualified", "quantity_defective", "level"]

    id = db.Column(db.Integer(), primary_key=True)
    task_id = db.Column(db.Integer(), db.ForeignKey("task.id"))
    task = db.relationship("Task", backref=db.backref("result"))
    date_finished = db.Column(db.Date(), nullable=False)  # 交货时间
    quantity_qualified = db.Column(db.Integer())  # 合格数量
    quantity_defective = db.Column(db.Integer())  # 次品数量
    level = db.Column(db.String(8))  # 质量评级
    _version_id = db.Column(db.Integer(), nullable=False)

    __mapper_args__ = {
        "version_id_col": _version_id
    }

    def __eq__(self, other):
        if isinstance(other, TaskResult) and getattr(other, 'id') == self.id:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class InStock(db.Model, Timestamp, Deleted):
    __tablename__ = "in_stock"
    __dictfields__ = ["id", "product_name", "serial_no", "date_instock"]

    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"))  # 产品
    product = db.relationship("Product")
    serial_no = db.Column(db.String(32), unique=True)  # 条码
    date_instock = db.Column(db.Date())  # 入库日期

    @property
    def product_name(self):
        return self.product.name

    def __eq__(self, other):
        if isinstance(other, InStock) and getattr(other, 'serial_no') == self.serial_no:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class ProductSequence(db.Model):
    __tablename__ = "product_sequence"

    id = db.Column(db.Integer(), db.ForeignKey("product.id"), primary_key=True)
    seq = db.Column(db.Integer(), default=1)
    _version_id = db.Column(db.Integer(), nullable=False)

    __mapper_args__ = {
        "version_id_col": _version_id
    }


class ProductOrder(db.Model, Timestamp, Deleted):
    __tablename__ = "product_order"
    __dictfields__ = ["id", "order_no", "source", "date_submitted", "memo", "status"]

    id = db.Column(db.Integer(), primary_key=True)
    order_no = db.Column(db.String(32), unique=True)  # 订单号
    source = db.Column(db.String(8))  # 订单来源
    date_submitted = db.Column(db.Date(), nullable=False)  # 下单时间
    memo = db.Column(db.String(512))
    status = db.Column(db.SmallInteger(), default=0, nullable=False)  # 订单是否完成
    items = db.relationship("ProductOrderItem", order_by="asc(ProductOrderItem.product_id)", passive_deletes=True,
                            cascade="all,delete-orphan")
    _version_id = db.Column(db.Integer(), nullable=False)

    __mapper_args__ = {
        "version_id_col": _version_id
    }

    def __eq__(self, other):
        if isinstance(other, ProductOrder) and getattr(other, 'order_no') == self.order_no:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class ProductOrderItem(db.Model, Timestamp):
    __tablename__ = 'product_order_item'
    __dictfields__ = ["id", "product_id", "product_name", "quantity", "unit_price", "amount", "date_delivered",
                      "outstock_serial_no", "memo"]

    id = db.Column(db.Integer(), primary_key=True)
    product_order_id = db.Column(db.Integer(), db.ForeignKey("product_order.id", ondelete="cascade"))
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"), nullable=False)  # 产品
    product = db.relationship("Product")
    quantity = db.Column(db.Integer())  # 数量
    unit_price = db.Column(db.Numeric(precision=8, scale=2))  # 单价
    amount = db.Column(db.Numeric(precision=8, scale=2))  # 金额
    date_delivered = db.Column(db.Date(), nullable=False)
    outstock_items = db.relationship("OutStockItem", uselist=True)
    memo = db.Column(db.String(512))

    __table_args__ = (db.UniqueConstraint('product_order_id', 'product_id', name='product_order_item_uk'),)

    @property
    def product_name(self):
        return self.product.name

    @property
    def outstock_serial_no(self):
        return [outstock_item.serial_no for outstock_item in self.outstock_items]

    def __eq__(self, other):
        if isinstance(other, ProductOrderItem) and \
                (getattr(other, 'product_order_id') == self.product_order_id and
                         getattr(other, 'product_id') == self.product_id):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class OutStockItem(db.Model):
    __tablename__ = "out_stock_item"
    __dictfields__ = ["serial_no", "date_outstock"]

    product_order_item_id = db.Column(db.Integer(), db.ForeignKey("product_order_item.id", ondelete="CASCADE"),
                                      primary_key=True)
    serial_no = db.Column(db.String(32), db.ForeignKey("in_stock.serial_no", ondelete="CASCADE"), primary_key=True,
                          unique=True)
    date_outstock = db.Column(db.Date(), default=date.today(), nullable=False)

    def __eq__(self, other):
        if isinstance(other, OutStockItem) and getattr(other, 'serial_no') == self.serial_no:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)










