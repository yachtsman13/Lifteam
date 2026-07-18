"""
Views для LiftTeam v2.2.
CRUD операции, дашборд, отчёты, визуальная сетка кассетниц, печать этикеток.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db import transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import (
    Client, EquipmentModel, Equipment, RepairOrder, SparePart,
    StorageCell, StockMovement, RepairOrderDetail, OrderStatusHistory, Employee
)
from .forms import (
    LoginForm, ClientForm, EquipmentModelForm, EquipmentForm,
    RepairOrderForm, RepairOrderDetailForm, SparePartForm,
    StockMovementForm, StorageCellForm, EmployeeForm, StatusChangeForm
)
from .utils import generate_barcode_image


def _send_stock_update(part):
    """Отправка обновления остатка через WebSocket."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "stock_updates",
        {
            "type": "stock_update",
            "data": {
                "part_id": part.id,
                "part_number": part.part_number,
                "name": part.name,
                "current_stock": part.current_stock,
                "min_stock": part.min_stock,
                "is_below_min": part.is_below_min_stock(),
            }
        }
    )


# ==================== АУТЕНТИФИКАЦИЯ ====================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ==================== ДАШБОРД ====================

@login_required
def dashboard(request):
    """Главная страница — статистика и алерты."""
    total_orders = RepairOrder.objects.count()
    active_orders = RepairOrder.objects.exclude(status='shipped').count()
    low_stock_parts = SparePart.objects.filter(current_stock__lt=F('min_stock'))
    low_stock_count = low_stock_parts.count()
    recent_orders = RepairOrder.objects.select_related('client', 'equipment').order_by('-date_received')[:10]

    # Статистика по статусам
    status_stats = RepairOrder.objects.values('status').annotate(count=Count('id'))
    status_stats_dict = {item['status']: item['count'] for item in status_stats}

    # Должники (не оплаченные заказы)
    debtors = RepairOrder.objects.filter(
        payment_status__in=['unpaid', 'partially_paid']
    ).select_related('client')

    context = {
        'total_orders': total_orders,
        'active_orders': active_orders,
        'low_stock_count': low_stock_count,
        'low_stock_parts': low_stock_parts[:20],
        'recent_orders': recent_orders,
        'status_stats': status_stats_dict,
        'debtors': debtors[:10],
    }
    return render(request, 'core/dashboard.html', context)


# ==================== КЛИЕНТЫ ====================

@login_required
def client_list(request):
    search = request.GET.get('q', '')
    clients = Client.objects.all()
    if search:
        clients = clients.filter(Q(name__icontains=search) | Q(inn__icontains=search))
    paginator = Paginator(clients.order_by('name'), 25)
    page = request.GET.get('page')
    return render(request, 'core/clients/list.html', {
        'clients': paginator.get_page(page),
        'search': search
    })


@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказчик добавлен')
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'core/clients/form.html', {'form': form, 'title': 'Новый заказчик'})


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказчик обновлён')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'core/clients/form.html', {'form': form, 'title': 'Редактирование заказчика', 'client': client})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Заказчик удалён')
        return redirect('client_list')
    return render(request, 'core/clients/delete.html', {'client': client})


# ==================== ОБОРУДОВАНИЕ ====================

@login_required
def equipment_list(request):
    search = request.GET.get('q', '')
    equipment = Equipment.objects.select_related('model', 'current_client')
    if search:
        equipment = equipment.filter(Q(serial_number__icontains=search) | Q(model__name__icontains=search))
    paginator = Paginator(equipment.order_by('serial_number'), 25)
    page = request.GET.get('page')
    return render(request, 'core/equipment/list.html', {
        'equipment': paginator.get_page(page),
        'search': search
    })


@login_required
def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оборудование добавлено')
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'core/equipment/form.html', {'form': form, 'title': 'Новое оборудование'})


@login_required
def equipment_edit(request, pk):
    eq = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=eq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оборудование обновлено')
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=eq)
    return render(request, 'core/equipment/form.html', {'form': form, 'title': 'Редактирование оборудования', 'equipment': eq})


@login_required
def equipment_delete(request, pk):
    eq = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        eq.delete()
        messages.success(request, 'Оборудование удалено')
        return redirect('equipment_list')
    return render(request, 'core/equipment/delete.html', {'equipment': eq})


# ==================== МОДЕЛИ ОБОРУДОВАНИЯ ====================

@login_required
def equipment_model_list(request):
    models = EquipmentModel.objects.all().order_by('name')
    return render(request, 'core/equipment/model_list.html', {'models': models})


