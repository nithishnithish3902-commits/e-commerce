from django.contrib import admin
from .models import *
#ithu admin la name id img show pannum#
#class CategoryAdmin(admin.ModelAdmin):#
 # list_display = ('id', 'name', 'image')#

#admin.site.register(Category, CategoryAdmin)
#class ProductAdmin(admin.ModelAdmin):
  #list_display = ('id', 'name', 'product_image')

admin.site.register(Category)
admin.site.register(Product)