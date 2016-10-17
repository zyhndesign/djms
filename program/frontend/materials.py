# coding:utf-8

from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required

from ..service import materialService
from ..model import Material

bp = Blueprint('materials', __name__, url_prefix="/materials")


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    return render_template("matMgr.html")


@bp.route("/create", methods=["POST"])
@login_required
def create():
    name = request.form.get('name')
    description = request.form.get('description')
    materialService.add_material(name, description)
    return jsonify(data=dict(success=True))


@bp.route("/list", methods=["GET"])
@login_required
def data():
    # limit = int(request.args.get("iDisplayLength", "10"))
    # offset = int(request.args.get("iDisplayStart", "0"))
    sEcho = request.args.get("sEcho")
    count, data = materialService.paginate()
    if data:
        data = [material.asdict(only=Material.__dictfields__) for material in data]

    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))







