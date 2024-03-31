from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, Http404, HttpResponse
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models import F, FloatField
import random
import hashlib
import time
import requests
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def get_cart_items_and_count(user):
    """
    This function returns the cart items and the total count of items for a given user.
    :param user: User object for which cart items and count are needed
    :return: Tuple containing cart items list and total count of items
    """
    # Get the cart associated with the user
    cart = Cart.objects.filter(user=user).first()
    # Initialize cart_items and cart_count
    cart_items = []
    cart_count = 0
    if cart:
        # Retrieve cart items if a cart is found
        cart_items = CartItem.objects.filter(cart=cart)
        # Calculate the total count of items in the cart
        cart_count = cart_items.aggregate(Sum('quantity'))[
            'quantity__sum'] or 0
    return cart_items, cart_count


def add_to_cart(request, product_id):
    """
    This function adds a product to the user's cart or updates the quantity if the product already exists in the cart.
    :param request: The request object
    :param product_id: The ID of the product to be added or updated
    :return: JsonResponse indicating success or a redirect to the 'Sign In' page
    """
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        # Get the product instance or raise a 404 error
        product = get_object_or_404(Product, id=product_id)
        # Get the desired quantity of the product from the POST data (default is 1)
        quantity = int(request.POST.get('quantity', 1))
        # First, get or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=user)
        # Check if the product already exists in the cart
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            # Update the quantity if the product already exists
            cart_item.quantity += quantity
            cart_item.save()
            messages.info(request, "Product quantity updated successfully.")
        else:
            # Create a new CartItem for the product
            cart_item = CartItem(cart=cart, product=product, quantity=quantity)
            cart_item.save()
            messages.info(request, "Product added to cart successfully.")
        # Return a JsonResponse indicating success
        return JsonResponse({"status": "success"})
    else:
        # Inform the user that they need to log in and redirect to the 'Sign In' page
        messages.info(request, "You need to login first.")
        return redirect(reverse('Sign In'))


@login_required
def remove_from_cart(request, product_id):
    """
    This function handles removing a product from the cart.
    :param request: The request object
    :param product_id: The ID of the product to remove from the cart
    :return: JsonResponse containing a success message and status, or an error message and status
    """
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        # Find the CartItem with the specified product ID
        cart_item = CartItem.objects.filter(
            cart_id=cart, product_id=product_id).first()
        # If the CartItem is found, delete it and send a success message
        if cart_item:
            cart_item.delete()
            messages.info(request, "Product removed from cart successfully.")
            return JsonResponse({"status": "success"})
        # If the CartItem is not found, send an error message
        else:
            messages.error(request, "Product not found in cart.")
            return JsonResponse({"status": "error"})
    # If the user is not authenticated, send an error message
    else:
        messages.info(request, "You need to login first.")
        return JsonResponse({"status": "error"})


def verify_otp(request):
    """
    This function handles the rendering of the OTP verification page.
    :param request: The request object
    :return: Rendered OTP verification page or redirect to the appropriate page with a message
    """
    # Check if 'email', 'otp', and 'otp_type' are present in the session
    if 'email' in request.session and 'otp' in request.session and 'otp_type' in request.session:
        # If all required session variables are present, render the OTP verification page
        return render(request, "otp.html")
    else:
        # If any required session variable is missing, show an error message and redirect to the appropriate page
        messages.error(request, "Session expired, please try again.")
        otp_type = request.session.get('otp_type', 'Sign Up')
        return redirect(reverse(otp_type))


