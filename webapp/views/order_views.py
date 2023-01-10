from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, View
from webapp.forms import OrderForm
from webapp.models import Order, ProductOrder, Product


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'order/list.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.request.user.pk)
        return queryset


class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(data=request.POST)
        if 'cart_items' in request.session:
            cart_product_ids = [item['product_id'] for item in request.session['cart_items']]
            if form.is_valid() and cart_product_ids:
                for i in range(len(request.session['cart_items'])):
                    product_id = request.session['cart_items'][i].get('product_id')
                    quantity = request.session['cart_items'][i]['quantity']
                    product_obj = (get_object_or_404(Product, pk=product_id))
                    order = Order.objects.create(**form.cleaned_data)
                    order.product_id = product_obj
                    order.user = self.request.user if self.request.user else None
                    order.save
                    ProductOrder.objects.create(order_id=order.pk, product_id=product_id, quantity=quantity)
                    del request.session['cart_items'][i]
                    request.session.modified = True
                return redirect('webapp:order_list')
            else:
                return render(request, 'cart/list.html')