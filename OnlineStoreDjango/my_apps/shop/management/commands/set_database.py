import csv
import os
import random

from django.core.management.base import BaseCommand
from my_apps.accounts.models import User
from my_apps.shop.models import Banner, Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Create content in DB"""
        self.create_categories()
        self.create_banners()
        self.create_products()

    def create_categories(self):
        self.stdout.write(self.style.SUCCESS("Start creating main category"))
        main_category = {
            "technique": "Техніка",
            "dishes": "Посуд",
            "food": "Їжа",
            "knowledge": "Знання",
            "clothes": "Одяг",
            "accessories": "Аксесуари",
            "chancellery": "Канцелярія",
        }
        main_category_list = []
        for slug, name in main_category.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "image_small": f"foto/category/{slug}.jpg"},
            )
            self.stdout.write(slug)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category {slug} is already created")
                )
            main_category_list.append(cat)

        self.stdout.write(self.style.SUCCESS(f"Start creating {main_category_list[0]}"))
        technique = {
            "keyboard": "Клавіатури",
            "earphones": "Навушники",
            "pover_bank": "Повербанки",
            "table_lamps": "Настільні лампи",
            "massagers": "Масажери",
        }
        for slug, name in technique.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": main_category_list[0],
                    "image": f"foto/category/{slug}.jpg",
                },
            )
            self.stdout.write(slug)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category {slug} is already created")
                )

        self.stdout.write(self.style.SUCCESS(f"Start creating {main_category_list[1]}"))
        dishes = {
            "cup": "Чашки",
            "thermal_mugs": "Термокружки",
            "lunch_box": "Ланч бокси",
            "water_bottles": "Пляшки для води",
        }
        for slug, name in dishes.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": main_category_list[1],
                    "image": f"foto/category/{slug}.jpg",
                },
            )
            self.stdout.write(slug)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category {slug} is already created")
                )

        self.stdout.write(self.style.SUCCESS(f"Start creating {main_category_list[2]}"))
        food = {
            "candy": "Цукерки",
            "prediction_cookies": "Печиво з передбаченням",
            "tea": "Чай",
            "coffee": "Кава",
            "cocktail_mixes": "Суміші для коктейлів",
        }
        for slug, name in food.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": main_category_list[2],
                    "image": f"foto/category/{slug}.jpg",
                },
            )
            self.stdout.write(slug)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category {slug} is already created")
                )

        self.stdout.write(self.style.SUCCESS(f"Start creating {main_category_list[3]}"))
        knowledge = {"book": "Книги", "courses": "Курси"}
        for slug, name in knowledge.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": main_category_list[3],
                    "image": f"foto/category/{slug}.jpg",
                },
            )
            self.stdout.write(slug)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category {slug} is already created")
                )

        self.stdout.write(self.style.SUCCESS(f"Start creating {main_category_list[4]}"))
        clothes = {
            "socks": "Шкарпетки",
            "T-shirt": "Футболки",
            "thin": "Худі",
            "plaids": "Пледи з рукавами",
            "slippers": "Тапці",
        }
        for slug, name in clothes.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": main_category_list[4],
                    "image": f"foto/category/{slug}.jpg",
                },
            )
            self.stdout.write(slug)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category {slug} is already created")
                )

        self.stdout.write(self.style.SUCCESS(f"Start creating {main_category_list[5]}"))
        accessories = {
            "backpack": "Рюкзаки",
            "covers_for_laptops": "Чохли для ноутбуків",
            "shoppers": "Шопери",
            "charm": "Брелоки",
        }
        for slug, name in accessories.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": main_category_list[5],
                    "image": f"foto/category/{slug}.jpg",
                },
            )
            self.stdout.write(slug)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category {slug} is already created")
                )

        self.stdout.write(self.style.SUCCESS(f"Start creating {main_category_list[6]}"))
        chancellery = {
            "notebook": "Блокноти",
            "sailplane": "Планери",
            "magnetic_boards": "Магнітні дошки",
            "pen": "Ручки",
        }
        for slug, name in chancellery.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": main_category_list[6],
                    "image": f"foto/category/{slug}.jpg",
                },
            )
            self.stdout.write(slug)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category {slug} is already created")
                )

    def create_banners(self):
        self.stdout.write(self.style.SUCCESS("Start creating banners"))

    def create_products(self):
        cat = {
            "Клавіатури": "keyboard",
            "Навушники": "earphones",
            "Повербанки": "pover_bank",
            "Настільні лампи": "table_lamps",
            "Масажери": "massagers",
            "Чашки": "cup",
            "Термокружки": "thermal_mugs",
            "Ланч бокси": "lunch_box",
            "Пляшки для води": "water_bottles",
            "Цукерки": "candy",
            "Печиво з передбаченням": "prediction_cookies",
            "Чай": "tea",
            "Кава": "coffee",
            "Суміші для коктейлів": "cocktail_mixes",
            "Шкарпетки": "socks",
            "Футболки": "T-shirt",
            "Худі": "thin",
            "Пледи з рукавами": "plaids",
            "Тапці": "slippers",
            "Рюкзаки": "backpack",
            "Чохли для ноутбуків": "covers_for_laptops",
            "Шопери": "shoppers",
            "Брелоки": "charm",
            "Блокноти": "notebook",
            "Планери": "sailplane",
            "Магнітні дошки": "magnetic_boards",
            "Ручки": "pen",
            "Книги": "book",
            "Курси": "courses",
        }
        self.stdout.write(self.style.SUCCESS("Start creating products"))
        current_file = os.path.realpath(__file__)
        current_directory = os.path.dirname(current_file)
        with open(current_directory + "/1.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                category_str = row[3].strip().capitalize()
                category_eng = cat.get(category_str)
                if (
                    category_eng
                    and Category.get_category(category_eng)
                    and len(row[5]) > 0
                ):
                    category = Category.get_category(category_eng)
                    try:
                        price = float(row[5].replace(" ", ""))
                    except ValueError:
                        print(category)
                        continue
                    name = row[6]
                    type = row[7]
                    description = row[8]
                    slug = row[0]
                    image = "foto/products/" + slug+ ".webp"
                    Product.objects.get_or_create(
                        slug=slug,
                        defaults={
                            "category": category,
                            "price": price,
                            "name": name,
                            "description": description,
                            "image": image,
                            "type": type
                        },
                    )

