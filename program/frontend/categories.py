# coding:utf-8

from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required

from ..service import categoryService
from ..model import Category

bp = Blueprint("categories", __name__, url_prefix="/categories")


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    return render_template("proCategoryMgr.html")


@bp.route("/create", methods=["POST"])
@login_required
def create():
    name = request.form.get("name")
    description = request.form.get("description")
    categoryService.add_category(name, description)
    return jsonify(data=dict(success=True))


@bp.route("/list", methods=["GET"])
@login_required
def data():
    # limit = int(request.args.get("iDisplayLength", "10"))
    # offset = int(request.args.get("iDisplayStart", "0"))
    sEcho = request.args.get("sEcho")

    count, data = categoryService.paginate()
    if data:
        data = [category.asdict(only=Category.__dictfields__) for category in data]
    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))
