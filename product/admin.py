from django.contrib import admin
from .models import Product, Catagory, Comment, Replies, Message, SubCatagory


class ProductStore(admin.ModelAdmin):
	list_display = ['title', 'user', 'catagory', 'price']
admin.site.register(Product, ProductStore)


class CatagoryStore(admin.ModelAdmin):
	list_display = ['catagory']
admin.site.register(Catagory, CatagoryStore)


class Commentlist(admin.ModelAdmin):
	list_display = ['user', 'product', 'comment']
admin.site.register(Comment, Commentlist)


class RepList(admin.ModelAdmin):
	list_display = ['replied_user','comment', 'reply']
admin.site.register(Replies, RepList)


class MsgList(admin.ModelAdmin):
	list_display=['message_user','message']
admin.site.register(Message, MsgList)


admin.site.register(SubCatagory)