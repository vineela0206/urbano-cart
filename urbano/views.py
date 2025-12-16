from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import Product, Category, Order, OrderItem, ContactMessage, CartItem
from django.db.models import Q
from django.utils import timezone

# Create your views here.
@require_http_methods(["GET", "POST"])
def safe_logout(request):
    logout(request)
    return redirect('home')

#Categories pages
FIXED_CATEGORY_SLUGS = [
    "clothing",
    "accessories",
    "electronics",
    "footwear",
    "home-living",
    "health-beauty",
]

def home(request):
    hero_categories = []
    for slug in FIXED_CATEGORY_SLUGS:
        category = get_object_or_404(Category, slug=slug)
        product = Product.objects.filter(category=category).first()
        if product:
            hero_categories.append({
                "category": category,
                "product": product
            })
    new_arrivals = Product.objects.all().order_by('-id')[:4]
    trending = Product.objects.filter(is_best_seller=True)[:3]
    context = {
        "hero_categories":hero_categories,
        "new_arrivals": new_arrivals,
        "trending": trending
    }
    return render(request, "home.html", context)

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log user in immediately
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def account(request):
    return render(request, 'account.html')


def categories(request):
    categories = Category.objects.filter(
        slug__in=FIXED_CATEGORY_SLUGS
    ).order_by("name")

    context = {
        "categories": categories
    }
    return render(request, "categories.html", context)

def category_products(request, slug):

    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    # filters
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    brand = request.GET.get("brand")
    sort = request.GET.get("sort")

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if brand and brand != "all":
        products = products.filter(brand__iexact=brand)

    if sort == "low_to_high":
        products = products.order_by("price")
    elif sort == "high_to_low":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-id")
    elif sort == "discount":
        products = sorted(products, key=lambda p: p.discount_percentage, reverse=True)

    brands = products.values_list("brand", flat=True).distinct()

    return render(request, "category_products.html", {
        "category": category,
        "products": products,
        "brands": brands,
        "page_title": category.name,
    })

def filter_and_sort_products(request, queryset):
    # --- PRICE FILTER ---
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    # --- BRAND FILTER ---
    brand = request.GET.get("brand")
    if brand and brand != "all":
        queryset = queryset.filter(brand=brand)

    # --- SORTING ---
    sort = request.GET.get("sort")
    if sort == "low_to_high":
        queryset = queryset.order_by("price")
    elif sort == "high_to_low":
        queryset = queryset.order_by("-price")
    elif sort == "newest":
        queryset = queryset.order_by("-id")
    elif sort == "discount":
        queryset = sorted(queryset, key=lambda p: p.discount_percentage, reverse=True)

    return queryset

#Trending pages
def best_sellers(request):
    products = Product.objects.filter(is_best_seller=True)
    products = filter_and_sort_products(request, products)
    brands = products.values_list("brand", flat=True).distinct()

    return render(request, "best_sellers.html", {
        "products": products,
        "brands": brands,
        "page_title": "Best Sellers",
    })

def new_arrivals(request):
    products = Product.objects.order_by("-id")[:12]
    products = filter_and_sort_products(request, products)
    brands = products.values_list("brand", flat=True).distinct()

    return render(request, "new_arrivals.html", {
        "products": products,
        "brands": brands,
        "page_title": "New Arrivals",
    })

def on_sale(request):
    products = Product.objects.filter(old_price__gt=0)
    products = filter_and_sort_products(request, products)
    brands = products.values_list("brand", flat=True).distinct()

    return render(request, "on_sale.html", {
        "products": products,
        "brands": brands,
        "page_title": "On Sale",
    })

#Collections pages
def summer_edit(request):
    products = Product.objects.filter(tag="summer")
    products = filter_and_sort_products(request, products)
    brands = products.values_list("brand", flat=True).distinct()

    return render(request, "summer_edit.html", {
        "products": products,
        "brands": brands,
        "page_title": "Summer Edit",
    })

