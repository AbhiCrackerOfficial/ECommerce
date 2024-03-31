# ECommerce

A Basic Django-powered ecommerce platform with a robust user experience, advanced security features, PayU payment integration, and a powerful admin panel. 

## Features

* **Intuitive Shopping Experience:** Seamless product browsing, detailed product pages, and a streamlined shopping cart.
* **User Accounts:** User signup with OTP verification, password reset functionality, and order history.
* **Secure Transactions:** PayU payment gateway integration for secure online payments. [**Not fully Completed Yet**]
* **Security:** Google reCAPTCHA integration to mitigate bot activity and protect user account actions.
* **Admin Panel:** Extensive management of products, orders, users, and website settings.

## Screenshots

![Product Page](/screenshots/2.png)
*Sigin Page*

![Product Page](/screenshots/4.png)
*Product Page*

![Shopping Cart](/screenshots/5.png)
*Shopping Cart*

![Shopping Cart](/screenshots/7.png)
*Order History*

## Getting Started

### Prerequisites

* Python 3 ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* Django ([https://www.djangoproject.com/download/](https://www.djangoproject.com/download/))
* A PayU merchant account ([https://www.payu.in/](https://www.payu.in/))

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AbhiCrackerOfficial/ECommerce.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ECommerce
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    [**and also setup and .env file with recaptcha, payu, smtp credentials**]

4. Run the migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser (admin):

    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the application at `http://127.0.0.1:8000` in your web browser.

## Usage

- To access the admin panel, go to `http://127.0.0.1:8000/admin` and log in with the superuser credentials created in step 5.
- As an admin, you can manage products, view orders, and perform other administrative tasks.
- Regular users can sign up, log in, browse products, add items to their cart, and complete orders.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---
