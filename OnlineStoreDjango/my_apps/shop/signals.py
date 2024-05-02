from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_init, post_delete
from statistics import mean

from my_apps.shop.models import Review


@receiver([post_save, post_delete], sender=Review)
def refresh_rating(sender, instance, **kwargs) -> None:
    """
    Actualize rate for product.
    """

    product = instance.product
    all_rates = product.reviews.all()
    global_rating: list = []
    stars: dict = {1: [], 2: [], 3: [], 4: [], 5: []}
    description_match: list = []
    photo_match: list = []
    rating_price: list = []
    quality: list = []
    for i in all_rates:  # todo make more clarify
        if i.global_rate:
            global_rating.append(i.global_rate)
            stars[i.global_rate].append(1)
        if i.description_match:
            description_match.append(i.description_match)
        if i.price:
            rating_price.append(i.price)
        if i.quality:
            quality.append(i.quality)
        if i.photo_match:
            photo_match.append(i.photo_match)
    product._1 = len(stars[1]) if stars[1] else None
    product._2 = len(stars[2]) if stars[2] else None
    product._3 = len(stars[3]) if stars[3] else None
    product._4 = len(stars[4]) if stars[4] else None
    product._5 = len(stars[5]) if stars[5] else None

    if global_rating:
        product.global_rating = round(mean(global_rating))
    else:
        product.global_rating = 0
    if description_match:
        product.description_match = round(mean(description_match))
    else:
        product.description_match = 0
    if photo_match:
        product.photo_match = round(mean(photo_match))
    else:
        product.photo_match = 0
    if rating_price:
        product.rating_price = round(mean(rating_price))
    else:
        product.rating_price = 0
    if quality:
        product.quality = round(mean(quality))
    else:
        product.quality = 0

    product.save()
