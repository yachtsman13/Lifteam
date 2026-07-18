"""
URL-маршруты приложения core.
v2.2
"""
from django.urls import path
from . import views

urlpatterns = [
    # Аутентификация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Дашборд
    path('', views.dashboard, name='dashboard'),

    # Клиенты
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),

    # Оборудование
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
    path('equipment/models/', views.equipment_model_list, name='equipment_model_list'),
    path('equipment/models/create/', views.equipment_model_create, name='equipment_model_create'),

    # Заказы на ремонт
    path('repair-orders/', views.repair_order_list, name='repair_order_list'),
    path('repair-orders/create/', views.repair_order_create, name='repair_order_create'),
    path('repair-orders/<int:pk>/', views.repair_order_detail, name='repair_order_detail'),
    path('repair-orders/<int:pk>/edit/', views.repair_order_edit, name='repair_order_edit'),
    path('repair-orders/<int:pk>/delete/', views.repair_order_delete, name='repair_order_delete'),
    path('repair-orders/<int:pk>/add-detail/', views.repair_order_add_detail, name='repair_order_add_detail'),
    path('repair-orders/<int:pk>/change-status/', views.repair_order_change_status, name='repair_order_change_status'),

    # Детали
    path('parts/', views.part_list, name='part_list'),
    path('parts/<int:pk>/', views.part_detail, name='part_detail'),
    path('parts/create/', views.part_create, name='part_create'),
    path('parts/<int:pk>/edit/', views.part_edit, name='part_edit'),
    path('parts/<int:pk>/delete/', views.part_delete, name='part_delete'),
    path('parts/<int:pk>/stock-incoming/', views.part_stock_incoming, name='part_stock_incoming'),
    path('parts/<int:pk>/assign-cell/', views.part_assign_cell, name='part_assign_cell'),

    # Ячейки хранения
    path('storage-cells/', views.storage_cell_grid, name='storage_cell_grid'),
    path('storage-cells/move/', views.storage_cell_move, name='storage_cell_move'),
    path('storage-cells/<int:pk>/label/', views.storage_cell_label, name='storage_cell_label'),

    # Отчёты
    path('reports/', views.reports, name='reports'),
    path('reports/purchase-plan/', views.report_purchase_plan, name='report_purchase_plan'),
    path('reports/stock-movements/', views.report_stock_movements, name='report_stock_movements'),
    path('reports/debtors/', views.report_debtors, name='report_debtors'),

    # Администрирование
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin/users/<int:pk>/edit/', views.admin_user_edit, name='admin_user_edit'),
]
