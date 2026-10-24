import logging
import traceback
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

from .models import Customer, Restaurant, Item, Cart, Order

import razorpay
from django.conf import settings

logger = logging.getLogger(__name__)


# =========================================================
# HOME
# =========================================================

def index(request):
    return render(request, 'delivery/index.html')


# =========================================================
# SIGN IN / SIGN UP
# =========================================================

def open_signin(request):
    return render(request, 'delivery/signin.html')


def open_signup(request):
    return render(request, 'delivery/signup.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        address = request.POST.get('address', '').strip()

        try:
            if not all([username, password, email, mobile, address]):
                return HttpResponse(
                    "All fields are required.",
                    status=400
                )

            # Validate against the current Customer model limits.
            if len(username) > 20:
                return HttpResponse("Username is too long.", status=400)

            if len(password) > 20:
                return HttpResponse("Password is too long.", status=400)

            if len(email) > 500:
                return HttpResponse("Email is too long.", status=400)

            if len(mobile) > 10:
                return HttpResponse("Mobile number is too long.", status=400)

            if len(address) > 50:
                return HttpResponse("Address is too long.", status=400)

            if Customer.objects.filter(username=username).exists():
                return HttpResponse("Duplicate username!", status=400)

            Customer.objects.create(
                username=username,
                password=password,
                email=email,
                mobile=mobile,
                address=address
            )

            return render(request, 'delivery/signin.html')

        except Exception:
            print("CUSTOMER REGISTRATION ERROR:", flush=True)
            traceback.print_exc()
            return HttpResponse(
                "Registration failed. Please try again.",
                 status=500
    )

    return render(request, 'delivery/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Admin login
        if username == 'Pruthu316' and password == 'admin316':
            return render(
                request,
                'delivery/admin_home.html',
                {'username': username}
            )

        # Customer login
        customer = Customer.objects.filter(
            username=username,
            password=password
        ).first()

        if customer:
            return render(
                request,
                'delivery/customer_home.html',
                {'username': username}
            )

        return render(
            request,
            'delivery/signin.html',
            {'error': 'Invalid username or password. Please try again.'}
        )

    return render(request, 'delivery/signin.html')


# =========================================================
# RESTAURANT MANAGEMENT
# =========================================================

def open_add_restaurant(request):
    return render(request, 'delivery/add_restaurant.html')


def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(
            name=name,
            picture=picture,
            cuisine=cuisine,
            rating=rating
        )

        return HttpResponse("Restaurant added successfully!")

    return render(request, 'delivery/add_restaurant.html')


# ---------------------------------------------------------
# ADMIN - SHOW RESTAURANTS
# ---------------------------------------------------------

def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()

    return render(
        request,
        'delivery/show_restaurants.html',
        {'restaurantList': restaurantList}
    )


# ---------------------------------------------------------
# CUSTOMER - SHOW RESTAURANTS
# ---------------------------------------------------------

def customer_restaurants(request, username):
    restaurantList = Restaurant.objects.all()

    return render(
        request,
        'delivery/customer_menu.html',
        {
            'restaurantList': restaurantList,
            'username': username,
            'page_type': 'restaurants'
        }
    )


# ---------------------------------------------------------
# UPDATE RESTAURANT
# ---------------------------------------------------------

def open_update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')

        restaurant.save()

        return HttpResponse("Restaurant updated successfully!")

    return render(
        request,
        'delivery/update_restaurant.html',
        {'restaurant': restaurant}
    )


# ---------------------------------------------------------
# DELETE RESTAURANT
# ---------------------------------------------------------

def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()

    return render(
        request,
        'delivery/show_restaurants.html',
        {'restaurantList': restaurantList}
    )


# =========================================================
# MENU MANAGEMENT
# =========================================================

def open_update_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    itemList = restaurant.items.all()

    return render(
        request,
        'delivery/update_menu.html',
        {
            'itemList': itemList,
            'restaurant': restaurant
        }
    )


# ---------------------------------------------------------
# ADD NEW MENU ITEM
# ---------------------------------------------------------

def update_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')

        if Item.objects.filter(
            restaurant=restaurant,
            name=name
        ).exists():
            return HttpResponse("Duplicate item!")

        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            vegeterian=vegeterian,
            picture=picture
        )

        return redirect(
            'open_update_menu',
            restaurant_id=restaurant.id
        )

    return redirect(
        'open_update_menu',
        restaurant_id=restaurant.id
    )


# ---------------------------------------------------------
# EDIT EXISTING MENU ITEM
# ---------------------------------------------------------

def edit_menu_item(request, restaurant_id, item_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    item = get_object_or_404(
        Item,
        id=item_id,
        restaurant=restaurant
    )

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        picture = request.POST.get('picture')
        vegeterian = request.POST.get('vegeterian') == 'on'

        duplicate_item = Item.objects.filter(
            restaurant=restaurant,
            name=name
        ).exclude(id=item.id).exists()

        if duplicate_item:
            return HttpResponse(
                "Another menu item with this name already exists!"
            )

        item.name = name
        item.description = description
        item.price = price
        item.picture = picture
        item.vegeterian = vegeterian
        item.save()

        return redirect(
            'open_update_menu',
            restaurant_id=restaurant.id
        )

    return render(
        request,
        'delivery/edit_menu_item.html',
        {
            'restaurant': restaurant,
            'item': item
        }
    )


# ---------------------------------------------------------
# DELETE EXISTING MENU ITEM
# ---------------------------------------------------------

def delete_menu_item(request, restaurant_id, item_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    item = get_object_or_404(
        Item,
        id=item_id,
        restaurant=restaurant
    )

    if request.method == 'POST':
        item.delete()

    return redirect(
        'open_update_menu',
        restaurant_id=restaurant.id
    )


# =========================================================
# CUSTOMER MENU
# =========================================================

def view_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    itemList = restaurant.items.all()

    return render(
        request,
        'delivery/customer_menu.html',
        {
            'itemList': itemList,
            'restaurant': restaurant,
            'username': username,
            'page_type': 'menu'
        }
    )


# =========================================================
# CART
# =========================================================

def add_to_cart(request, item_id, username):
    if request.method != 'POST':
        return JsonResponse(
            {'success': False, 'message': 'Use POST to add an item.'},
            status=405
        )

    item = get_object_or_404(Item, id=item_id)
    customer = get_object_or_404(Customer, username=username)

    cart, created = Cart.objects.get_or_create(customer=customer)
    cart.items.add(item)

    return JsonResponse({
        'success': True,
        'message': 'Added to cart successfully!'
    })


# ---------------------------------------------------------
# DELETE ITEM FROM CART
# ---------------------------------------------------------

def delete_from_cart(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)

    cart = get_object_or_404(Cart, customer=customer)
    item = get_object_or_404(Item, id=item_id)

    cart.items.remove(item)

    return redirect('show_cart', username=username)


# ---------------------------------------------------------
# SHOW CART
# ---------------------------------------------------------

def show_cart(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(
        request,
        'delivery/cart.html',
        {
            'itemList': items,
            'total_price': total_price,
            'username': username
        }
    )


# =========================================================
# CHECKOUT
# =========================================================

def checkout(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(
            request,
            'delivery/checkout.html',
            {
                'username': username,
                'error': 'Your cart is empty!'
            }
        )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    amount_paise = int(round(float(total_price) * 100))

    order_data = {
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': 1
    }

    razorpay_order = client.order.create(data=order_data)

    return render(
        request,
        'delivery/checkout.html',
        {
            'username': username,
            'cart_items': cart_items,
            'total_price': total_price,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': razorpay_order['id'],
            'amount': amount_paise
        }
    )


# =========================================================
# PAYMENT VERIFICATION
# =========================================================

def verify_payment(request, username):
    if request.method != 'POST':
        return JsonResponse(
            {'success': False, 'message': 'Invalid request method.'},
            status=405
        )

    customer = get_object_or_404(Customer, username=username)
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '').strip()
    razorpay_order_id = request.POST.get('razorpay_order_id', '').strip()
    razorpay_signature = request.POST.get('razorpay_signature', '').strip()

    if not (razorpay_payment_id and razorpay_order_id and razorpay_signature):
        return JsonResponse(
            {'success': False, 'message': 'Missing payment verification parameters.'},
            status=400
        )

    # Prevent duplicate orders
    existing_order = Order.objects.filter(
        razorpay_payment_id=razorpay_payment_id
    ).first()

    if existing_order:
        return JsonResponse({
            'success': True,
            'order_id': existing_order.id,
            'redirect_url': f'/orders/{username}/'
        })

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse(
            {'success': False, 'message': 'Payment verification failed!'},
            status=400
        )
    except Exception:
        logger.exception("Payment verification failed")
        return JsonResponse(
            {'success': False, 'message': 'Payment verification failed.'},
            status=500
        )

    cart = Cart.objects.filter(customer=customer).first()
    cart_items = list(cart.items.all()) if cart else []
    total = cart.total_price() if cart else 0

    order = Order.objects.create(
        customer=customer,
        total_price=total,
        payment_status='Paid',
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id
    )

    if cart_items:
        order.items.set(cart_items)

    if cart:
        cart.items.clear()

    return JsonResponse({
        'success': True,
        'order_id': order.id,
        'redirect_url': f'/orders/{username}/'
    })


# =========================================================
# ORDER HISTORY
# =========================================================

def orders(request, username):
    customer = get_object_or_404(Customer, username=username)

    order_history = Order.objects.filter(
        customer=customer
    ).prefetch_related('items').order_by('-created_at')

    return render(
        request,
        'delivery/orders.html',
        {
            'username': username,
            'customer': customer,
            'order_history': order_history
        }
    )


# =========================================================
# CUSTOMER PROFILE
# =========================================================

def customer_profile(request, username):
    customer = get_object_or_404(Customer, username=username)

    return render(
        request,
        'delivery/customer_profile.html',
        {
            'customer': customer,
            'username': username
        }
    )


# =========================================================
# CUSTOMER - EDIT PROFILE
# =========================================================

def edit_profile(request, username):
    customer = get_object_or_404(Customer, username=username)

    if request.method == 'POST':
        new_username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password', '')

        if not new_username:
            return render(
                request,
                'delivery/edit_profile.html',
                {
                    'customer': customer,
                    'username': username,
                    'error': 'Username cannot be empty.'
                }
            )

        if Customer.objects.filter(
            username=new_username
        ).exclude(pk=customer.pk).exists():
            return render(
                request,
                'delivery/edit_profile.html',
                {
                    'customer': customer,
                    'username': username,
                    'error': 'This username is already taken.'
                }
            )

        customer.username = new_username
        customer.email = email
        customer.mobile = mobile
        customer.address = address

        if password:
            customer.password = password

        customer.save()

        return redirect(
            'customer_profile',
            username=new_username
        )

    return render(
        request,
        'delivery/edit_profile.html',
        {
            'customer': customer,
            'username': username
        }
    )