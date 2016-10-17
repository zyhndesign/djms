# coding:utf-8

from ..core import db, Deleted

from sqlalchemy_utils.models import Timestamp


sp_material_table = db.Table('sp_material', db.Model.metadata,
                             db.Column('sp_id', db.Integer, db.ForeignKey('service_provider.id', ondelete="cascade"),
                                       primary_key=True),
                             db.Column('material_id', db.Integer, db.ForeignKey('material.id', ondelete="cascade"),
                                       primary_key=True)
)

product_material_table = db.Table("product_material", db.Model.metadata,
                                  db.Column('product_id', db.Integer,
                                            db.ForeignKey('product.id', ondelete="cascade"),
                                            primary_key=True),
                                  db.Column('material_id', db.Integer, db.ForeignKey('material.id', ondelete="cascade"),
                                            primary_key=True)
)


class ServiceProvider(db.Model, Timestamp, Deleted):
    __tablename__ = 'service_provider'
    __dictfields__ = ["id", "name", "contact_name", "contact_address", "contact_tel", "shop_address", "memo",
                      "materials_name"]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)  # 供应商名称
    contact_name = db.Column(db.String(64), nullable=False)  # 联系人
    contact_address = db.Column(db.String(128), nullable=False)  # 联系地址
    contact_tel = db.Column(db.String(128), nullable=False)  # 联系电话
    shop_address = db.Column(db.String(256), nullable=True)  # 淘宝店铺地址
    memo = db.Column(db.String(512))  # 备注
    materials = db.relationship('Material', secondary=sp_material_table, passive_deletes=True,
                                backref="service_providers")

    @property
    def materials_name(self):
        return [material.name for material in self.materials]

    @property
    def materials_id(self):
        return [material.id for material in self.materials]

    @materials_id.setter
    def materials_id(self, value):
        materials = Material.query.filter(Material.id.in_(value)).all()
        self.materials = materials

    def __eq__(self, other):
        if isinstance(other, ServiceProvider) and getattr(other, 'name') == self.name:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class TextileWorker(db.Model, Timestamp, Deleted):
    __tablename__ = 'textile_worker'
    __dictfields__ = ["id", "fullname", "tel", "idcard", "address", "manager_fullname", "is_manager", "memo"]

    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(32))  # 姓名
    tel = db.Column(db.String(20))  # 联系电话
    idcard = db.Column(db.String(20), unique=True, nullable=False)  # 身份证号码
    address = db.Column(db.String(128), nullable=False)  # 居住地
    manager_id = db.Column(db.Integer(), db.ForeignKey("textile_worker.id"))  # 所属管理人员ID
    manager = db.relationship('TextileWorker', remote_side=[id])  # 所属管理人员
    is_manager = db.Column(db.Boolean(), default=False, nullable=False)
    memo = db.Column(db.String(512), nullable=True)  # 备注

    @property
    def manager_fullname(self):
        return self.manager.fullname if self.manager else None

    def __eq__(self, other):
        if isinstance(other, TextileWorker) and getattr(other, 'idcard') == self.idcard:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class Material(db.Model, Timestamp, Deleted):
    __tablename__ = "material"
    __dictfields__ = ["id", 'name', 'description']

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(256), nullable=True)

    def __eq__(self, other):
        if isinstance(other, Material) and getattr(other, 'name') == self.name:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class Category(db.Model, Timestamp, Deleted):
    __tablename__ = "category"
    __dictfields__ = ["id", 'name', 'description']

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(256), nullable=True)

    def __eq__(self, other):
        if isinstance(other, Category) and getattr(other, 'name') == self.name:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class Product(db.Model, Timestamp, Deleted):
    __tablename__ = "product"
    __dictfields__ = ["id", "name", "drawing", "attachment", "man_hours", "serial_number", "price", "reed",
                      "category_name", "materials_name", "memo"]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)  # 产品名称
    drawing = db.Column(db.String(256), nullable=False)  # 产品图
    attachment = db.Column(db.String(256), nullable=False)  # 附件
    man_hours = db.Column(db.Float(), nullable=False)  # 产品工时（小时）
    serial_number = db.Column(db.String(32), nullable=False, unique=True)  # 编号
    price = db.Column(db.Numeric(precision=10, scale=2))  # 定价
    reed = db.Column(db.SmallInteger())  # 竹筘类型
    memo = db.Column(db.String(512), nullable=True)  # 备注
    category_id = db.Column(db.Integer(), db.ForeignKey("category.id"))  # 所属类别
    category = db.relationship("Category", uselist=False, backref=db.backref('products', uselist=True))
    materials = db.relationship('Material', secondary=product_material_table, passive_deletes=True)

    @property
    def category_name(self):
        return self.category.name

    @property
    def materials_name(self):
        return [material.name for material in self.materials]

    @property
    def materials_id(self):
        return [material.id for material in self.materials]

    @materials_id.setter
    def materials_id(self, value):
        materials = Material.query.filter(Material.id.in_(value)).all()
        self.materials = materials