def submit_otp(request):
    """
    This function handles the OTP submission and verification.
    :param request: The request object
    :return: Redirect to the appropriate page with a message based on the OTP verification result
    """
    # Check if the request method is POST and required session variables are present
    if request.method == "POST" and 'email' in request.session and 'otp' in request.session and 'otp_type' in request.session:
        # Get the submitted OTP from the request
        user_otp = request.POST.get('otp')
        # Get the stored OTP from the session
        session_otp = request.session.get('otp')
        # Compare the submitted OTP with the stored OTP
        if str(user_otp) == str(session_otp):
            User = get_user_model()
            user = User.objects.get(email=request.session.get('email'))
            if request.session['otp_type'] == 'account_activation':
                # If the OTP is for account activation, activate the user account and redirect to the login page
                User = get_user_model()
                user = User.objects.get(email=request.session.get('email'))
                user.is_active = True
                user.save()
                messages.info(
                    request, "Your account has been activated. Please login.")
                # Clear the session data related to account activation
                del request.session['email']
                del request.session['otp']
                del request.session['otp_type']
                return redirect(reverse('Sign In'))
            if request.session['otp_type'] == 'password_reset':
                # If the OTP is for password reset, set 'password_reset' session variable and redirect to the password reset page
                request.session['password_reset'] = True
                messages.info(
                    request, "OTP verified, please reset your password.")
                return redirect('Reset Password')
            else:
                # If the OTP is for account activation, activate the user account and redirect to the login page
                user.is_active = True
                user.save()
                messages.info(
                    request, "Your account has been activated. Please login.")
                return redirect('Sign In')
        else:
            # If the submitted OTP is invalid, show an error message and redirect to the OTP verification page
            messages.error(request, "Invalid OTP")
            return redirect(reverse('verify_otp'))
    else:
        # If the required session variables are missing, show an error message and redirect to the appropriate page
        messages.error(request, "Session expired, please try again.")
        otp_type = request.session.get('otp_type', 'Sign Up')
        return redirect(reverse(otp_type))


@user_passes_test(lambda u: u.is_anonymous, login_url='home', redirect_field_name=None)
def signup(request):
    """
    This function handles user registration and sends an OTP for email verification.
    :param request: The request object
    :return: Render the signup page or redirect to the OTP verification page
    """
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the user's input from the request
        name = request.POST["name"]
        fname = name.split()[0]
        lname = " ".join(name.split()[1:])
        email = request.POST["email"].lower()
        username = email
        password = request.POST["password"]
        # Get the user model and check if the user already exists
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            # Create a new user
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()
            # Store the user's email in the session
            request.session['email'] = email
            # Generate a random OTP and send it via email
            otp = random.randint(100000, 999999)
            subject = 'Ecommerce Account Activation - One-Time Password (OTP)'
            message = f'Dear customer,\n\nThank you for signing up on Ecommerce! To activate your account, please use the following One-Time Password (OTP):\n{otp}\nThis OTP is valid for 15 minutes. If you did not request this OTP, please ignore this email.\n\nBest regards,\nThe Ecommerce Team'
            from_email = 'ecommercepyd@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            # Store the OTP in the session and redirect to the OTP verification page
            request.session['otp'] = otp
            request.session['otp_type'] = 'Sign Up'
            return redirect(reverse('verify_otp'))
        elif User.objects.filter(username=username, is_active=False).exists():
            request.session['email'] = email
            # Generate a random OTP and send it via email
            otp = random.randint(100000, 999999)
            subject = 'Ecommerce Account Activation - One-Time Password (OTP)'
            message = f'Dear customer,\n\nThank you for signing up on Ecommerce! To activate your account, please use the following One-Time Password (OTP):\n{otp}\nThis OTP is valid for 15 minutes. If you did not request this OTP, please ignore this email.\n\nBest regards,\nThe Ecommerce Team'
            from_email = 'ecommercepyd@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            # Store the OTP in the session and redirect to the OTP verification page
            request.session['otp'] = otp
            request.session['otp_type'] = 'account_activation'
            return redirect(reverse('verify_otp'))
        else:
            # Display an error message if the user already exists
            messages.error(request, "User already exists")
    # Render the signup page
    return render(request, 'signup.html')


