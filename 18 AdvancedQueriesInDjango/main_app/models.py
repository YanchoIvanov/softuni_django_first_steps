from django.db import models
from django.db.models import Sum, Q, F


def product_quantity_ordered():
    total_products_ordered = (Product.objects.annotate(total_ordered_quantity=Sum('orderproduct__quantity')
                                                      ).exclude(total_ordered_quantity=None
                                                                ).order_by('-total_ordered_quantity'))
    result = []
    for product in total_products_ordered:
        result.append(f"Quantity ordered of {product.name}: {product.total_ordered_quantity}")

    return '\n'.join(result)


def ordered_products_per_customer():
    prefetched_orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')

    result = []

    for order in prefetched_orders:
        result.append(f"Order ID: {order.id}, Customer: {order.customer.username}")

        for order_product in order.orderproduct_set.all():
            result.append(f"- Product: {order_product.product.name}, Category: {order_product.product.category.name}")

    return '\n'.join(result)


def filter_products():
    query = Q(is_available=True) & Q(price__gt=3.00)
    products = Product.objects.filter(query).order_by('-price', 'name')

    result = []

    for product in products:
        result.append(f"{product.name}: {product.price}lv.")

    return '\n'.join(result)


def give_discount():
    reduce = F('price') * 0.7
    query = Q(is_available=True) & Q(price__gt=3.00)
    Product.objects.filter(query).update(price=reduce)
    all_available_products = (Product.objects.filter(is_available=True).order_by('-price', 'name'))

    result = []

    for product in all_available_products:
        result.append(f"{product.name}: {product.price}lv.")

    return '\n'.join(result)


class ProductManager(models.Manager):

    def available_products(self):
        return self.filter(is_available=True)

    def available_products_in_category(self, category_name):
        return self.filter(is_available=True, category__name=category_name)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category.name}: {self.name}"

    objects = ProductManager()


class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


