from my_apps.shop.models import Order, OrderItem


def order_create(*args, **kwargs) -> Order:
    print(kwargs)
    items = kwargs.pop("items")
    is_another_person = kwargs["is_another_person"]
    if is_another_person:
        another_person = kwargs["another_person"]
    first_name = kwargs["firstName"]
    last_name = kwargs["lastName"]
    email = kwargs["email"]
    tel = kwargs["tel"]
    delivery_type = kwargs["delivery_type"]
    deliveries = {}
    if delivery_type != "self":
        deliveries = {
            "delivery_option": kwargs["delivery_option"],
            "town": kwargs["town"],
            "building": kwargs["building"],
            "flat": kwargs["flat"],
            "post_office": kwargs["post_office"],
        }

        delivery_option = kwargs["delivery_option"]
        town = kwargs["town"]
        building = kwargs["building"]
        flat = kwargs["flat"]
        post_office = kwargs["post_office"]
    is_comment = kwargs["is_comment"]
    if is_comment:
        comment = kwargs["comment"]
    is_not_recall = kwargs["is_not_recall"]
    is_gift = kwargs["is_gift"]

    obj = Order(
        first_name=first_name,
        last_name=last_name,
        email=email,
        tel=tel,
        delivery_type=delivery_type,
        is_not_recall=is_not_recall,
        is_gift=is_gift,
        is_comment=is_comment,
        **deliveries,
    )

    obj.full_clean()
    obj.save()

    return obj