@login_required
def equipment_model_create(request):
    if request.method == 'POST':
        form = EquipmentModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Модель добавлена')
            return redirect('equipment_model_list')
    else:
        form = EquipmentModelForm()
    return render(request, 'core/equipment/model_form.html', {'form': form})


# ==================== ЗАКАЗЫ НА РЕМОНТ ====================

@login_required
def repair_order_list(request):
    search = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    orders = RepairOrder.objects.select_related('client', 'equipment__model')
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(client__name__icontains=search) |
            Q(equipment__serial_number__icontains=search)
        )
    if status_filter:
        orders = orders.filter(status=status_filter)
    paginator = Paginator(orders.order_by('-date_received'), 25)
    page = request.GET.get('page')
    return render(request, 'core/repair_orders/list.html', {
        'orders': paginator.get_page(page),
        'search': search,
        'status_filter': status_filter,
        'status_choices': RepairOrder.STATUS_CHOICES,
    })


@login_required
def repair_order_create(request):
    if request.method == 'POST':
        form = RepairOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Заказ {order.order_number} создан')
            return redirect('repair_order_detail', pk=order.pk)
    else:
        form = RepairOrderForm()
    return render(request, 'core/repair_orders/form.html', {'form': form, 'title': 'Новый заказ на ремонт'})


@login_required
def repair_order_detail(request, pk):
    order = get_object_or_404(RepairOrder.objects.select_related('client', 'equipment__model'), pk=pk)
    details = order.details.select_related('part')
    history = order.status_history.select_related('changed_by').order_by('-changed_at')
    detail_form = RepairOrderDetailForm()
    status_form = StatusChangeForm()
    return render(request, 'core/repair_orders/detail.html', {
        'order': order,
        'details': details,
        'history': history,
        'detail_form': detail_form,
        'status_form': status_form,
    })


@login_required
def repair_order_edit(request, pk):
    order = get_object_or_404(RepairOrder, pk=pk)
    if request.method == 'POST':
        form = RepairOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ обновлён')
            return redirect('repair_order_detail', pk=order.pk)
    else:
        form = RepairOrderForm(instance=order)
    return render(request, 'core/repair_orders/form.html', {
        'form': form, 'title': f'Редактирование заказа {order.order_number}', 'order': order
    })


@login_required
@require_POST
def repair_order_add_detail(request, pk):
    """Добавление детали в заказ со списанием со склада (явная транзакция)."""
    order = get_object_or_404(RepairOrder, pk=pk)
    form = RepairOrderDetailForm(request.POST)
    if form.is_valid():
        detail = form.save(commit=False)
        detail.repair_order = order
        part = detail.part

        if part.current_stock < detail.quantity_used:
            messages.warning(request,
                f'Внимание: недостаточно {part.name} на складе! Текущий остаток: {part.current_stock}. '
                f'Будет списано с отрицательным остатком.')

        with transaction.atomic():
            detail.save()
            # Явное списание со склада
            part.current_stock -= detail.quantity_used
            part.save(update_fields=['current_stock'])
            # Создание записи движения
            StockMovement.objects.create(
                part=part,
                quantity=detail.quantity_used,
                movement_type='outgoing',
                repair_order=order,
                notes=f'Списано по заказу {order.order_number}'
            )
            # Создание записи истории статуса
            OrderStatusHistory.objects.create(
                order=order,
                status=order.status,
                changed_by=request.user,
                notes=f'Добавлена деталь {part.name} x{detail.quantity_used}'
            )

        _send_stock_update(part)
        messages.success(request, f'Деталь {part.name} добавлена в заказ')
    else:
        messages.error(request, 'Ошибка при добавлении детали')
    return redirect('repair_order_detail', pk=pk)


@login_required
@require_POST
def repair_order_change_status(request, pk):
    """Изменение статуса заказа с логированием."""
    order = get_object_or_404(RepairOrder, pk=pk)
    form = StatusChangeForm(request.POST)
    if form.is_valid():
        new_status = form.cleaned_data['new_status']
        notes = form.cleaned_data.get('notes', '')
        old_status = order.status

        if old_status == new_status:
            messages.info(request, 'Статус не изменился')
            return redirect('repair_order_detail', pk=pk)

        order.status = new_status
        if new_status == 'shipped':
            order.shipping_date = timezone.now()
        if new_status in ('ready_for_shipment', 'shipped'):
            order.date_completed = timezone.now()
        order.save()

        # Создаём новую запись истории (а не обновляем старую)
        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            changed_by=request.user,
            notes=notes or f'Статус изменён с "{dict(RepairOrder.STATUS_CHOICES).get(old_status)}"'
        )

        messages.success(request, f'Статус изменён на «{order.get_status_display()}»')
    return redirect('repair_order_detail', pk=pk)


