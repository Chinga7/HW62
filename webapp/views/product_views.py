from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Product
from webapp.forms import SearchForm, ProductForm


CATEGORY_CHOICES = [
    ('other', 'Other'),
    ('books', 'Books'),
    ('flowers', 'Flowers'),
    ('furniture', 'Furniture'),
    ('gadgets', 'Gadgets')
]


# Create your views here.
class ProductListView(ListView):
    template_name = 'product/list.html'
    model = Product
    context_object_name = 'products'
    ordering = 'category', 'name'
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(leftover__gt=0)
        if self.search_value:
            queryset = queryset.filter(Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value) | Q(leftover__gt=0))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product/create.html'
    form_class = ProductForm
    permission_required = 'webapp.add_product'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'product/update.html'
    form_class = ProductForm
    model = Product
    context_object_name = 'product'
    permission_required = 'webapp.change_product'


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'product/delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('webapp:product_list')
    permission_required = 'webapp.delete_product'