def change_quantity(request, product_id, operation):
    """
    This function changes the quantity of a product in the cart.
    :param request: The request object
    :param product_id: The product's ID
    :param operation: The operation to perform (increment or decrement)
    :return: A JSON response indicating the result of the operation
    """
    if request.user.is_authenticated:
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        # First, get or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=user)
        # Check if the product already exists in the cart
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            if operation == "increment":
                cart_item.quantity += 1
            elif operation == "decrement":
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                    messages.info(request, "Product removed from cart.")
                    return JsonResponse({"status": "success"})
            else:
                messages.error(request, "Invalid operation.")
                return JsonResponse({"status": "error"})
            cart_item.save()
            messages.info(request, "Product quantity updated successfully.")
            return JsonResponse({"status": "success"})
        else:
            messages.error(request, "Product not found in the cart.")
            return JsonResponse({"status": "error"})
    else:
        messages.info(request, "You need to login first.")
        return redirect(reverse('Sign In'))


def search(request):
    # Initialize the context dictionary
    context = {}

    # Get the search parameters from the request
    query = request.GET.get('search', '')
    category_id = request.GET.get('category', None)
    sort = request.GET.get('sort', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Initialize the filter parameters with an empty Q object
    filter_params = Q()

    # Add filters to the filter_params based on the search parameters
    if query:
        filter_params &= Q(name__icontains=query)
        context['query'] = query
    if category_id:
        filter_params &= Q(category__id=category_id)
        context['category_name'] = Category.objects.get(id=category_id).name
    if min_price:
        filter_params &= Q(price__gte=min_price)
    if max_price:
        filter_params &= Q(price__lte=max_price)

    # Filter the products using the filter_params
    products = Product.objects.filter(filter_params)

    # Apply sorting based on the sort parameter
    if sort == "low_to_high":
        products = products.order_by('price')
    elif sort == "high_to_low":
        products = products.order_by('-price')
    elif sort == "a_to_z":
        products = products.order_by('name')
    elif sort == "z_to_a":
        products = products.order_by('-name')
    
    # Get all categories
    categories = Category.objects.all()

    # Update the context dictionary with the new data
    context.update({
        'products': products,
        'categories': categories,
        'category_id': category_id,
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price
    })

    # Check if the user is authenticated and update the context accordingly
    if request.user.is_authenticated:
        context['fname'] = request.user.first_name
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = CartItem.objects.filter(
                cart=cart).aggregate(Sum('quantity'))['quantity__sum']
            context['count'] = cart_count if cart_count else 0

    # Render the shop.html template with the context data
    return render(request, 'shop.html', context)


def index(request):
    context = {
        'categories': Category.objects.all(),
        'products': Product.objects.all()
    }
    if request.user.is_authenticated:
        context['fname'] = request.user.first_name
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = CartItem.objects.filter(
                cart=cart).aggregate(Sum('quantity'))['quantity__sum']
            context['count'] = cart_count if cart_count else 0
    return render(request, 'home.html', context)


def signin(request):

    redirect_url = ""
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            # Verify reCAPTCHA response
            recaptcha_response = request.POST.get('g-recaptcha-response')
            recaptcha_data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=recaptcha_data, verify=False)
            result = r.json()
            if not result['success']:
                messages.error(request, "Invalid reCAPTCHA. Please try again.")
                redirect_url = reverse('Sign In')
            else:
                # Authenticate the user
                username = request.POST["email"]
                password = request.POST["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    user.last_login = timezone.now()
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(
                        request, "User is logged in. Redirecting in 3s...")
                    redirect_url = reverse('home')
                else:
                    messages.error(request, "Invalid username or password")
                    redirect_url = reverse('Sign In')
    return render(request, 'signin.html', {'redirect_url': redirect_url})


def check_user_existence(request):

    if request.method == "GET":
        email = request.GET.get("email", "").lower()
        User = get_user_model()
        try:
            User.objects.get(username=email)
            return JsonResponse({"exists": True})
        except User.DoesNotExist:
            return JsonResponse({"exists": False})
    return JsonResponse({"error": "Invalid request"})


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


@login_required(login_url='Sign In')
def cart(request):
    categories = Category.objects.all()
    cart_items, cart_count = get_cart_items_and_count(request.user)
    products = {item.product.id: item.product for item in cart_items}
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'categories': categories,
        'citems': cart_items,
        'products': products,
        'cart_total': cart_total,
        'fname': request.user.first_name,
        'count': cart_count,
    }

    return render(request, 'cart.html', context)


