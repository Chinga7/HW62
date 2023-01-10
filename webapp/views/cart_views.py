from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from webapp.models import Product
from webapp.forms import OrderForm
from django.contrib import messages


TOTAL = 0


class CartListView(View):
    template_name = 'cart/list.html'

    def get(self, request, *args, **kwargs):
        response = []
        cart_items = request.session.get('cart_items')
        if cart_items:
            cart_product_ids = [item['product_id'] for item in cart_items]
            products = Product.objects.filter(pk__in=cart_product_ids)

            global TOTAL
            TOTAL = 0
            quantity = 0
            for product in products:
                if cart_items:
                    for item in cart_items:
                        if item['product_id'] == product.pk:
                            quantity = item['quantity']
                    sum = quantity * product.price
                response.append({
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantity,
                    'sum': sum
                })
                TOTAL += sum
        context = {
            'items': response,
            'total': TOTAL,
            'form': OrderForm
        }
        return render(request, self.template_name, context)


def add_to_cart(request, pk, source):
    product = get_object_or_404(Product, pk=pk)
    if 'cart_items' in request.session and product.leftover > 0:
        cart_product_ids = [item['product_id'] for item in request.session['cart_items']]
        if pk in cart_product_ids:
            for item in request.session['cart_items']:
                if item['product_id'] == pk:
                    item['quantity'] += 1
        else:
            request.session['cart_items'].append({
                'product_id': pk,
                'quantity': 1
            })
        product.leftover -= 1
        product.save()
        messages.add_message(request, messages.SUCCESS, f'{product.name} was successfully added')
    elif 'cart_items' not in request.session and product.leftover > 0:
        request.session['cart_items'] = [{
            'product_id': pk,
            'quantity': 1
        }]
        product.leftover -= 1
        product.save()
        messages.add_message(request, messages.SUCCESS, f'{product.name} was successfully added')
    else:
        messages.add_message(request, messages.ERROR, f'{product.name} was not added')
    request.session.modified = True

    if source == 'detail':
        return redirect('webapp:product_detail', pk)
    return redirect('webapp:product_list')


class CartDeleteView(View):
    template_name = 'cart/delete.html'
    success_url = reverse_lazy('webapp:cart_list')

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        context = {
            'product': product
        }
        return render(request, self.template_name,context)

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)

        for i in range(len(request.session['cart_items'])):
            if request.session['cart_items'][i].get('product_id') == pk:
                quantity = request.session['cart_items'][i]['quantity']
                del request.session['cart_items'][i]
                request.session.modified = True
                product.leftover += quantity
                product.save()
                messages.add_message(request, messages.WARNING, f'{quantity} of {product.name}s was successfully deleted')
                break
            else:
                messages.add_message(request, messages.ERROR, f"{product.name}'s items was not successfully deleted")
        return redirect('webapp:cart_list')