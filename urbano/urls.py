from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='templates/login.html'), name='login'),
    path('logout/', views.safe_logout, name='logout'),
    path('account/', views.account, name='account'),
    # category pages
    path("categories/", views.categories, name="categories"),
    path("category/<slug:slug>/", views.category_products, name="category_products"),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    # trending pages
    path("best-sellers/", views.best_sellers, name="best_sellers"),
    path("new-arrivals/", views.new_arrivals, name="new_arrivals"),
    path("on-sale/", views.on_sale, name="on_sale"),
    # collections
    path("summer-edit/", views.summer_edit, name="summer_edit"),
    path("workspace/", views.workspace, name="workspace"),
    path("gifts/", views.gifts, name="gifts"),
    # featured
    path("featured/", views.featured_product, name="featured_product"),
    #cart
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("search/", views.search_products, name="search"),
    path("update-cart/<str:key>/", views.update_cart, name="update_cart"),
    path("remove-cart/<str:key>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/", views.payment, name="payment"),
    path("payment-callback/", views.payment_callback, name="payment_callback"),
    path("order-success/<str:order_id>/", views.order_success, name="order_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
    path('my-orders/', views.my_orders, name='my_orders'),
    path("cancel-order/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("about-us/", views.about, name="about"),
    path("contact/", views.contact_view, name="contact"),
]


