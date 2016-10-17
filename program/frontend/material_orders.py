# coding:utf-8


from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required
import sqlalchemy as sqla

from ..service import materialOrderService, materialService
from ..model import Material, ServiceProvider, MaterialOrder


bp = Blueprint('material_orders', __name__, url_prefix='/materialorders')


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    return render_template("matInMgr.html")


@bp.route("/create", methods=["GET"])
@login_required
def form():
    materials = materialService.all()
    return render_template("matInUpdate.html", materials=materials)


@bp.route("/create", methods=["POST"])
@login_required
def create():
    sp_id = int(request.form.get("sp"))
    material_id = int(request.form.get("material"))
    materialOrderService.add_material_order(sp_id, material_id, **request.form.to_dict())
    return jsonify(data=dict(success=True))


@bp.route("/<int:material_order_id>/delete", methods=["POST"])
@login_required
def delete(material_order_id):
    materialOrderService.remove_material_order(material_order_id)
    return jsonify(data=dict(success=True))


@bp.route("/list", methods=["GET"])
@login_required
def data():
    limit = int(request.args.get("iDisplayLength", "10"))
    offset = int(request.args.get("iDisplayStart", "0"))
    sEcho = request.args.get("sEcho")
    name = request.args.get("name")
    if name:
        name = '%' + name + '%'
        filters = [sqla.or_(MaterialOrder.sp.has(ServiceProvider.name.like(name)),
                            MaterialOrder.material.has(Material.name.like(name)))]
    else:
        filters = []

    count, data = materialOrderService.paginate(filters=filters, offset=offset, limit=limit)
    if data:
        data = [material_order.asdict(only=MaterialOrder.__dictfields__) for material_order in data]

    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))







