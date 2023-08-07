from django.db import models
from django.utils.translation import gettext_lazy as _
from my_apps.accounts.models import User


class Category(models.Model):
    name = models.CharField(_("category name"), max_length=100)
    slug = models.SlugField(_("category slug"), unique=True)
    description = models.TextField(_("category description"), blank=True)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("product name"), max_length=200)
    slug = models.SlugField(_("product slug"), unique=True)
    description = models.TextField(_("product description"), blank=True)
    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE
    )
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        _("discount"), max_digits=5, decimal_places=2, default=0
    )
    quantity = models.PositiveIntegerField(_("count of product"), default=0)
    image = models.ImageField(
        _("product image"), upload_to="products/", blank=True, null=True
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)
    sold = models.PositiveIntegerField(_("number sold"), default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    ready = 1
    on_its_way = 2
    delivered = 3
    STATUS_CHOICES = (
        (ready, "ready"),
        (on_its_way, "on its way"),
        (delivered, "delivered"),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    customer = models.ForeignKey(
        User, related_name="customer", on_delete=models.CASCADE
    )
    manager = models.ForeignKey(User, related_name="manager", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItem")
    order_date = models.DateTimeField(_("create order"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update order"), auto_now=True)
    total_amount = models.DecimalField(
        _("total amount order"), max_digits=10, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"Order #{self.pk} by {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity product"), blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.pk}"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(_("title"), max_length=200)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(_("create"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.product.name}"


class Rating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    global_value = models.IntegerField(
        _("global rating"), choices=[(i, i) for i in range(1, 11)]
    )
    quality = models.IntegerField(
        _("quality rating"), choices=[(i, i) for i in range(1, 11)]
    )
    delivery = models.IntegerField(
        _("delivery rating"), choices=[(i, i) for i in range(1, 11)]
    )
    foto_quality = models.IntegerField(
        _("foto quality rating"), choices=[(i, i) for i in range(1, 11)]
    )
    description_quality = models.IntegerField(
        _("description quality"), choices=[(i, i) for i in range(1, 11)]
    )
    value = models.IntegerField(
        _("another rating"), choices=[(i, i) for i in range(1, 11)]
    )
    created_at = models.DateTimeField(_("create"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)

    def __str__(self):
        return f"{self.value} stars - {self.product.name}"
