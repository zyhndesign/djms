# coding:utf-8

from sqlalchemy_utils.batch import batch_fetch

from ..model import ServiceProvider
from ..core import BaseService


class ServiceProviderService(BaseService):
    __model__ = ServiceProvider

    def add_sp(self, materials_id, **kwargs):
        service_provider = ServiceProvider()
        service_provider.name = kwargs.get('name')
        service_provider.contact_name = kwargs.get('contact_name')
        service_provider.contact_address = kwargs.get('contact_address')
        service_provider.contact_tel = kwargs.get('contact_tel')
        service_provider.shop_address = kwargs.get('shop_address')
        service_provider.memo = kwargs.get('memo')
        service_provider.materials_id = materials_id
        return self.save(service_provider)

    def update_sp(self, service_provider_id, materials_id, **kwargs):
        service_provider = self.get_or_404(service_provider_id)
        service_provider.name = kwargs.get('name')
        service_provider.contact_name = kwargs.get('contact_name')
        service_provider.contact_address = kwargs.get('contact_address')
        service_provider.contact_tel = kwargs.get('contact_tel')
        service_provider.shop_address = kwargs.get('shop_address')
        service_provider.memo = kwargs.get('memo')
        service_provider.materials_id = [] if materials_id is None else materials_id
        return self.save(service_provider)

    def remove_sp(self, service_provider_id):
        service_provider = self.get_or_404(service_provider_id)
        self.delete(service_provider)

    def paginate(self, filters=[], offset=0, limit=10):
        count, data = self.paginate_by(filters, order_by=ServiceProvider.id.desc(), offset=offset, limit=limit)
        if data:
            batch_fetch(data, ServiceProvider.materials)
        return count, data

    def find_by(self, filters=[], order_by=None):
        if order_by is None:
            order_by = ServiceProvider.name.asc()
        data = self.__model__.query.filter(*filters).order_by(order_by).all()
        if data:
            batch_fetch(data, ServiceProvider.materials)
        return data






