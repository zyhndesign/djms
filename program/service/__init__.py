# coding:utf-8

from .material_service import MaterialService
from .category_service import CategoryService
from .product_service import ProductService
from .serviceprovider_service import ServiceProviderService
from .textileworker_service import TextileWorkerService
from .materialorder_service import MaterialOrderService
from .task_service import TaskService
from .instock_service import InStockService
from .productorder_service import ProductOrderService
from .stats_service import StatsService


__all__ = [
    "materialService",
    "categoryService",
    "productService",
    "spService",
    "textileWorkerService",
    "materialOrderService",
    "materialOrderService",
    "instockService",
    "taskService",
    "productOrderService",
    "statsService"
]

materialService = MaterialService()
categoryService = CategoryService()
productService = ProductService()
spService = ServiceProviderService()
textileWorkerService = TextileWorkerService()
materialOrderService = MaterialOrderService()
instockService = InStockService()
taskService = TaskService()
productOrderService = ProductOrderService()
statsService = StatsService()