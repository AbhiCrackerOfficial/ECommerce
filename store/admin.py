from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Product, Order, OrderItem, Payment, AuthUsers


class AuthUsersAdmin(UserAdmin):
    # Add the new fields to the fieldsets for the User admin
    fieldsets = UserAdmin.fieldsets + (
        ("Address and Contact Info", {
            "fields": ("street", "city", "state", "zipcode", "phone_number",)
        }),
    )
    # Add the new fields to the list of fields used when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Address and Contact Info", {
            "fields": ("street", "city", "state", "zipcode", "phone_number",)
        }),
    )


admin.site.register(AuthUsers, AuthUsersAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price',
                    'image', 'category', 'stock_count')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'status')
    search_fields = ('user__username',)
    list_filter = ('status',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_method', 'date_paid', 'amount')
    search_fields = ('order__id',)
    list_filter = ('payment_method',)
