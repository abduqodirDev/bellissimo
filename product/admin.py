from django.contrib import admin

from product.models import Category, Product, ProductChild, Ingredient, IngredientToProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'category', 'price', 'in_stock', 'image', 'product_child')
    list_filter = ('category', 'status', 'in_stock')
    search_fields = ('name', 'description')
    list_display_links = ('name', 'product_child')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(ProductChild)
class ProductChildAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'pizza_type', 'ingredient_count', 'ingredient')
    list_filter = ('status', 'pizza_type')
    search_fields = ('id', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'price_status', 'in_stock')
    list_filter = ('status', 'price_status')


@admin.register(IngredientToProduct)
class IngredientToProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
