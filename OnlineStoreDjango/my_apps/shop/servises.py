from my_apps.shop.models import Order, OrderItem, Product


def order_create(*args, **kwargs) -> Order:
    items = kwargs.pop("items")
    another_person = {"another_person_tel": None}
    if kwargs.get("is_another_person", False):
        a_p = kwargs.pop("another_person")
        another_person["another_person_firstName"] = a_p.get("firstName")
        another_person["another_person_lastName"] = a_p.get("lastName")
        another_person["another_person_tel"] = a_p.get("tel")

    first_name = kwargs.pop("firstName", None)
    last_name = kwargs.pop("lastName", None)

    obj = Order(first_name=first_name, last_name=last_name, **kwargs, **another_person)

    obj.full_clean()
    obj.save()

    for item in items:
        product = Product.get_by_id(item.get("product"))
        quantity = item.get("quantity")
        is_secret_present = item.get("is_secret_present", False)
        price = product.discount or product.price
        img = product.img
        name = product.name
        OrderItem(order=obj, product=product, quantity=quantity, is_secret_present=is_secret_present, price=price,
                  img=img, name=name).save()

    return obj
