# coding:utf-8

from sqlalchemy_utils.batch import batch_fetch

from ..model import TextileWorker
from ..core import BaseService


class TextileWorkerService(BaseService):
    __model__ = TextileWorker

    def add_worker(self, **kwargs):
        textile_worker = TextileWorker()
        textile_worker.fullname = kwargs.get('fullname')
        textile_worker.tel = kwargs.get('tel')
        textile_worker.idcard = kwargs.get('idcard')
        textile_worker.address = kwargs.get('address')
        textile_worker.manager_id = int(kwargs['manager']) if kwargs.get('manager') else None
        textile_worker.is_manager = True if kwargs.get('is_manager') == '1' else False
        textile_worker.memo = kwargs.get('memo')
        return self.save(textile_worker)

    def update_worker(self, textile_worker_id, **kwargs):
        textile_worker = self.get_or_404(textile_worker_id)
        textile_worker.fullname = kwargs.get('fullname')
        textile_worker.tel = kwargs.get('tel')
        textile_worker.idcard = kwargs.get('idcard')
        textile_worker.address = kwargs.get('address')
        textile_worker.manager_id = int(kwargs['manager']) if kwargs.get('manager') else None
        textile_worker.is_manager = True if kwargs.get('is_manager') == '1' else False
        textile_worker.memo = kwargs.get('memo')
        return self.save(textile_worker)

    def managers(self):
        return self.__model__.query.filter(TextileWorker.is_manager == True).order_by(
            TextileWorker.fullname.asc()).all()

    def paginate(self, filters=[], offset=0, limit=10):
        count, data = self.paginate_by(filters=filters, order_by=TextileWorker.id.desc(), offset=offset, limit=limit)
        if data:
            batch_fetch(data, TextileWorker.manager)
        return count, data
