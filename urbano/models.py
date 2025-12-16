from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    title = models.CharField(max_length=200)
    sizes = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    brand = models.CharField(max_length=100, blank=True, null=True)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True)
    features = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    tag = models.CharField(
        max_length=50,
        choices=[
            ('summer', 'Summer Edit'),
            ('workspace', 'Workspace'),
            ('gifts', 'Gifts'),
        ],
        blank=True,
        null=True
    )
    is_best_seller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    @property
    def size_list(self):
        return [s.strip() for s in (self.sizes or "").split(",") if s.strip()]

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/multiple/')

    def __str__(self):
        return f"{self.product.title} Image"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'product', 'size')  # ensures unique per user/product/size

    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.size}) x {self.quantity}"
    
# ---- Order models ----
class Order(models.Model):
    PAYMENT_METHODS = (("RZP", "Razorpay"), ("COD", "Cash on Delivery"))
    STATUS_CHOICES = (
        ("Placed", "Placed"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Cancelled", "Cancelled"),
    )
    DELIVERY_CHOICES = [
        ('standard', 'Standard Delivery (5-7 days)'),
        ('express', 'Express Delivery (1-2 days)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_link_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Placed")
    is_paid = models.BooleanField(default=False)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='standard')
    delivery_days = models.PositiveIntegerField(default=5)
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    def total(self):
        return self.quantity * self.price

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"





