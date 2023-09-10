from modeltranslation.translator import TranslationOptions, translator

from .models import Banner, Category, Product


class CategoryTranslationOption(TranslationOptions):
    fields = ("name", "description")


class ProductTranslationOption(TranslationOptions):
    fields = ("name", "type", "description")


class BannerTranslationOption(TranslationOptions):
    fields = ("title", "description")


translator.register(Category, CategoryTranslationOption)
translator.register(Product, ProductTranslationOption)
translator.register(Banner, BannerTranslationOption)
