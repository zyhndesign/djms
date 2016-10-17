# coding:utf-8

from flask import Blueprint, render_template, request, jsonify
from flask_security import login_required

from ..service import textileWorkerService
from ..model import TextileWorker

bp = Blueprint("textile_workers", __name__, url_prefix="/workers")


@bp.route("/", methods=["GET"])
@login_required
def mgr():
    return render_template("zWorkerMgr.html")


@bp.route("/create", methods=["GET"])
@bp.route("/<int:worker_id>/update", methods=["GET"])
def form(worker_id=None):
    if worker_id:
        worker = textileWorkerService.get_or_404(worker_id)
    else:
        worker = {}
    managers = textileWorkerService.managers()
    return render_template("zWorkerUpdate.html", worker=worker, managers=managers)


@bp.route("/create_or_update", methods=["POST"])
@login_required
def create_or_update():
    worker_id = request.form.get('id', None)
    if worker_id:
        textileWorkerService.update_worker(int(worker_id), **request.form.to_dict())
    else:
        textileWorkerService.add_worker(**request.form.to_dict())
    return jsonify(data=dict(success=True))


@bp.route("/list", methods=["GET"])
@login_required
def data():
    limit = int(request.args.get("iDisplayLength", "10"))
    offset = int(request.args.get("iDisplayStart", "0"))
    sEcho = request.args.get("sEcho")
    fullname = request.args.get("fullname")
    if fullname:
        fullname = '%' + fullname + '%'
        filters = [TextileWorker.fullname.like(fullname)]
    else:
        filters = []
    count, data = textileWorkerService.paginate(filters=filters, offset=offset, limit=limit)
    if data:
        data = [worker.asdict(only=TextileWorker.__dictfields__) for worker in data]
    return jsonify(data=dict(success=True, sEcho=sEcho, iTotalRecords=count, iTotalDisplayRecords=count, aaData=data))

