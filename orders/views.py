from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderForm
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer


def order_list(request):
    table_number = request.GET.get('table_number')
    status = request.GET.get('status')

    # Фильтрация заказов
    orders = Order.objects.all()
    if table_number:
        orders = orders.filter(table_number=table_number)
    if status:
        orders = orders.filter(status=status)

    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Сначала сохраняем объект Order без связи Many-to-Many
            order = form.save(commit=False)
            order.save()  # Сохраняем объект, чтобы получить id
            # Теперь устанавливаем связь Many-to-Many с блюдами
            form.save_m2m()  # Сохраняем связи Many-to-Many
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})


def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})


def revenue_report(request):
    # Фильтруем заказы со статусом "оплачено" и суммируем их стоимость
    total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'orders/revenue_report.html', {'total_revenue': total_revenue})


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