@login_required
def repair_order_delete(request, pk):
    order = get_object_or_404(RepairOrder, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заказ удалён')
        return redirect('repair_order_list')
    return render(request, 'core/repair_orders/delete.html', {'order': order})


# ==================== ДЕТАЛИ / ЗАПЧАСТИ ====================

@login_required
def part_list(request):
    search = request.GET.get('q', '')
    component_type = request.GET.get('component_type', '')
    parts = SparePart.objects.all()
    if search:
        parts = parts.filter(
            Q(part_number__icontains=search) |
            Q(name__icontains=search) |
            Q(component_type__icontains=search) |
            Q(description__icontains=search)
        )
    if component_type:
        parts = parts.filter(component_type=component_type)

    component_types = SparePart.objects.exclude(component_type='').values_list('component_type', flat=True).distinct().order_by('component_type')

    paginator = Paginator(parts.order_by('part_number'), 25)
    page = request.GET.get('page')
    return render(request, 'core/parts/list.html', {
        'parts': paginator.get_page(page),
        'search': search,
        'component_type': component_type,
        'component_types': component_types,
    })


@login_required
def part_detail(request, pk):
    part = get_object_or_404(SparePart.objects.prefetch_related('movements'), pk=pk)
    movements = part.movements.order_by('-movement_date')[:50]
    free_cells = StorageCell.objects.filter(part__isnull=True).order_by('cabinet_number', 'row_number', 'cell_row')
    return render(request, 'core/parts/detail.html', {
        'part': part,
        'movements': movements,
        'free_cells': free_cells,
    })


@login_required
def part_create(request):
    if request.method == 'POST':
        form = SparePartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, f'Деталь {part.part_number} добавлена')
            return redirect('part_detail', pk=part.pk)
    else:
        form = SparePartForm()
    return render(request, 'core/parts/form.html', {'form': form, 'title': 'Новая деталь'})


@login_required
def part_edit(request, pk):
    part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        form = SparePartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            messages.success(request, 'Деталь обновлена')
            return redirect('part_detail', pk=part.pk)
    else:
        form = SparePartForm(instance=part)
    return render(request, 'core/parts/form.html', {'form': form, 'title': 'Редактирование детали', 'part': part})


@login_required
def part_delete(request, pk):
    part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        part.delete()
        messages.success(request, 'Деталь удалена')
        return redirect('part_list')
    return render(request, 'core/parts/delete.html', {'part': part})


@login_required
@require_POST
def part_stock_incoming(request, pk):
    """Приход детали на склад."""
    part = get_object_or_404(SparePart, pk=pk)
    form = StockMovementForm(request.POST)
    if form.is_valid():
        with transaction.atomic():
            movement = form.save(commit=False)
            movement.part = part
            movement.movement_type = 'incoming'
            part.current_stock += movement.quantity
            part.save(update_fields=['current_stock'])
            movement.save()
        _send_stock_update(part)
        messages.success(request, f'Приход +{movement.quantity} {part.name} оформлен')
    else:
        messages.error(request, 'Ошибка при оформлении прихода')
    return redirect('part_detail', pk=pk)


@login_required
@require_POST
def part_assign_cell(request, pk):
    """Назначение детали на ячейку хранения."""
    part = get_object_or_404(SparePart, pk=pk)
    cell_id = request.POST.get('cell_id')
    if cell_id:
        cell = get_object_or_404(StorageCell, pk=cell_id)
        StorageCell.objects.filter(part=part).update(part=None)
        cell.part = part
        cell.save()
        messages.success(request, f'Деталь назначена на ячейку {cell.address}')
    return redirect('part_detail', pk=pk)


# ==================== ЯЧЕЙКИ ХРАНЕНИЯ / КАССЕТНИЦЫ ====================

