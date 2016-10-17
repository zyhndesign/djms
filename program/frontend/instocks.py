# coding:utf-8
from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required
import sqlalchemy as sqla

from ..service import instockService, productService
from ..model import InStock, Product, OutStockItem

bp = Blueprint("instocks", __name__, url_prefix="/instocks")


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    return render_template("proSuccInMgr.html")


@bp.route("/create", methods=["GET"])
@login_required
def form():
    products = productService.all()
    return render_template("proSuccInUpdate.html", products=products)


@bp.route("/create", methods=["POST"])
@login_required
def create():
    product_id = int(request.form.get("product"))
    quantity = int(request.form.get("quantity"))
    date_instock = request.form.get("date_instock")
    instockService.add_in_stock(product_id, quantity, date_instock)
    return jsonify(data=dict(success=True))


@bp.route("/<int:instock_id>/delete", methods=["POST"])
@login_required
def delete(instock_id):
    instockService.remove_in_stock(instock_id)
    return jsonify(data=dict(success=True))


@bp.route("/list", methods=["GET"])
@login_required
def data():
    limit = int(request.args.get("iDisplayLength", "10"))
    offset = int(request.args.get("iDisplayStart", "0"))
    sEcho = request.args.get("sEcho")
    content = request.args.get("content")
    stock_status = request.args.get('stock_status', '0')
    sql_filters = [InStock.deleted == False]
    if content:
        content = '%' + content + '%'
        sql_filters.append(sqla.or_(InStock.product.has(Product.name.like(content)),
                                    InStock.serial_no.like(content)))

    if stock_status == '1':
        sql_filters.append(OutStockItem.serial_no.isnot(None))
    elif stock_status == '2':
        sql_filters.append(OutStockItem.serial_no == None)

    if len(sql_filters) > 1:
        filters = [sqla.and_(*sql_filters)]
    else:
        filters = sql_filters

    count, data = instockService.paginate(filters=filters, offset=offset, limit=limit)
    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))


