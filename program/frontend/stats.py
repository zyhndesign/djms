# coding:utf-8
from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required

from ..service import statsService

bp = Blueprint("stats", __name__, url_prefix="/stats")


@bp.route("/", methods=["GET"])
@bp.route("/product", methods=["GET"])
@login_required
def mgr_product_inventory():
    return render_template("proStore.html")


@bp.route("/material", methods=["GET"])
@login_required
def mgr_material_inventory():
    return render_template("matStore.html")


@bp.route("/product/list", methods=["GET"])
@login_required
def list_product_inventory():
    sEcho = request.args.get("sEcho")
    data = statsService.product_stats()
    return jsonify(
        data=dict(success=True, sEcho=sEcho, iTotalRecords=len(data), iTotalDisplayRecords=len(data), aaData=data))


@bp.route("/material/list", methods=["GET"])
@login_required
def list_material_inventory():
    sEcho = request.args.get("sEcho")
    data = statsService.material_stats()
    return jsonify(
        data=dict(success=True, sEcho=sEcho, iTotalRecords=len(data), iTotalDisplayRecords=len(data), aaData=data))
