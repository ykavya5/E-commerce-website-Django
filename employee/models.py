from django.db import models
# Create your models here.
class Daily:
    daily_id:int
    product_id:int
    prod_name:str
    inflow:str
    outflow:int
    rem:str
    date:str
class Payment:
    payment_id:int
    payment_date:str
    order_id:str
    payment_amount:str
    payment_type:str
class Order:
    order_id:int
    cust_id:str
    total_amount:str
    order_date:str
    status:str
    ship_id:str
    order_status:str

class c_reg:
    cust_id:int
    username:str
    password:str
    phone:int
    address:str
    email:str
class Products:
    product_id:int
    product_name:str
    price:int
    image:str
    size:str
    prod_status:str
    category_id:int
    description:str
class Category:
    category_id:int
    category_name:str
class Od:
    orderdetails_id:int
    cust_id:str
    product_id:int
    quantity:str
    size:str
class Dailysheet:
    daily_id:int
    product_id:str
    inflow:str
    outflow:int
    rem:str
    date:str

class Sadd:
    ship_id:int
    cust_id:str
    order_id:str
    name:str
    phone:int
    address:str
    city:str
    state:str
    zipcode:int

class Orders:
    order_id:int
    cust_id:str
    total_amount:str
    order_date:str
    order_status:str
    product_id:int
class Ohd:
    product_id:int
    product_name:str
    image:str
    prod_size:str
    deacription:str
class Queries:
    cust_id:int
    name:str
    email:str
    subject:str
    message:str 
    




