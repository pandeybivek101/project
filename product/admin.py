from django.contrib import admin
from .models import Product, Catagory, Comment, Replies
# Register your models here.
admin.site.register(Product)
admin.site.register(Catagory)
admin.site.register(Comment)
admin.site.register(Replies)