def shop(request):
    # Retrieve all categories
    categories = Category.objects.all()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    filter_params = Q()
    if min_price:
        filter_params &= Q(price__gte=min_price)
    if max_price:
        filter_params &= Q(price__lte=max_price)
    # Get the sort parameter from the request
    sort = request.GET.get('sort', '')
    # Get all products and apply sorting based on the sort parameter
    products = Product.objects.filter(filter_params)
    if sort == "low_to_high":
        products = products.order_by('price')
    elif sort == "high_to_low":
        products = products.order_by('-price')
    elif sort == "a_to_z":
        products = products.order_by('name')
    elif sort == "z_to_a":
        products = products.order_by('-name')
    # Prepare context for rendering the template
    context = {
        'products': products,
        'categories': categories,
        'sort': sort
    }
    # If the user is authenticated, add their first name and cart count to the context
    if request.user.is_authenticated:
        context['fname'] = request.user.first_name
        _, cart_count = get_cart_items_and_count(request.user)
        context['count'] = cart_count
    # Render the 'shop.html' template with the context
    return render(request, 'shop.html', context)


def forgot(request):
    # If the request method is POST, process the form data
    if request.method == "POST":
        # Get the email from the POST request
        email = request.POST.get('email')
        # Get the user model and check if the email exists in the database
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            # Get the user with the matching email
            user = User.objects.get(email=email)
            # Generate a random OTP
            otp = random.randint(100000, 999999)
            # Prepare the email content
            subject = 'Ecommerce Password Reset: One-Time Password (OTP)'
            message = f'Dear customer,\n\nThank you for using Ecommerce. We have received your request to reset your password. To proceed, please use the One-Time Password (OTP) below:\n\nOTP: {otp}\n\nIf you did not request a password reset, please ignore this email or contact our support team for assistance.\n\nBest regards,\nThe Ecommerce Team'
            from_email = 'ecommercepyd@gmail.com'
            recipient_list = [email]
            # Send the email with the OTP
            send_mail(subject, message, from_email, recipient_list)
            # Store the email, OTP, and OTP type in the session
            request.session['email'] = email
            request.session['otp'] = otp
            request.session['otp_type'] = 'password_reset'
            # Redirect the user to the OTP verification page
            return redirect(reverse('verify_otp'))
        else:
            # Display an error message if the email is not found
            messages.error(request, "Email not found")
            return redirect(reverse('Forgot Password'))
    else:
        # Render the forgot.html template if the request method is not POST
        return render(request, 'forgot.html')


def product(request, product_id):
    # Get the product with the given product_id, or return None if not found
    product = Product.objects.filter(id=product_id).first()
    # If the product is not found, raise a 404 error
    if not product:
        raise Http404("Product not found")
    # Get other products in the same category as the current product
    same_products = Product.objects.filter(category_id=product.category_id)
    # Prepare the context dictionary with the product and same_products
    context = {
        'product': product,
        'same_products': same_products,
        'categories': Category.objects.all()
    }
    # If the user is authenticated, add the user's first name and cart item count to the context
    if request.user.is_authenticated:
        context['fname'] = request.user.first_name
        _, cart_count = get_cart_items_and_count(request.user)
        context['count'] = cart_count
    # Render the productdetail.html template with the context data
    return render(request, 'productdetail.html', context=context)


def reset(request):
    # Check if the OTP is not in the session, return an error if not present
    if 'otp' not in request.session:
        return error_403(request)

    # If the request method is POST, process the form data
    if request.method == "POST" and 'email' in request.session and request.session.get('password_reset', False):

        # Get the new password and confirm password from the POST request
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the password and confirm password match
        if password == confirm_password:
            # Get the user model and the user with the matching email
            User = get_user_model()
            user = User.objects.get(email=request.session.get('email'))

            # Update the user's password and save the changes
            user.set_password(password)
            user.save()

            # Clear session data related to password reset
            del request.session['email']
            del request.session['password_reset']
            del request.session['otp']
            del request.session['otp_type']

            # Display a message indicating that the password has been reset
            messages.info(
                request, "Your password has been reset. Please login.")
            return redirect('Sign In')
        else:
            # Display an error message if the passwords do not match
            messages.error(request, "Passwords do not match.")
            return redirect(reverse('Reset Password'))
    else:
        if request.method == "POST":
            # Display an error message if the password reset request is invalid
            messages.error(request, "Invalid password reset request.")
            return redirect(reverse('Forgot Password'))
        else:
            # Render the reset.html template if the request method is not POST
            return render(request, 'reset.html')