def workspace(request):
    products = Product.objects.filter(tag="workspace")
    products = filter_and_sort_products(request, products)
    brands = products.values_list("brand", flat=True).distinct()

    return render(request, "workspace.html", {
        "products": products,
        "brands": brands,
        "page_title": "Workspace",
    })

def gifts(request):
    products = Product.objects.filter(tag="gift")
    products = filter_and_sort_products(request, products)
    brands = products.values_list("brand", flat=True).distinct()

    return render(request, "gifts.html", {
        "products": products,
        "brands": brands,
        "page_title": "Gifts",
    })

#Featured preview page
def featured_product(request):
    products = Product.objects.filter(is_featured=True)
    products = filter_and_sort_products(request, products)
    brands = products.values_list("brand", flat=True).distinct()
    return render(request, "featured.html", {
        "products": products,
        "brands": brands,
        "page_title": "featured",
    })

#product details page
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.images.all()  # Fetch all related images
    return render(request, "product_detail.html", {"product": product, "images": images})

#cart
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    # get quantity
    quantity = request.POST.get("quantity")
    if quantity:
        try:
            quantity = int(quantity)
        except:
            quantity = 1
    else:
        quantity = 1
    product = Product.objects.get(id=product_id)
    # categories that require a size
    categories_with_sizes = ["Clothing", "Footwear"]
    # check if size was not sent but product requires size
    size = request.POST.get("size")
    if product.category.name in categories_with_sizes and not size:
        # store quantity temporarily so it doesn't get lost
        request.session["pending_quantity"] = quantity
        return render(request, "select_size.html", {
            "product": product
        })

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            size=size
        )
        cart_item.quantity += quantity
        cart_item.save()
        return redirect("cart")
    
    # Unique cart key → product + size
    key = f"{product_id}"
    if size:
        key = f"{product_id}-{size}"

    # if item exists, update qty
    if key in cart:
        cart[key]["qty"] += quantity
    else:
        cart[key] = {
            "qty": quantity,
            "size": size
        }

    request.session["cart"] = cart
    return redirect("cart")

def cart(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
        total_price = sum(i.product.price * i.quantity for i in items)
        total_items = sum(i.quantity for i in items)

        return render(request, "cart.html", {
            "cart_items": items,
            "total_price": total_price,
            "total_items": total_items,
        })
    cart = request.session.get("cart", {})
    cart_items = []

    total_price = 0
    total_items = 0

    for key, data in cart.items():
        product_id = key.split("-")[0]
        qty = data.get("qty", 1)
        size = data.get("size", None)

        product = Product.objects.get(id=product_id)
        item_total = product.price * qty
        total_price += item_total
        total_items += qty

        cart_items.append({
            "id": key,
            "product": product,
            "quantity": qty,
            "size": size,
            "total": item_total
        })

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "total_items": total_items
    })

def search_products(request):
    query = request.GET.get("q", "").strip()

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(brand__icontains=query)
        )

    # Filters
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    brand = request.GET.get("brand")
    sort = request.GET.get("sort")

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if brand and brand != "all":
        products = products.filter(brand__iexact=brand)

    if sort == "low_to_high":
        products = products.order_by("price")
    elif sort == "high_to_low":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-id")
    elif sort == "discount":
        products = sorted(products, key=lambda p: p.discount_percentage, reverse=True)

    brands = products.values_list("brand", flat=True).distinct()

    return render(request, "search_results.html", {
        "products": products,
        "brands": brands,
        "page_title": f"Search results for: {query}",
    })

def update_cart(request, key):
    if request.method == "POST":
        qty = int(request.POST.get("quantity"))
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=key, user=request.user)
            cart_item.quantity = qty
            cart_item.save()
            return redirect("cart")
        cart = request.session.get("cart", {})
        if key in cart:
            cart[key]["qty"] = qty
        request.session["cart"] = cart
    return redirect("cart")


