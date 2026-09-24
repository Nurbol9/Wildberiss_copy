from django.contrib import admin
from .models import (UserProfile, Category, Product,
                     SubCategory, ProductImage, Review,Cart, CartItem)

from modeltranslation.admin import TranslationAdmin,TranslationInlineModelAdmin


admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
