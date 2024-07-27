from django.contrib import admin

from common.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'user', 'name_address')
    list_filter = ('user', )
    search_fields = ('address', 'name_address')
