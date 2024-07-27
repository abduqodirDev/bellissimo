from django.contrib import admin

from order.models import CartItem, ItemThrough, Order


class CartItemInline(admin.TabularInline):
    model = ItemThrough
    extra = 1


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'quantity', 'subtotal')
    list_filter = ('user', 'status')


@admin.register(ItemThrough)
class ItemThroughAdmin(admin.ModelAdmin):
    list_display = ('order', 'cartitem', 'is_pizza', 'pizza_shape', 'pizza_volume')
    list_filter = ('order', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)
    list_display = ('user', 'status', 'total_price', 'order_number')
    list_filter = ('user', 'status')
