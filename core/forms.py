"""
Формы для LiftTeam v2.2.
"""
from django import forms
from django.contrib.auth import authenticate
from .models import (
    Client, EquipmentModel, Equipment, RepairOrder, RepairOrderDetail,
    SparePart, StorageCell, StockMovement, Employee
)


class LoginForm(forms.Form):
    """Кастомная форма входа по логину (username)."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин', 'autofocus': True}),
        label='Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Неверный логин или пароль')
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Аккаунт неактивен')

    def get_user(self):
        return self.user_cache


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'inn', 'kpp', 'contact_person', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название',
            'inn': 'ИНН',
            'kpp': 'КПП',
            'contact_person': 'Контактное лицо',
            'phone': 'Телефон',
            'email': 'Email',
        }


class EquipmentModelForm(forms.ModelForm):
    class Meta:
        model = EquipmentModel
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название модели',
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['model', 'serial_number', 'current_client']
        widgets = {
            'model': forms.Select(attrs={'class': 'form-select'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'current_client': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'model': 'Модель',
            'serial_number': 'Серийный номер',
            'current_client': 'Текущий заказчик',
        }


class RepairOrderForm(forms.ModelForm):
    class Meta:
        model = RepairOrder
        fields = [
            'client', 'equipment', 'initial_condition', 'fault_description',
            'seal_numbers', 'repair_cost', 'invoice_number', 'invoice_date',
            'payment_status', 'status', 'yandex_disk_folder'
        ]
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'equipment': forms.Select(attrs={'class': 'form-select'}),
            'initial_condition': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fault_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'seal_numbers': forms.TextInput(attrs={'class': 'form-control'}),
            'repair_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'yandex_disk_folder': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'client': 'Заказчик',
            'equipment': 'Оборудование',
            'initial_condition': 'Начальное состояние',
            'fault_description': 'Описание неисправности',
            'seal_numbers': 'Номера пломб',
            'repair_cost': 'Стоимость ремонта',
            'invoice_number': 'Номер счёта',
            'invoice_date': 'Дата счёта',
            'payment_status': 'Статус оплаты',
            'status': 'Статус заказа',
            'yandex_disk_folder': 'Папка на Яндекс.Диске',
        }


class RepairOrderDetailForm(forms.ModelForm):
    class Meta:
        model = RepairOrderDetail
        fields = ['part', 'quantity_used']
        widgets = {
            'part': forms.Select(attrs={'class': 'form-select'}),
            'quantity_used': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
        labels = {
            'part': 'Деталь',
            'quantity_used': 'Количество',
        }


class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = [
            'part_number', 'name', 'component_type', 'resistance', 'power',
            'voltage', 'current', 'capacitance', 'min_stock', 'lead_time_days',
            'preferred_supplier', 'description'
        ]
        widgets = {
            'part_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'component_type': forms.TextInput(attrs={'class': 'form-control', 'list': 'component-types'}),
            'resistance': forms.TextInput(attrs={'class': 'form-control'}),
            'power': forms.TextInput(attrs={'class': 'form-control'}),
            'voltage': forms.TextInput(attrs={'class': 'form-control'}),
            'current': forms.TextInput(attrs={'class': 'form-control'}),
            'capacitance': forms.TextInput(attrs={'class': 'form-control'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'lead_time_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'preferred_supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'part_number': 'Артикул',
            'name': 'Название',
            'component_type': 'Тип компонента',
            'resistance': 'Сопротивление',
            'power': 'Мощность',
            'voltage': 'Напряжение',
            'current': 'Ток',
            'capacitance': 'Ёмкость',
            'min_stock': 'Минимальный остаток',
            'lead_time_days': 'Срок поставки (дней)',
            'preferred_supplier': 'Предпочтительный поставщик',
            'description': 'Описание',
        }


class StockMovementForm(forms.ModelForm):
    """Форма для прихода на склад."""
    class Meta:
        model = StockMovement
        fields = ['quantity', 'document_number', 'notes']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'quantity': 'Количество',
            'document_number': 'Номер документа',
            'notes': 'Примечания',
        }


class StorageCellForm(forms.ModelForm):
    class Meta:
        model = StorageCell
        fields = ['cabinet_number', 'row_number', 'cell_row', 'part']
        widgets = {
            'cabinet_number': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '12'}),
            'row_number': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '8'}),
            'cell_row': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '8'}),
            'part': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'cabinet_number': 'Номер кассетницы',
            'row_number': 'Номер ряда',
            'cell_row': 'Номер ячейки',
            'part': 'Деталь',
        }


class EmployeeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль', required=False,
        help_text='Оставьте пустым, чтобы не менять пароль при редактировании'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Подтверждение пароля', required=False
    )

    class Meta:
        model = Employee
        fields = ['username', 'full_name', 'email', 'role', 'is_active', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Логин',
            'full_name': 'ФИО',
            'email': 'Email',
            'role': 'Роль',
            'is_active': 'Активен',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class StatusChangeForm(forms.Form):
    new_status = forms.ChoiceField(
        choices=RepairOrder.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Новый статус'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label='Примечания', required=False
    )
