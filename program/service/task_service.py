# coding:utf-8

import datetime
from sqlalchemy_utils.batch import batch_fetch
from decimal import Decimal

from ..model import Task, TaskResult, TaskMaterial, MaterialInventory
from ..core import BaseService, db, AppError
from . import _helpers


class TaskService(BaseService):
    __model__ = Task

    def add_task(self, textile_worker_id, product_id, **kwargs):
        task = Task()
        task.textile_worker_id = textile_worker_id
        task.product_id = product_id
        task.date_started = datetime.datetime.strptime(kwargs.get('date_started'), '%Y-%m-%d')
        task.date_expected = datetime.datetime.strptime(kwargs.get('date_expected'), '%Y-%m-%d')
        task.quantity_expected = int(kwargs.get("quantity_expected"))
        task.memo = kwargs.get('memo')
        self.save(task)
        return task

    def update_task(self, task_id, textile_worker_id, product_id, **kwargs):
        task = self.get_or_404(task_id)
        task.textile_worker_id = textile_worker_id
        task.product_id = product_id
        task.date_started = datetime.datetime.strptime(kwargs.get('date_started'), '%Y-%m-%d')
        task.date_expected = datetime.datetime.strptime(kwargs.get('date_expected'), '%Y-%m-%d')
        task.quantity_expected = int(kwargs.get("quantity_expected"))
        task.memo = kwargs.get('memo')
        self.save(task)
        return task

    def add_task_material(self, task_id, material_id, amount, unit):
        task_material = TaskMaterial()
        task_material.task_id = task_id
        task_material.material_id = material_id
        task_material.amount = amount
        task_material.unit = unit

        material_inventory = MaterialInventory.query.get_or_404(material_id)
        task_material_amount = Decimal(str(_helpers.to_inventory_unit(amount, unit)))

        if material_inventory.amount - material_inventory.amount_out - task_material_amount < 0:
            raise AppError('MATERIAL_NOT_ENOUGH')
        material_inventory.amount_out += task_material_amount

        self.save(task_material)
        self.save(material_inventory)

    def task_materials(self, task_id):
        task_materials = TaskMaterial.query.options(db.joinedload("material")). \
            filter(TaskMaterial.task_id == task_id).order_by(TaskMaterial.material_id.asc()).all()
        return task_materials

    def add_task_result(self, task_id, **kwargs):
        task_result = TaskResult.query.filter(TaskResult.task_id == task_id).first()
        if task_result is None:
            task_result = TaskResult()
            task_result.task_id = task_id
            task = self.get_or_404(task_id)
            task.finished = True
            self.save(task)

        task_result.date_finished = datetime.datetime.strptime(kwargs.get('date_finished'), '%Y-%m-%d')
        task_result.quantity_qualified = int(kwargs.get('quantity_qualified'))
        task_result.quantity_defective = int(kwargs.get('quantity_defective'))
        task_result.level = kwargs.get('level')
        self.save(task_result)

    def task_result(self, task_id):
        task_result = TaskResult.query.filter(TaskResult.task_id == task_id).first()
        return task_result


    def paginate(self, filters=[], offset=0, limit=10):
        count, data = self.paginate_by(filters=filters, order_by=Task.date_started.desc(), offset=offset,
                                       limit=limit)
        if data:
            batch_fetch(data, Task.textile_worker, Task.product)

        return count, data















