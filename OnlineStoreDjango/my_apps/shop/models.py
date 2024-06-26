import uuid

from django.db import models
from django.db.models import Q, QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, ValidationError

from phonenumber_field.modelfields import PhoneNumberField

from my_apps.accounts.models import User


class Settings(models.Model):  # type: ignore
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("title"), max_length=100, unique=True)
    description = models.TextField(_("text"), blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    def to_dict(self):
        obj_dict = {"title": self.name, "text": self.description}
        return obj_dict


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    """

    try:
        uuid_obj = uuid.UUID(str(uuid_to_test), version=version)
    except ValueError:
        return False
    return True


class Category(models.Model):  # type: ignore
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
    slug = models.SlugField(
        _("category slug"), unique=True, blank=True, null=True, db_index=True
    )  # create index
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
    def get_main_categories():
        return Category.objects.filter(category=None)

    @staticmethod
    def get_category(slug):
        try:
            cat = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise NotFound(detail="category not found")
        return cat

    @staticmethod
    def get_by_id(_id):
        if not is_valid_uuid(_id):
            raise NotFound(detail="category id not UUID")
        try:
            category = Category.objects.get(id=_id)
        except Category.DoesNotExist:
            raise NotFound(detail="category not found")
        return category

    def get_sub_categories(self):
        subcategories = Category.objects.filter(category=self)
        return subcategories

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Category ID - {self.pk}"

    class Meta:
        ordering = ["-category__name", "name"]


class Product(models.Model):  # type: ignore
    RATING = [(i, i) for i in range(0, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("product name"), max_length=200)
    slug = models.SlugField(_("product slug"), unique=True)
    type = models.CharField(_("product type"), max_length=200, blank=True, null=True)
    description = models.TextField(_("product description"), blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    discount = models.DecimalField(_("discount"), max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(_("count of product"), default=0)
    img = models.ImageField(_("product image"), upload_to="foto/products/", blank=True, null=True)
    img1 = models.ImageField(
        _("product image 1"), upload_to="foto/products/", blank=True, null=True
    )
    img2 = models.ImageField(
        _("product image 2"), upload_to="foto/products/", blank=True, null=True
    )
    img3 = models.ImageField(
        _("product image 3"), upload_to="foto/products/", blank=True, null=True
    )
    img_small = models.ImageField(
        _("product image small"), upload_to="foto/products/", blank=True, null=True
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)
    sold = models.PositiveIntegerField(_("number sold"), default=0)

    wishlist = models.ManyToManyField(
        User,
        related_name="wishlist",
        blank=True,
    )  # add products to user wishlist
    basket = models.ManyToManyField(User, through="BasketItem")  # type: ignore
    global_rating = models.IntegerField(
        _("global rating"), choices=RATING, default=0
    )
    quality = models.IntegerField(
        _("quality rating"), choices=RATING, default=0
    )
    rating_price = models.IntegerField(
        _("price"), choices=RATING, default=0
    )
    photo_match = models.IntegerField(
        _("photo_match"), choices=RATING, default=0
    )
    description_match = models.IntegerField(
        _("description_match"), choices=RATING, default=0
    )
    _1 = models.IntegerField("number of reviews 1*", blank=True, null=True)
    _2 = models.IntegerField("number of reviews 2*", blank=True, null=True)
    _3 = models.IntegerField("number of reviews 3*", blank=True, null=True)
    _4 = models.IntegerField("number of reviews 4*", blank=True, null=True)
    _5 = models.IntegerField("number of reviews 5*", blank=True, null=True)

    @staticmethod
    def get_products_in_category(category: uuid.UUID):
        """return all products in category or subcategories."""
        category = Category.get_by_id(category)
        products = Product.objects.select_related("category").filter(
            Q(category__category=category) | Q(category=category)
        )
        return products

    @staticmethod
    def get_by_id(key):
        if is_valid_uuid(key):
            try:
                product = Product.objects.get(id=key)
            except Product.DoesNotExist:
                raise NotFound(detail="product not found")
            return product
        else:
            raise NotFound(detail="product id not UUID")

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Product ID - {self.pk}"

    def is_in_cart(self, user: User) -> bool | None:
        if user.is_authenticated:
            basket = user.basket.all()
            products_in_basket = [product.product for product in basket]
            return True if self in products_in_basket else False

    def is_in_wishlist(self, user: User) -> bool | None:
        if user.is_authenticated:
            wishlist = user.wishlist.all()
            return True if self in wishlist else False

    def get_category_name(self):
        return self.category.name

    def get_category_slug(self) -> str:
        return self.category.slug

    def get_reviews(self):
        return self.reviews.select_related("customer").all()

    def images(self):
        img = [str(self.img)]
        if self.img1:
            img.append(str(self.img1))
        if self.img2:
            img.append(str(self.img2))
        if self.img3:
            img.append(str(self.img3))
        return img

    def rate_by_stars(self) -> dict:
        """Return dict with the number of comments with a certain number of stars.

        rate_by_stars: {
            _5: number;
            _4:number;
            _3:number;
            _2:number;
            _1:number;
            _0:number;
        }
        """

        stars_dict = {}
        if self._1:
            stars_dict["_1"] = self._1
        if self._2:
            stars_dict["_2"] = self._2
        if self._3:
            stars_dict["_3"] = self._3
        if self._4:
            stars_dict["_4"] = self._4
        if self._5:
            stars_dict["_5"] = self._5
        return stars_dict

    def rate_by_criteria(self) -> dict:
        """rating by criteria. arithmetic mean of all comments by criteria.

        rate_by_criteria: {
            quality: number
            photo_match: number
            description_match: number
            price: number
        }
        """

        return {
            "quality": self.quality,
            "photo_match": self.photo_match,
            "description_match": self.description_match,
            "price": self.rating_price,
        }

    class Meta:
        ordering = ["category"]
        indexes = [models.Index(fields=["created_at", "price"])]
        constraints = [models.CheckConstraint(check=models.Q(price__gt=0), name="valid_price")]


class BasketItem(models.Model):
    registered_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="basket")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod_in_basket")
    quantity = models.PositiveIntegerField(_("quantity product"), default=0)
    is_secret_present = models.BooleanField(default=False)


class Review(models.Model):

    RATING = [(i, i) for i in range(0, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(_("title"), max_length=200)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(_("create"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)

    global_rate = models.IntegerField(
        _("global_rating"), choices=RATING, default=0
    )

    quality = models.IntegerField(
        _("quality rating"), choices=RATING, default=0
    )
    price = models.IntegerField(_("price"), choices=RATING, default=0)
    photo_match = models.IntegerField(
        _("foto quality rating"), choices=RATING, default=0
    )
    description_match = models.IntegerField(
        _("description match"), choices=RATING, default=0
    )

    def get_user_name(self):
        return self.author.get_full_name()

    def rate_by_criteria(self) -> dict:
        """rating by criteria. arithmetic mean of all comments by criteria.

        return: {
            quality: number
            photo_match: number
            description_match: number
            price: number
        }
        """

        return {
            "quality": self.quality,
            "photo_match": self.photo_match,
            "description_match": self.description_match,
            "price": self.price,
        }

    def __str__(self):
        return f"{self.global_rate} stars - {self.product.name}"


class Banner(models.Model):  # type: ignore
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


class Faq(models.Model):  # type: ignore
    """Frequently asked questions and their answers about the product."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="faq")
    question = models.CharField(_("question"), max_length=200)
    answer = models.TextField(_("answer"))


class Order(models.Model):
    id = models.AutoField(primary_key=True, editable=False)

    STATUS_CHOICES = (
        ("staffing", "staffing"),
        ("sending", "sending"),
        ("returning", "returning"),
        ("completing", "completing"),
    )
    DELIVERY_TYPE = [
        ("self", "self"),
        ("nova", "nova"),
        ("ukr", "ukr"),
    ]
    DELIVERY_OPTION = [
        ("courier", "courier"),
        ("post_office", "post_office"),
    ]
    status = models.CharField(choices=STATUS_CHOICES, default="staffing", max_length=11)

    customer = models.ForeignKey(
        User, related_name="customer", on_delete=models.CASCADE, blank=True, null=True
    )
    manager = models.ForeignKey(
        User, related_name="manager", on_delete=models.CASCADE, blank=True, null=True
    )
    products = models.ManyToManyField(Product, through="OrderItem")  # type: ignore
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
    first_name = models.CharField(_("first name"), max_length=50, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, max_length=254)
    tel = PhoneNumberField(null=True, blank=True)
    delivery_type = models.CharField(
        choices=DELIVERY_TYPE, max_length=5, default="SELF"
    )  # вид доставки (самовивіз, через нову або укр пошту)
    delivery_option = models.CharField(
        choices=DELIVERY_OPTION, max_length=12, blank=True, null=True
    )  # якщо обрана пошту як вид, то кур'єром чи на відділення
    town = models.CharField(max_length=50, blank=True, null=True)  # місто (якщо вказаний вид пошта)
    address = models.CharField(
        max_length=150, blank=True, null=True
    )  # вулиця (якщо вказаний вид пошта + кур'єр)
    building = models.CharField(
        max_length=50, blank=True, null=True
    )  # номер дому (якщо вказаний вид пошта + кур'єр)
    flat = models.CharField(
        max_length=50, blank=True, null=True
    )  # номер квартири (якщо вказаний вид пошта + кур'єр)
    post_office = models.CharField(
        max_length=50, blank=True, null=True
    )  # відділення (якщо вказаний вид пошта + відділення)
    comment = models.TextField(blank=True, null=True)  # текст коментаря (якщо is_comment: true)
    is_not_recall = models.BooleanField(default=False)  # флаг не треба телефонувати
    is_another_person = models.BooleanField(default=False)  # флаг отримувач інша людина
    is_gift = models.BooleanField(default=False)  # флаг святкова упаковка
    is_comment = models.BooleanField(default=False)  # флаг чи є коментар

    another_person_tel = PhoneNumberField(null=True, blank=True)
    another_person_firstName = models.CharField(
        _("another person first name"), max_length=50, blank=True, null=True
    )
    another_person_lastName = models.CharField(
        _("another person last name"), max_length=50, blank=True, null=True
    )
    """
        another_person?: { // дані отримувача інша людина (якщо is_another_person:true)
        tel: string;
        firstName: string;
        lastName: string;
    """

    @classmethod
    def get_by_id(cls, pk: str):
        try:
            order = cls.objects.get(id=pk)
        except Order.DoesNotExist:
            raise NotFound(detail="order not found")
        return order

    def add_product_to_order(self, product: Product, amount):
        products_in_order = self.products.all()
        if product in products_in_order:
            oi = OrderItem.objects.get(product=product, order=self)
            oi.quantity = amount
            oi.save()
        else:
            self.products.add(product, through_defaults={"quantity": amount})  # type: ignore

    def get_products_order(self):
        oi = OrderItem.objects.filter(order=self)
        product_list_in_order = []
        for prod in oi:
            product_list_in_order.append({"prodID": prod.product.id, "quantity": prod.quantity})
        return product_list_in_order

    def delete_product_order(self, product: Product):
        products_in_order = self.products.all()
        if product in products_in_order:
            self.products.remove(product)

    @staticmethod
    def get_current_order_id(user):
        order, _ = Order.objects.get_or_create(customer=user, status="new_order")
        return order

    def __str__(self):
        return f"Order #{self.pk} by {self.customer}"

    class Meta:
        ordering = ["-order_date"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity product"), default=0)  # todo dell default
    is_secret_present = models.BooleanField(default=False)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, default=0)  # todo dell default
    img = models.ImageField(_("product image"), upload_to="foto/products/", blank=True, null=True)
    name = models.CharField(_("name"), max_length=150, blank=True, null=True)

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
