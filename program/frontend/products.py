# coding:utf-8
from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required

from ..service import productService, categoryService, materialService
from ..model import Product

bp = Blueprint("products", __name__, url_prefix="/products")


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    return render_template("proMgr.html")


@bp.route("/create", methods=["GET"])
@bp.route("/<int:product_id>/update", methods=["GET"])
def form(product_id=None):
    if product_id:
        product = productService.get_or_404(product_id)
    else:
        product = {}
    materials = materialService.all()
    categories = categoryService.all()
    return render_template("proUpdate.html", product=product, categories=categories, materials=materials)


@bp.route("/create_or_update", methods=["POST"])
def create_or_update():
    product_id = request.form.get('id', None)
    category_id = int(request.form.get("category"))
    materials_id = map(int, request.form.getlist("_materials"))
    if product_id:
        productService.update_product(int(product_id), category_id, materials_id, **request.form.to_dict())
    else:
        productService.add_product(category_id, materials_id, **request.form.to_dict())
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
        filters = [Product.name.like(name)]
    else:
        filters = []
    count, data = productService.paginate(filters=filters, offset=offset, limit=limit)
    if data:
        data = [product.asdict(only=Product.__dictfields__) for product in data]
    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))

