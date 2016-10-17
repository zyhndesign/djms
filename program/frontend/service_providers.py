# coding:utf-8

from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required

from ..service import spService, materialService
from ..model import ServiceProvider, Material
import sqlalchemy as sqla

bp = Blueprint('service_providers', __name__, url_prefix="/sp")


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    return render_template("supplierMgr.html")


@bp.route("/create", methods=['GET'])
@bp.route("/<int:sp_id>/update", methods=["GET"])
@login_required
def form(sp_id=None):
    if sp_id:
        sp = spService.get_or_404(sp_id)
    else:
        sp = {}
    materials = materialService.all()
    return render_template("supplierUpdate.html", sp=sp, materials=materials)


@bp.route("/create_or_update", methods=['POST'])
@login_required
def create_or_update():
    sp_id = request.form.get('id', None)
    materials_id = map(int, request.form.getlist("materials"))
    if sp_id:
        spService.update_sp(int(sp_id), materials_id, **request.form.to_dict())
    else:
        spService.add_sp(materials_id, **request.form.to_dict())
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
        filters = [sqla.or_(ServiceProvider.name.like(name), ServiceProvider.contact_name.like(name))]
    else:
        filters = []

    count, data = spService.paginate(filters=filters, offset=offset, limit=limit)
    if data:
        data = [sp.asdict(only=ServiceProvider.__dictfields__) for sp in data]
    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))


@bp.route("/material/<int:material_id>", methods=["GET"])
@login_required
def sp_material(material_id):
    data = spService.find_by(filters=[ServiceProvider.materials.any(Material.id == material_id)],
                             order_by=ServiceProvider.name.asc())
    if data:
        data = [sp.asdict(only=ServiceProvider.__dictfields__) for sp in data]
    return jsonify(data=dict(success=True, sp=data))