def remove_from_cart(request, key):
    if request.user.is_authenticated:
        CartItem.objects.filter(
            id=key,
            user=request.user
        ).delete()
        return redirect("cart")
    cart = request.session.get("cart", {})
    cart.pop(key, None)
    request.session["cart"] = cart
    return redirect("cart")

@login_required(login_url='login')
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        return redirect("cart")

    demo_data = {}
    if request.user.username == "demo@example.com":
        demo_data = {
            "fullname": "Demo User",
            "phone": "9999999999",
            "address": "123 Demo Street",
            "city": "Demo City",
            "state": "Demo State",
            "pincode": "500000",
        }

    total_price = sum(i.product.price * i.quantity for i in items)
    total_items = sum(i.quantity for i in items)

    return render(request, "checkout.html", {
        "cart_items" : items,
        "total_price": total_price,
        "total_items": total_items,
    })

#Razorpay Order & Redirect to Payment Page
def payment(request):
    if request.method != "POST":
        return redirect("checkout")

    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        return redirect("cart")

    fullname = request.POST.get("fullname")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    city = request.POST.get("city")
    state = request.POST.get("state")
    pincode = request.POST.get("pincode")
    delivery_method = request.POST.get("delivery_method")
    if delivery_method == "standard":
        delivery_days = 5
    elif delivery_method == "express":
        delivery_days = 2
    payment_method = request.POST.get("payment_method")

    # Calculate totals
    total_price = 0
    for item in items:
        total_price += item.product.price * item.quantity

    # Creating Order in DB
    order = Order.objects.create(
        user=request.user,
        fullname=fullname,
        phone=phone,
        address=address,
        city=city,
        state=state,
        pincode=pincode,
        delivery_method=delivery_method,
        delivery_days=delivery_days,
        payment_method=payment_method,
        total_price=total_price,
        is_paid=False,
    )

    # Save Order Items
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            size=item.size,  
        )

    if request.user.username == "demo@example.com":
        # Do not trigger Razorpay
        order.is_paid = True
        order.payment_method = "demo"
        order.save()

        CartItem.objects.filter(user=request.user).delete()

        return redirect("order_success", order_id=order.id)

    # If COD → Complete Order
    if payment_method == "cod":
        order.is_paid = False
        order.save()

        CartItem.objects.filter(user=request.user).delete()
        return redirect("order_success", order_id=order.id)

    # RAZORPAY FLOW -------------------------
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    razorpay_order = client.order.create({
        "amount": int(total_price * 100), 
        "currency": "INR",
        "payment_capture": 1,
    })

    order.razorpay_order_id = razorpay_order["id"]
    order.save()

    return render(request, "payment_page.html", {
        "order": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": razorpay_order["id"],
        "amount": total_price,
    })

#Payment Callback URL
@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        order = Order.objects.get(razorpay_order_id=order_id)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                "razorpay_payment_id": payment_id,
                "razorpay_order_id": order_id,
                "razorpay_signature": signature,
            })

            order.payment_id = payment_id
            order.razorpay_signature = signature
            order.is_paid = True
            order.save()

            CartItem.objects.filter(user=request.user).delete()

            return redirect("order_success", order_id=order.id)

        except Exception as e:
            return render(request, "payment_failed.html")

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "order_success.html", {"order": order})

def payment_failed(request):
    return render(request, "payment_failed.html")

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "my_orders.html", {"orders": orders})

@login_required(login_url='login')
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order.is_cancelled = True
    order.cancelled_at = timezone.now()
    order.save()
    return redirect("my_orders")

def about(request):
    return render(request, "about.html")

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        # Save to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        # Send Email (to admin)
        send_mail(
            subject=f"New Contact Message from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_text}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,
        )

        # Success Message
        messages.success(request, "Thank you! Your message has been sent successfully.")

        return redirect("contact")

    return render(request, "contact.html")
