"""
Главные URL-маршруты проекта lifteam.
v2.2
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from core.api import (
    ClientViewSet, EquipmentModelViewSet, EquipmentViewSet,
    RepairOrderViewSet, SparePartViewSet, StorageCellViewSet, StockMovementViewSet
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'equipment-models', EquipmentModelViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'repair-orders', RepairOrderViewSet)
router.register(r'parts', SparePartViewSet)
router.register(r'storage-cells', StorageCellViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
