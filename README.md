# E-commerce-website-Django for Cloth Store 

This project is a web-based Ecommerce site for a cloth store. It consists of two main modules - customer and admin. The admin module is responsible for managing the stock, sales, and customer queries. The customer module allows customers to regiter, login, view products, add them to a cart, place orders, and view their order history. Customers can also contact the store through a contact us page for any queries they may have. All data is stored in a MySQL server.

## Project Structure

The project structure is as follows:

```
ecommerce_site/
├── employee/
│   ├── migrations/
│   ├── _pycache_/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── websiteformathamanikeshwaritradingcompay/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
├── media/
├── templates/
├── manage.py
└── db.sqlite3
```

## Installation

To run this project, you need to have Python 3 installed on your system. You also need to install the following dependencies:

- Django
- MySQL Server
- MySQL Connector for Python

You can install these dependencies using pip. Here's how:

```
pip install django
pip install mysql-connector-python
```

## Usage

To use this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the dependencies as described above.
3. Create a MySQL database and update the `DATABASES` setting in `settings.py` with your database details.
4. Run `python manage.py runserver` to start the development server.
5. Visit `http://localhost:8000/login` to access the admin module and manage stock, sales, and queries.
6. Visit `http://localhost:8000` to access the customer module and view products, add them to a cart, place orders, and view order history.

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request. We welcome contributions from anyone!

## Contact

If you have any questions or comments about this project, please contact at yamsanikavya15@gmail.com 