def checkout(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get all categories
        categories = Category.objects.all()
        # Prepare the context dictionary with the user's first name and categories
        context = {'fname': request.user.first_name, 'categories': categories}
        # Check if the user's address is set, and add it to the context if present
        if request.user.street != None:
            context.update({
                'street': request.user.street,
                'city': request.user.city,
                'state': request.user.state,
                'zipcode': request.user.zipcode,
                'phone': request.user.phone_number
            })
        # Get the cart items and count for the current user
        cart_items, cart_count = get_cart_items_and_count(request.user)
        # Update the context dictionary with the cart items, count, and total
        context.update({
            'citems': cart_items,
            'count': cart_count,
            'cart_total': sum(item.product.price * item.quantity for item in cart_items)
        })
        # Render the checkout.html template with the context data
        return render(request, 'checkout.html', context)
    else:
        # If the user is not authenticated, return an error
        return error_403(request)


def profile(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get all categories
        categories = Category.objects.all()
        # Prepare the context dictionary with the user's basic information and categories
        context = {
            'fname': request.user.first_name,
            'lname': request.user.last_name,
            'email': request.user.email,
            'categories': categories,
        }
        # Check if the user's address is set, and add it to the context if present
        if request.user.street != None:
            context.update({
                'street': request.user.street,
                'city': request.user.city,
                'state': request.user.state,
                'zipcode': request.user.zipcode,
                'phone': request.user.phone_number
            })
        # Get the user's orders and prefetch the related order items
        orders = Order.objects.filter(
            user=request.user).prefetch_related('orderitem_set')
        # Fetch order items for each order and create a list of dictionaries
        orders_with_items = [
            {
                'order': order,
                'items': order.orderitem_set.all()
            }
            for order in orders
        ]
        # Add the orders with items to the context
        context['orders_with_items'] = orders_with_items
        # Get the cart items and count for the current user
        cart_items, cart_count = get_cart_items_and_count(request.user)
        # Update the context dictionary with the cart items and count
        context.update({
            'citems': cart_items,
            'count': cart_count
        })
        # Render the profile.html template with the context data
        return render(request, 'profile.html', context)
    else:
        # If the user is not authenticated, return an error
        return error_403(request)


def update_profile(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the request method is POST
        if request.method == 'POST':
            # Get the form data from the POST request
            name = request.POST.get('name')
            fname = name.split()[0]
            lname = " ".join(name.split()[1:])
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            if request.POST.get('password') != "********":
                password = request.POST.get('password')
            street = request.POST.get('street')
            state = request.POST.get('state')
            city = request.POST.get('city')
            zipcode = request.POST.get('zipcode')
            # Update the user's profile with the new data
            user = request.user
            user.first_name, user.last_name = fname, lname
            user.email = email
            user.phone_number = phone
            if request.POST.get('password') != "********":
                user.set_password(password)
            user.street = street
            user.state = state
            user.city = city
            user.zipcode = zipcode
            user.save()
            # Return a JSON response indicating success
            if request.POST.get('password') != "********":
                messages.info(
                    request, "Your profile has been updated. Login Again to see changes.")
                return redirect('Sign In')
            else:
                messages.info(request, "Your profile has been updated.")
                return redirect('Profile')
        else:
            # Return a JSON response indicating an error if the request method is not POST
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    else:
        # If the user is not authenticated, return an error
        return error_403(request)


@csrf_exempt
def payment(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the key and salt from the settings
        key = settings.PAYMENT_KEY
        salt = settings.PAYMENT_SALT

        # Generate a transaction ID
        txn_id = hashlib.sha256(
            str(time.time()).encode('utf-8')).hexdigest()[:12]

        # Get the payment amount, product info, email, and phone from the request
        amount = request.session.get('amount')
        product_info = "PRODUCT INFO"
        email = request.user.email
        phone = str(request.user.phone_number)
        # Generate a hash string
        hash_sequence = f"{key}|{txn_id}|{amount}|{product_info}|{request.user.first_name}|{email}|||||||||||{salt}"
        hashed = hashlib.sha512(
            hash_sequence.encode('utf-8')).hexdigest().lower()
        # Set the success and failure URLs
        surl = request.build_absolute_uri('/payment/success/')
        furl = request.build_absolute_uri('/payment/failure/')
        # Set the PayU data
        payu_data = {
            'key': key,
            'txnid': txn_id,
            'amount': amount,
            'productinfo': product_info,
            'firstname': request.user.first_name,
            'email': email,
            'phone': phone,
            'surl': surl,
            'furl': furl,
            'hash': hashed,
        }
        # Render the payment form with the PayU data
        return render(request, 'payment_form.html', {'payu_data': payu_data})
    else:
        # If the user is not authenticated, return an error
        return error_403(request)


def paycheck(request, operation):
    if request.user.is_authenticated:
        if operation == "success":
            # Create an Order with the 'Processing' status
            order = Order(user=request.user, status='Processing')
            order.save()
            # Create OrderItems from CartItems
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            # Calculate the total amount for the order
            total_amount = 0
            for item in cart_items:
                order_item = OrderItem(
                    order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                order_item.save()
                total_amount += item.product.price * item.quantity
            # Create a Payment record with the calculated total amount
            payment = Payment(order=order, payment_method=request.POST.get(
                'payment_method'), amount=total_amount)
            payment.save()
            # Clear CartItems after a successful order
            cart_items.delete()
            # Send a success message and redirect URL in JSON response
            response_data = {
                'message': 'Order submitted successfully',
                'redirect_url': '/',
            }
            messages.success(request, "Order placed successfully.")
            return JsonResponse(response_data)
        elif operation == "failure":
            # Send a failure message and redirect URL in JSON response
            response_data = {
                'message': 'Order submission failed',
                'redirect_url': '/',
            }
            messages.error(request, "Order submission failed.")
            return JsonResponse(response_data)
    else:
        return error_403(request)


def order_confirmation(request):
    """
    This function handles order confirmation by creating an Order, OrderItems, and a Payment record.
    It also updates the user's address and clears the CartItems after a successful order.
    :param request: The request object
    :return: JsonResponse containing a success message and redirect URL, or an error message for invalid request method
    """
    # Check if the request method is POST
    if request.method == 'POST':
        # Get form data from POST request
        address1 = request.POST.get('address1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment')
        # Update the user's address and phone number
        user = request.user
        user.street = address1
        user.city = city
        user.state = state
        user.zipcode = zip
        user.phone_number = phone
        user.save()
        if payment_method == 'COD':
            # Create an Order with the 'Processing' status
            order = Order(user=user, status='Processing')
            order.save()
            # Create OrderItems from CartItems
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            # Calculate the total amount for the order
            total_amount = 0
            for item in cart_items:
                order_item = OrderItem(
                    order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                order_item.save()
                total_amount += item.product.price * item.quantity
                item.product.stock_count -= item.quantity
                item.product.save()

            # Create a Payment record with the calculated total amount
            payment = Payment(
                order=order, payment_method=payment_method, amount=total_amount)
            payment.save()
            # Clear CartItems after a successful order
            cart_items.delete()
            # Send a success message and redirect URL in JSON response
            response_data = {
                'message': 'Order submitted successfully',
                'redirect_url': '/',
            }
            messages.success(request, "Order placed successfully.")
            return HttpResponse(status=200)
        elif payment_method == 'PayU':
            request.session['amount'] = str(request.POST.get('amount'))+".00"
            # return redirect(reverse('Payment'))
            return HttpResponse(status=302)
        else:
            response_data = {
                'message': 'Invalid payment method',
            }
            return JsonResponse(response_data, status=400)


def error_403(request):
    return render(request, '403.html', status=403)
