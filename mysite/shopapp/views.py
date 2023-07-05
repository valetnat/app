import logging
from csv import DictWriter
from timeit import default_timer

from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core import serializers
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .common import save_csv_products
from .forms import ProductForm
from .models import Product, Order, ProductImage
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse


log = logging.getLogger(__name__)


@extend_schema(description='Products views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Set of views on Product

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    ordering_fields = ["name", 'price']
    search_fields = ["name"]
    filterset_fields = [
        "name",
        "description",
    ]

    @method_decorator(cache_page(5))
    def list(self, *args, **kwargs):
        # print("Frefe")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves **product**, return 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Product by id not found')
        }
    )
    def retrieve(self,  *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = 'products-export.csv'
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]

        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(
        methods=['post'],
        detail=False,
        parser_classes=[MultiPartParser]
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('products')
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = ['user', 'products']
    ordering_fields = ['user', 'created_at']


class ShopIndexView(View):
    # @method_decorator(cache_page(5)) #  or set cache page in urls
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        print('Shop idex context', context)
        return render(request, 'shopapp/shop-index.html', context=context)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]

        elem = products_data[0]
        name = elem['name']
        print(name)
        return JsonResponse({"products": products_data})


# RSS articles
class LatestProductsFeed(Feed):
    """
    RSS Products View
    """
    title = "Shopapp products (latest)"
    description = 'Updates on changes and addition shopapp products'
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
            Product.objects
            .filter(archived=False)[:2]
        )

    def item_name(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:30]


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/user_orders_list.html'

    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs["user_id"])
        return (Order.objects
                .filter(user=self.owner)
                .select_related("user")
                .prefetch_related("products")
                )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.owner
        return context


class UserOrdersDataExportView(View):

    def get(self, request, *args, **kwargs):

        cache_key = "user_{}".format(self.kwargs['user_id'])
        data_json = cache.get(cache_key)

        if data_json is None:
            self.owner = get_object_or_404(User, pk=self.kwargs["user_id"])
            orders = (Order.objects
                      .filter(user=self.owner)
                      .select_related("user")
                      .prefetch_related("products")
                      .order_by("pk")
                      )

            data_json = {"Orders": OrderSerializer(orders, many=True).data}
            cache.set(cache_key, data_json, 5)

        return JsonResponse(data_json)