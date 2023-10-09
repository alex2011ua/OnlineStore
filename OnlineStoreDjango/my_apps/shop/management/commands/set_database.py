import csv
import os

from django.core.management.base import BaseCommand
from my_apps.shop.models import Banner, Category, Product


class Command(BaseCommand):
    main_category = {
        "technique": "Техніка",
        "dishes": "Посуд",
        "food": "Їжа",
        "knowledge": "Знання",
        "clothes": "Одяг",
        "accessories": "Аксесуари",
        "office": "Канцелярія",
        "games": "Ігри",
    }
    subcat_dict = {
        "technique": [
            {"slug": "keyboards", "name": "Клавіатури", "name_en": "Keyboards"},
            {"slug": "headphones", "name": "Навушники", "name_en": "Headphones"},
            {"slug": "powerbanks", "name": "Повербанки", "name_en": "Powerbanks"},
            {"slug": "lamps", "name": "Настільні лампи", "name_en": "Lamps"},
            {"slug": "massagers", "name": "Масажери", "name_en": "Massagers"},
        ],
        "dishes": [
            {"slug": "mugs", "name": "Чашки", "name_en": "Mugs"},
            {"slug": "termomugs", "name": "Термокружки", "name_en": "Termomugs"},
            {"slug": "lunchboxes", "name": "Ланч бокси", "name_en": "Lunch boxes"},
            {"slug": "bottles", "name": "Пляшки для води", "name_en": "Bottles"},
        ],
        "food": [
            {"slug": "candies", "name": "Цукерки", "name_en": "Candies"},
            {
                "slug": "secret_cookies",
                "name": "Печиво з передбаченням",
                "name_en": "Secret cookies",
            },
            {"slug": "tea", "name": "Чай", "name_en": "Tea"},
            {"slug": "coffee", "name": "Кава", "name_en": "Coffee"},
            {
                "slug": "cocktails",
                "name": "Суміші для коктейлів",
                "name_en": "Cocktails",
            },
        ],
        "knowledge": [
            {"slug": "books", "name": "Книги", "name_en": "Books"},
            {"slug": "courses", "name": "Курси", "name_en": "Courses"},
        ],
        "clothes": [
            {"slug": "socks", "name": "Шкарпетки", "name_en": "Socks"},
            {"slug": "tshirts", "name": "Футболки", "name_en": "T-shirts"},
            {"slug": "hoodies", "name": "Худі", "name_en": "Hoodies"},
            {"slug": "plaids", "name": "Пледи з рукавами", "name_en": "Plaids"},
            {"slug": "slippers", "name": "Капці", "name_en": "Slippers"},
        ],
        "accessories": [
            {"slug": "backpack", "name": "Рюкзаки", "name_en": "Backpack"},
            {
                "slug": "laptopBackpack",
                "name": "Чохли для ноутбуків",
                "name_en": "Laptop Backpack",
            },
            {"slug": "shopper", "name": "Шопери", "name_en": "Shoppers"},
            {"slug": "keychain", "name": "Брелоки", "name_en": "Keychain"},
        ],
        "office": [
            {"slug": "notebooks", "name": "Блокноти", "name_en": "Notebooks"},
            {"slug": "datebook", "name": "Планери", "name_en": "Datebook"},
            {"slug": "magboard", "name": "Магнітні дошки", "name_en": "Magboard"},
            {"slug": "pens", "name": "Ручки", "name_en": "Pens"},
        ],
        "games": [
            {"slug": "3Dpuzzles", "name": "3d пазли", "name_en": "3D puzzles"},
            {
                "slug": "boardGames",
                "name": "Настільні ігри",
                "name_en": "Board Games",
            },
            {"slug": "puzzles", "name": "Головоломки", "name_en": "Puzzles"},
        ],
    }

    def handle(self, *args, **options):
        """Create content in DB"""
        Category.objects.all().delete()
        self.create_categories()
        Banner.objects.all().delete()
        self.create_banners()
        Product.objects.all().delete()
        self.create_products()

    def create_categories(self):
        self.stdout.write(self.style.SUCCESS("Start creating main category"))
        main_category_obj: dict = {}
        for slug, name in self.main_category.items():
            cat, created = Category.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "name_en": slug.capitalize(),
                    "img_small": f"foto/categories/{slug}.svg",
                },
            )
            if created:
                self.stdout.write(self.style.WARNING(f"Category {slug} created"))
            main_category_obj[slug] = cat

        for main_cat, sub_cat in self.subcat_dict.items():
            parrents_cat = main_category_obj[main_cat]
            for cat in sub_cat:
                try:
                    slug = cat["slug"]
                    cat_obj, created = Category.objects.update_or_create(
                        slug=slug,
                        defaults={
                            "name": cat["name"],
                            "name_en": cat["name_en"],
                            "category": parrents_cat,
                            "img": f"foto/categories/{slug}.webp",
                        },
                    )
                    if created:
                        self.stdout.write(
                            self.style.WARNING(f"Category {slug} created")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Category {slug}  has acready created before"
                            )
                        )
                except Exception as ex:
                    self.stdout.write(
                        self.style.WARNING(f"---( \r Error create category")
                    )
                    self.stdout.write(self.style.WARNING(f"cat: {cat}, \r )---"))

    def create_banners(self):
        self.stdout.write(self.style.SUCCESS("Start creating banners"))
        Banner.objects.update_or_create(
            slug="banner150",
            defaults={
                "title_en": "Sales",
                "title": "Знижка",
                "description": "Будьте готові заощадити до 150",
                "description_en": "Get ready to save up to 150",
                "img": "foto/banners/banner150.webp",
                "mobileImg": "foto/banners/banner150_mobile.webp",
                "link": "/catalog",
            },
        )
        Banner.objects.update_or_create(
            slug="banner250",
            defaults={
                "title": "Знижка",
                "title_en": "Sales",
                "description": "Будьте готові заощадити до 250",
                "description_en": "Get ready to save up to 250",
                "img": "foto/banners/banner250.webp",
                "mobileImg": "foto/banners/banner250_mobile.webp",
                "link": "/catalog",
            },
        )
        Banner.objects.update_or_create(
            slug="banner360",
            defaults={
                "title": "Знижка",
                "title_en": "Sales",
                "description": "Будьте готові заощадити до 360",
                "description_en": "Get ready to save up to 360",
                "img": "foto/banners/banner360.webp",
                "mobileImg": "foto/banners/banner360_mobile.webp",
                "link": "/catalog",
            },
        )

    def get_category_by_name(self, name):
        for cat in self.subcat_dict.values():
            for sub_cat in cat:
                if sub_cat["name"] == name:
                    return Category.objects.get(slug=sub_cat["slug"])
        raise Exception("no category")

    def create_products(self):
        self.stdout.write(self.style.SUCCESS("Start creating products"))
        current_file = os.path.realpath(__file__)
        current_directory = os.path.dirname(current_file)
        cout_products = 0
        with open(current_directory + "/1.csv") as csvfile:
            reader = csv.reader(csvfile)
            reader.__next__()
            for row in reader:
                # Get category
                category_str = row[3].strip().capitalize()
                name = row[6]
                name_en = row[13]
                if len(name) == 0:
                    continue
                slug = row[0]
                image = "foto/products/" + slug + ".webp"

                type_product = row[7]
                type_product_en = row[14]
                description = row[8]
                description_en = row[15]
                try:
                    category = self.get_category_by_name(category_str)
                    price = float(row[5].replace(" ", ""))
                    quantity = int(row[9]) if row[9].isdigit() else 0
                    sold = int(row[10]) if row[10].isdigit() else 0
                    global_rating = int(row[11]) if row[11].isdigit() else None
                    discount = int(row[12]) if row[12].isdigit() else 0

                    product, created = Product.objects.update_or_create(
                        slug=slug,
                        defaults={
                            "category": category,
                            "price": price,
                            "name": name,
                            "name_en": name_en,
                            "description": description,
                            "description_en": description_en,
                            "img": image,
                            "type": type_product,
                            "type_en": type_product_en,
                            "quantity": quantity,
                            "sold": sold,
                            "global_rating": global_rating,
                            "discount": discount,
                        },
                    )
                    cout_products += 1
                except Exception as ex:
                    self.stdout.write(
                        self.style.WARNING(f"---( \r Error read from csv file: {ex}")
                    )
                    self.stdout.write(
                        self.style.WARNING(
                            f"slug: {slug}, name: {name}, category: {category_str}\r )---"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS("count products:" + str(cout_products))
            )
