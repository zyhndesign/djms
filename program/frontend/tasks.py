# coding:utf-8

from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required
import sqlalchemy as sqla

from ..service import taskService, productService, textileWorkerService, materialService
from ..model import Task, TextileWorker, Material, Product, TaskResult, TaskMaterial

bp = Blueprint('tasks', __name__, url_prefix="/tasks")


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    materials = materialService.get_all()
    return render_template("taskMgr.html", materials=materials)


@bp.route("/create", methods=["GET"])
@bp.route("/<int:task_id>/update", methods=["GET"])
@login_required
def form(task_id=None):
    products = productService.get_all()
    workers = textileWorkerService.get_all()
    if task_id:
        task = taskService.get_or_404(task_id)
    else:
        task = {}
    return render_template("taskUpdate.html", task=task, products=products, workers=workers)


@bp.route("/create_or_update", methods=['POST'])
@login_required
def create_or_update():
    task_id = request.form.get('id')
    textile_worker_id = int(request.form.get('worker'))
    product_id = int(request.form.get('product'))
    if task_id:
        taskService.update_task(int(task_id), textile_worker_id, product_id, **request.form.to_dict())
    else:
        taskService.add_task(textile_worker_id, product_id, **request.form.to_dict())
    return jsonify(data=dict(success=True))


@bp.route("/<int:task_id>/material", methods=['GET'])
@login_required
def list_task_material(task_id):
    task_materials = taskService.task_materials(task_id)
    if task_materials:
        task_materials = [task_material.asdict(only=TaskMaterial.__dictfields__) \
                          for task_material in task_materials]
    return jsonify(data=dict(success=True, materials=task_materials))


@bp.route("/<int:task_id>/material/add", methods=['POST'])
@login_required
def add_task_material(task_id):
    material_id = int(request.form.get("material"))
    amount = float(request.form.get("amount"))
    unit = request.form.get('unit', 'g')
    if request.form.get("recycle") == '1':
        amount = -amount
    taskService.add_task_material(task_id, material_id, amount, unit)
    return jsonify(data=dict(success=True))


@bp.route("/<int:task_id>/result", methods=['GET'])
@login_required
def get_task_result(task_id):
    task_result = taskService.task_result(task_id)
    if task_result:
        task_result = task_result.asdict(only=TaskResult.__dictfields__)
    return jsonify(data=dict(success=True, result=task_result))


@bp.route("/<int:task_id>/result/add", methods=['POST'])
@login_required
def add_task_result(task_id):
    taskService.add_task_result(task_id, **request.form.to_dict())
    return jsonify(data=dict(success=True))


@bp.route("/list", methods=["GET"])
@login_required
def data():
    limit = int(request.args.get("iDisplayLength", "10"))
    offset = int(request.args.get("iDisplayStart", "0"))
    sEcho = request.args.get("sEcho")
    content = request.args.get("content")

    if content:
        content = '%' + content + '%'
        filters = [sqla.or_(Task.product.has(Product.name.like(content)),
                            Task.textile_worker.has(TextileWorker.fullname.like(content)))]
    else:
        filters = []
    count, data = taskService.paginate(filters=filters, offset=offset, limit=limit)
    if data:
        data = [task.asdict(only=Task.__dictfields__) for task in data]
    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))





