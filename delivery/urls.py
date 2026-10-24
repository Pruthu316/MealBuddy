from django.urls import path
from . import views

urlpatterns = [

    # =========================================================
    # HOME
    # =========================================================

    path(
        '',
        views.index,
        name='index'
    ),

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    path(
        'open_signin/',
        views.open_signin,
        name='open_signin'
    ),

    path(
        'open_signup/',
        views.open_signup,
        name='open_signup'
    ),

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'signin/',
        views.signin,
        name='signin'
    ),

    # =========================================================
    # ADMIN - RESTAURANT MANAGEMENT
    # =========================================================

    path(
        'open_add_restaurant/',
        views.open_add_restaurant,
        name='open_add_restaurant'
    ),

    path(
        'add_restaurant/',
        views.add_restaurant,
        name='add_restaurant'
    ),

    path(
        'open_show_restaurant/',
        views.open_show_restaurant,
        name='open_show_restaurant'
    ),

    path(
        'open_update_restaurant/<int:restaurant_id>/',
        views.open_update_restaurant,
        name='open_update_restaurant'
    ),

    path(
        'delete_restaurant/<int:restaurant_id>/',
        views.delete_restaurant,
        name='delete_restaurant'
    ),

    # =========================================================
    # ADMIN - MENU MANAGEMENT
    # =========================================================

    path(
        'open_update_menu/<int:restaurant_id>/',
        views.open_update_menu,
        name='open_update_menu'
    ),

    path(
        'update_menu/<int:restaurant_id>/',
        views.update_menu,
        name='update_menu'
    ),

    path(
        'edit_menu_item/<int:restaurant_id>/<int:item_id>/',
        views.edit_menu_item,
        name='edit_menu_item'
    ),

    path(
        'delete_menu_item/<int:restaurant_id>/<int:item_id>/',
        views.delete_menu_item,
        name='delete_menu_item'
    ),

    # =========================================================
    # CUSTOMER - PROFILE
    # =========================================================

    path(
        'customer_profile/<str:username>/',
        views.customer_profile,
        name='customer_profile'
    ),

    # =========================================================
    # CUSTOMER - EDIT PROFILE
    # =========================================================

    path(
        'edit_profile/<str:username>/',
        views.edit_profile,
        name='edit_profile'
    ),

    # =========================================================
    # CUSTOMER - RESTAURANTS
    # =========================================================

    path(
        'customer_restaurants/<str:username>/',
        views.customer_restaurants,
        name='customer_restaurants'
    ),

    # =========================================================
    # CUSTOMER - MENU
    # =========================================================

    path(
        'view_menu/<int:restaurant_id>/<str:username>/',
        views.view_menu,
        name='view_menu'
    ),

    # =========================================================
    # CUSTOMER - CART
    # =========================================================

    path(
        'add_to_cart/<int:item_id>/<str:username>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'show_cart/<str:username>/',
        views.show_cart,
        name='show_cart'
    ),

    path(
        'delete_from_cart/<int:item_id>/<str:username>/',
        views.delete_from_cart,
        name='delete_from_cart'
    ),

    # =========================================================
    # CUSTOMER - CHECKOUT & ORDERS
    # =========================================================

    path(
        'checkout/<str:username>/',
        views.checkout,
        name='checkout'
    ),

    path(
        'verify_payment/<str:username>/',
        views.verify_payment,
        name='verify_payment'
    ),

    path(
        'orders/<str:username>/',
        views.orders,
        name='orders'
    ),

]