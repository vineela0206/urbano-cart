from django.contrib import admin
from .models import Product, Category, ProductImage, ContactMessage, Order, OrderItem, CartItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'old_price', 'category')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('category',)
    inlines = [ProductImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "size", "quantity")
    list_filter = ("user", "product", "size")
    search_fields = ("user__username", "product__title", "size")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "total_display")

    def total_display(self, obj):
        return obj.total()

    total_display.short_description = "Total"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "payment_method", "status", "is_paid", "created_at")
    list_filter = ("status", "payment_method", "is_paid", "created_at")
    search_fields = ("user__username", "id", "payment_id")
    readonly_fields = ("payment_id", "razorpay_payment_link_id", "razorpay_signature", "created_at")
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "total")
    search_fields = ("order__id", "product__title")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)