from django.contrib import admin
from api.models import Category, Product, CustomUser

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CustomUser)
