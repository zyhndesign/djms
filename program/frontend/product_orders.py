# coding:utf-8

import datetime
from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required
import sqlalchemy as sqla

from ..service import productOrderService, productService
from ..model import ProductOrder, ProductOrderItem, Product

bp = Blueprint("productOrders", __name__, url_prefix="/productorders")


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    products = productService.all()
    return render_template("orderMgr.html", products=products)


@bp.route("/create", methods=["GET"])
@login_required
def form():
    return render_template("orderUpdate.html")


@bp.route("/create", methods=["POST"])
@login_required
def create_order():
    productOrderService.add_product_order(**request.form.to_dict())
    return jsonify(data=dict(success=True))


@bp.route("/<int:product_order_id>/set-status", methods=["POST"])
@login_required
def set_order_status(product_order_id):
    status = int(request.form.get("status", "1"))
    memo = request.form.get("memo")
    productOrderService.set_product_order_status(product_order_id, status, memo)
    return jsonify(data=dict(success=True))


@bp.route("/<int:product_order_id>/add", methods=["POST"])
@login_required
def add_order_item(product_order_id):
    productOrderService.add_product_order_item(product_order_id=product_order_id, **request.form.to_dict())
    return jsonify(data=dict(success=True))


@bp.route("/<int:product_order_id>/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_order_item(product_order_id, item_id):
    productOrderService.remove_product_order_item(product_order_id, item_id)
    return jsonify(data=dict(success=True))


@bp.route("/<int:product_order_id>/items", methods=["GET"])
@login_required
def list_order_items(product_order_id):
    items = productOrderService.get_product_order_items(product_order_id)
    if items:
        items = [item.asdict(only=ProductOrderItem.__dictfields__) for item in items]
    return jsonify(data=dict(success=True, items=items))


@bp.route("/<int:product_order_id>/<int:item_id>/add_outstock", methods=["POST"])
@login_required
def order_item_add_outstock(product_order_id, item_id):
    date_outstock = datetime.datetime.strptime(request.form.get("date_outstock"), '%Y-%m-%d')
    serial_no_list = request.form.get("serial_no").replace(u"，", ",").split(",")
    invalid_serial_no, duplicate_serial_no = productOrderService. \
        add_product_order_item_outstock(product_order_id, item_id, date_outstock, serial_no_list)
    if invalid_serial_no or duplicate_serial_no:
        data = dict(success=False, invalid_serial_no=invalid_serial_no, duplicate_serial_no=duplicate_serial_no)
    else:
        data = dict(success=True)
    return jsonify(data=data)


@bp.route("/<int:product_order_id>/<int:item_id>/remove_outstock", methods=["POST"])
@login_required
def order_item_remove_outstock(product_order_id, item_id):
    serial_no = request.form.get('serial_no')
    productOrderService.remove_product_order_item_outstock(product_order_id, item_id, serial_no)
    return jsonify(data=dict(success=True))


@bp.route("/list", methods=["GET"])
@login_required
def data():
    limit = int(request.args.get("iDisplayLength", "10"))
    offset = int(request.args.get("iDisplayStart", "0"))
    sEcho = request.args.get("sEcho")
    content = request.args.get('content')
    if content:
        content = '%' + content + '%'
        filters = [sqla.or_(ProductOrder.product.has(Product.name.like(content)), ProductOrder.order_no.like(content))]
    else:
        filters = []
    count, data = productOrderService.paginate(filters=filters, offset=offset, limit=limit)
    if data:
        data = [product_order.asdict(only=ProductOrder.__dictfields__) for product_order in data]
    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))


