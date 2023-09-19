import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from my_apps.accounts.models import User


class Settings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("name settimgs"), max_length=100, unique=True)
    description = models.TextField(_("category description"), blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        "self",
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="sub_category",
    )
    name = models.CharField(_("category name"), max_length=100)
    slug = models.SlugField(_("category slug"), unique=True, blank=True, null=True)
    description = models.TextField(_("category description"), blank=True, null=True)
    img_small = models.ImageField(
        _("category icon image small"),
        upload_to="foto/categories/",
        blank=True,
        null=True,
    )
    img = models.ImageField(
        _("category image"), upload_to="foto/categories/", blank=True, null=True
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category(slug):
        cat = Category.objects.filter(slug=slug)
        if cat:
            return cat[0]

    @staticmethod
    def get_by_id(id):
        """
        todo: add
        """
        return Category.objects.get(id=id)

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Category ID - {self.pk}"

    class Meta:
        ordering = ["-category__name", "name"]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("product name"), max_length=200)
    slug = models.SlugField(_("product slug"), unique=True)
    type = models.CharField(_("product type"), max_length=200, blank=True, null=True)
    description = models.TextField(_("product description"), blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        _("discount"), max_digits=5, decimal_places=2, default=0
    )
    quantity = models.PositiveIntegerField(_("count of product"), default=0)
    img = models.ImageField(
        _("product image"), upload_to="foto/products/", blank=True, null=True
    )
    img_small = models.ImageField(
        _("product image small"), upload_to="foto/products/", blank=True, null=True
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)
    sold = models.PositiveIntegerField(_("number sold"), default=0)

    wishlist = models.ManyToManyField(
        User, related_name="wishlist"
    )  # add products to user wishlist

    global_rating = models.IntegerField(
        _("global rating"),
        choices=[(i, i) for i in range(0, 6)],
        blank=True,
        null=True,
    )
    quality = models.IntegerField(
        _("quality rating"),
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
    )
    delivery = models.IntegerField(
        _("delivery rating"),
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
    )
    foto_quality = models.IntegerField(
        _("foto quality rating"),
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
    )

    @staticmethod
    def get_products_in_category(category: uuid.UUID):
        """return all products in category or subcategories."""
        if category:
            products = Product.objects.filter(
                Q(category__category=category) | Q(category=category)
            )
            return products
        else:
            return Product.objects.all()

    @staticmethod
    def get_by_id(key):
        p = Product.objects.filter(id=key)
        if len(p) == 1:
            return p[0]

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Product ID - {self.pk}"

    def get_category_name(self):
        return self.category.name

    class Meta:
        ordering = ["category"]


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    new_order = 1
    ready = 2
    on_its_way = 3
    delivered = 4

    STATUS_CHOICES = (
        (new_order, "new order"),
        (ready, "ready"),
        (on_its_way, "on its way"),
        (delivered, "delivered"),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)

    customer = models.ForeignKey(
        User, related_name="customer", on_delete=models.CASCADE
    )
    manager = models.ForeignKey(
        User, related_name="manager", on_delete=models.CASCADE, blank=True, null=True
    )
    products = models.ManyToManyField(Product, through="OrderItem")
    order_date = models.DateTimeField(_("create order"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update order"), auto_now=True)
    total_amount = models.DecimalField(
        _("total amount order"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )

    def get_order_info(self, id):
        order = self.objects.get(id=id)

    @staticmethod
    def get_current_order_id(user):
        order, _ = Order.objects.get_or_create(customer=user, status=Order.new_order)
        return order

    def __str__(self):
        return f"Order #{self.pk} by {self.customer}"

    class Meta:
        ordering = ["-order_date"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity product"), default=0)

    def save(self, *args, **kwargs):
        """modify total_amount in order (add to order)"""

        self.order.total_amount += self.product.price * self.quantity
        self.order.save()
        # call the save() method of the parent
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """modify total_amount in order (minus from order)"""
        self.order.total_amount -= self.product.price * self.quantity
        self.order.save()
        # call the save() method of the parent
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.pk}"


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    global_value = models.IntegerField(
        _("global rating"),
        choices=[(i, i) for i in range(0, 6)],
        blank=True,
        null=True,
    )
    quality = models.IntegerField(
        _("quality rating"),
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
    )
    delivery = models.IntegerField(
        _("delivery rating"),
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
    )
    foto_quality = models.IntegerField(
        _("foto quality rating"),
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
    )
    description_quality = models.IntegerField(
        _("description quality"),
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
    )
    value = models.IntegerField(
        _("another rating"),
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_("create"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)

    def __str__(self):
        return f"{self.value} stars - {self.product.name}"


class Banner(models.Model):
    import uuid

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(_("product slug"), unique=True)
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    img = models.ImageField(
        _("banner image"),
        upload_to="foto/banners/",
        blank=True,
        null=True,
    )
    mobileImg = models.ImageField(
        _("banner for mobile"),
        upload_to="foto/banners/",
        blank=True,
        null=True,
    )
    link = models.CharField(_("link"), default="/catalog")
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f"Baner ID - {self.id}"

    class Meta:
        ordering = ["-updated_at"]