@login_required
def storage_cell_grid(request):
    """Визуальная сетка кассетниц."""
    cabinet = int(request.GET.get('cabinet', 1))
    selected_part_id = request.GET.get('selected_part', '')
    selected_part = None
    if selected_part_id:
        selected_part = get_object_or_404(SparePart, pk=selected_part_id)

    cells = StorageCell.objects.filter(cabinet_number=cabinet).select_related('part')
    cell_map = {}
    for cell in cells:
        cell_map[(cell.row_number, cell.cell_row)] = cell

    grid = []
    for row in range(1, 9):
        grid_row = []
        for col in range(1, 9):
            cell = cell_map.get((row, col))
            if cell:
                status = cell.get_status()
                if selected_part and cell.part == selected_part:
                    status = 'selected'
                grid_row.append({
                    'exists': True,
                    'cell': cell,
                    'status': status,
                })
            else:
                grid_row.append({'exists': False})
        grid.append(grid_row)

    parts = SparePart.objects.all().order_by('part_number')

    return render(request, 'core/storage_cells/grid.html', {
        'grid': grid,
        'cabinet': cabinet,
        'cabinet_range': range(1, 13),
        'selected_part': selected_part,
        'parts': parts,
    })


@login_required
@require_POST
def storage_cell_move(request):
    """Перемещение детали между ячейками (AJAX)."""
    from_cell_id = request.POST.get('from_cell')
    to_cell_id = request.POST.get('to_cell')
    part_id = request.POST.get('part_id')

    try:
        with transaction.atomic():
            if from_cell_id:
                from_cell = StorageCell.objects.select_for_update().get(pk=from_cell_id)
                part = from_cell.part
                from_cell.part = None
                from_cell.save()
            elif part_id:
                part = SparePart.objects.get(pk=part_id)
            else:
                return JsonResponse({'error': 'Не указана деталь'}, status=400)

            to_cell = None
            if to_cell_id:
                to_cell = StorageCell.objects.select_for_update().get(pk=to_cell_id)
                if to_cell.part is not None and to_cell.part != part:
                    return JsonResponse({'error': 'Ячейка занята'}, status=400)
                to_cell.part = part
                to_cell.save()

            if part:
                _send_stock_update(part)

            return JsonResponse({'success': True, 'message': 'Перемещение выполнено', 'address': to_cell.address if to_cell else None})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def storage_cell_label(request, pk):
    """Печать этикетки ячейки."""
    cell = get_object_or_404(StorageCell.objects.select_related('part'), pk=pk)
    barcode_img = generate_barcode_image(cell.address)
    return render(request, 'core/storage_cells/label.html', {
        'cell': cell,
        'barcode_img': barcode_img,
    })


# ==================== ОТЧЁТЫ ====================

@login_required
def reports(request):
    return render(request, 'core/reports/index.html')


@login_required
def report_purchase_plan(request):
    """План закупок — детали ниже минимального остатка."""
    parts = SparePart.objects.filter(current_stock__lt=F('min_stock')).order_by('part_number')
    return render(request, 'core/reports/purchase_plan.html', {'parts': parts})


@login_required
def report_stock_movements(request):
    """Журнал движений запчастей."""
    movements = StockMovement.objects.select_related('part', 'repair_order').order_by('-movement_date')

    part_id = request.GET.get('part')
    movement_type = request.GET.get('type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if part_id:
        movements = movements.filter(part_id=part_id)
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    if date_from:
        movements = movements.filter(movement_date__date__gte=date_from)
    if date_to:
        movements = movements.filter(movement_date__date__lte=date_to)

    paginator = Paginator(movements, 50)
    page = request.GET.get('page')

    parts_list = SparePart.objects.all().order_by('part_number')
    return render(request, 'core/reports/stock_movements.html', {
        'movements': paginator.get_page(page),
        'parts_list': parts_list,
    })


@login_required
def report_debtors(request):
    """Задолженности по заказам."""
    orders = RepairOrder.objects.filter(
        payment_status__in=['unpaid', 'partially_paid']
    ).select_related('client').order_by('-date_received')
    total_debt = orders.aggregate(total=Sum('repair_cost'))['total'] or 0
    return render(request, 'core/reports/debtors.html', {
        'orders': orders,
        'total_debt': total_debt,
    })


# ==================== АДМИНИСТРИРОВАНИЕ ====================

@login_required
def admin_users(request):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещён')
        return redirect('dashboard')
    users = Employee.objects.all().order_by('full_name')
    return render(request, 'core/admin/users.html', {'users': users})


@login_required
def admin_user_create(request):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещён')
        return redirect('dashboard')
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь создан')
            return redirect('admin_users')
    else:
        form = EmployeeForm()
    return render(request, 'core/admin/user_form.html', {'form': form, 'title': 'Новый пользователь'})


@login_required
def admin_user_edit(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещён')
        return redirect('dashboard')
    user = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь обновлён')
            return redirect('admin_users')
    else:
        form = EmployeeForm(instance=user)
    return render(request, 'core/admin/user_form.html', {'form': form, 'title': 'Редактирование пользователя', 'user_obj': user})
