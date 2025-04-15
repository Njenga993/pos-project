from django.contrib import admin
from .models import Product, Sale, SaleItem, Inventory

admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Sale)
admin.site.register(SaleItem)
