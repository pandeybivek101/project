from django.contrib import admin
from .models import Product, Catagory, Comment
# Register your models here.
admin.site.register(Product)
admin.site.register(Catagory)
admin.site.register(Comment)