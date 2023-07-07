from django.contrib import admin
from .models import Product, Invoice, ProductInInvoice, Client

# Register your models here.
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Client)


admin.site.register(ProductInInvoice)

