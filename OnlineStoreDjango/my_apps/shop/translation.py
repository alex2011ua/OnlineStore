from modeltranslation.translator import TranslationOptions, translator

from .models import Banner, Category, Faq, Product, Settings


class CategoryTranslationOption(TranslationOptions):
    fields = ("name", "description")


class ProductTranslationOption(TranslationOptions):
    fields = ("name", "type", "description")


class BannerTranslationOption(TranslationOptions):
    fields = ("title", "description", "img", "mobileImg")


class SettingsTranslationOption(TranslationOptions):
    fields = ("name", "description")


class FaqTranslationOption(TranslationOptions):
    fields = ("question", "answer")


translator.register(Category, CategoryTranslationOption)
translator.register(Product, ProductTranslationOption)
translator.register(Banner, BannerTranslationOption)
translator.register(Settings, SettingsTranslationOption)
translator.register(Faq, FaqTranslationOption)
