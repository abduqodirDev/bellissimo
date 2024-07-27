from django.contrib import admin

from kombo.models import Kombo, ChildKombo, ChildKomboItem


class ChildKomboItemInline(admin.TabularInline):
    model = ChildKomboItem
    extra = 1


@admin.register(Kombo)
class KomboAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'discount_price', 'in_stock', 'image')
    list_filter = ['in_stock']
    search_fields = ('name', 'description', 'product')
    exclude = ('category', )


@admin.register(ChildKombo)
class ChildKomboAdmin(admin.ModelAdmin):
    inlines = (ChildKomboItemInline, )
    list_display = ('kombo', 'status', 'quantity')
    list_filter = ('kombo', 'status')
    list_display_links = ('kombo', 'status')


@admin.register(ChildKomboItem)
class ChildKomboItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ('product', )
    list_display = ('childkombo', 'product', 'is_pizza', 'overprice', 'size')
    list_filter = ('childkombo', 'is_pizza')
