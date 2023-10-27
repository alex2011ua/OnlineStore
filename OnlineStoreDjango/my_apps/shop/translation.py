from modeltranslation.translator import TranslationOptions, translator

from .models import Banner, Category, Product, Settings


class CategoryTranslationOption(TranslationOptions):
    fields = ("name", "description")


class ProductTranslationOption(TranslationOptions):
    fields = ("name", "type", "description")


class BannerTranslationOption(TranslationOptions):
    fields = ("title", "description")


class SettingsTranslationOption(TranslationOptions):
    fields = ("name", "description")


translator.register(Category, CategoryTranslationOption)
translator.register(Product, ProductTranslationOption)
translator.register(Banner, BannerTranslationOption)
translator.register(Settings, SettingsTranslationOption)
