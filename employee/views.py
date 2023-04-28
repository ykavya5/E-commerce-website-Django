from django.shortcuts import render,redirect
import logging
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
import mysql.connector
from .forms import ContactForm
from django.core.mail import send_mail 
from .models import Daily
from .models import Payment
from .models import Order
from .models import c_reg
from .models import Products
from .models import Category
from .models import Od
from .models import Dailysheet
from .models import Sadd, Orders, Ohd, Queries
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import smtplib,ssl
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth import authenticate, login
# Create your views here.
def registration(request):
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        ) 
        mycursor =conn.cursor()
        #retrive post details       
        #name=request.POST['name'] 
        username=request.POST['username']
        password=request.POST['password']     
        email=request.POST['email']
        phoneno=request.POST['phone']
        address=request.POST['address']       
        mycursor.execute("insert into customer_reg (username,password,phoneno,address,email) values('"+username+"','"+password+"','"+str(phoneno)+"','"+address+"','"+email+"')")
        conn.commit()
        return redirect('cust_login')
    else:
        return render(request,'registration.html')
def cust_login(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        
        )
        mycursor = conn.cursor()
        #retrive post details       
        
        uname=request.POST['username']
        pwd=request.POST['password']     
           
        mycursor.execute("select * from customer_reg where username='"+uname+"' and password='"+pwd+"'")
        result=mycursor.fetchone()
        if(result!=None):
            request.session['username'] = uname
            #return render(request, 'cust_index.html', {"username" : uname})
            return redirect('cust_index')
            
        else:
            return render(request,'cust_login.html',{'status':'invalid credentials'})    
    else:
        return render(request,'cust_login.html')

def login(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        
        )
        mycursor = conn.cursor()
        #retrive post details       
        
        uname=request.POST['username']
        pwd=request.POST['password']     
        mycursor.execute("select * from admin_login where username='"+uname+"' and password='"+pwd+"'")
        result=mycursor.fetchone()
        if(result!=None):
            request.session['username'] = uname
            return redirect( 'index1')
           # redirect('index1')
        else:
            return render(request,'login.html',{'status':'invalid credentials'})    
    else:
        return render(request,'login.html')

def index(request):
    if request.method == 'GET':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mmtc"
                )
            mycursor =conn.cursor()
            mycursor.execute("select * from product_details")
            result=mycursor.fetchall()
            d=[]
            for row in result:
                obj=Products()
                obj.product_id=row[0]
                obj.product_name=row[1]
                obj.price=row[2]
                obj.image=row[3]
                obj.prod_size=row[4]
                obj.prod_status=row[5]
                obj.category_id=row[6]
                d.append(obj)
    return render(request, 'index.html',{'pro': d}) 
   
def logout(request):
    try:
        del request.session['username']
        request.session.modified = True
        return render(request,'index.html') 
    except KeyError:
        return redirect('login')  
def cust_logout(request):
    try:
        if 'username' in request.session:
            del request.session['username']
        if 'cartlist' in request.session:
            del request.session['cartlist']
        request.session.modified = True
        return redirect('index') 
    except KeyError:
        return redirect('login')  
def shop(request):
    if request.method == 'GET':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mmtc"
                )
            mycursor =conn.cursor()
            mycursor.execute("select * from product_details")
            result=mycursor.fetchall()
            d=[]
            for row in result:
                obj=Products()
                obj.product_id=row[0]
                obj.product_name=row[1]
                obj.price=row[2]
                obj.image=row[3]
                obj.prod_size=row[4]
                obj.prod_status=row[5]
                obj.category_id=row[6]
                d.append(obj) 
            if "search_name" in request.GET:
                search_name = request.GET["search_name"]
                mycursor.execute("SELECT * FROM product_details WHERE product_name LIKE '%{}%'".format(search_name))
                result = mycursor.fetchall()
                search_results = []
                for row in result:
                    obj = Products()
                    obj.product_id = row[0]
                    obj.product_name = row[1]
                    obj.price = row[2]
                    obj.image = row[3]
                    obj.prod_size = row[4]
                    obj.prod_status = row[5]
                    obj.category_id = row[6]
                    search_results.append(obj)
                return render(request, 'shop.html', { 'pro': search_results, 'search_name': search_name})
            return render(request,"shop.html",{'pro':d})

def shopc(request):
    if "username" in request.session:
        uname = request.session['username']
        if request.method == 'GET':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mmtc"
            )
            mycursor = conn.cursor()
            mycursor.execute("select * from product_details")
            result = mycursor.fetchall()
            d = []
            for row in result:
                obj = Products()
                obj.product_id = row[0]
                obj.product_name = row[1]
                obj.price = row[2]
                obj.image = row[3]
                obj.prod_size = row[4]
                obj.prod_status = row[5]
                obj.category_id = row[6]
                d.append(obj)

            mycursor.execute("select * from product_category")
            result = mycursor.fetchall()
            f = []
            for row in result:
                obj = Category()
                obj.category_id = row[0]
                obj.category_name = row[1]
                f.append(obj)

            if "search_name" in request.GET:
                search_name = request.GET["search_name"]
                mycursor.execute("SELECT * FROM product_details WHERE product_name LIKE '%{}%'".format(search_name))
                result = mycursor.fetchall()
                search_results = []
                for row in result:
                    obj = Products()
                    obj.product_id = row[0]
                    obj.product_name = row[1]
                    obj.price = row[2]
                    obj.image = row[3]
                    obj.prod_size = row[4]
                    obj.prod_status = row[5]
                    obj.category_id = row[6]
                    search_results.append(obj)
                return render(request, 'shopc.html', {'cat': f, 'pro': search_results, 'search_name': search_name})
            
            return render(request, 'shopc.html', {'cat': f,'pro': d})
    else:
        return render(request,'cust_login.html')    

     

def queries(request):
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        ) 
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )

        mycursor =conn.cursor()
        mycursor.execute("select * from contact")
        result=mycursor.fetchall()
        p=[]
        for row in result:
            obj=Queries()
            obj.cust_id=row[0]
            obj.name=row[1]
            obj.email=row[2]
            obj.subject=row[3]
            obj.message=row[4]
            p.append(obj)
    return render(request,'queries.html',{'q':p})           


def index1(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
    mycursor=conn.cursor()
    mycursor.execute("select count(cust_id) from customer_reg")
    result=mycursor.fetchone()[0]
    print(result)  
    mycursor.execute("select count(order_id) from orders_list")
    result1=mycursor.fetchone()[0]
    print(result1)      
        

    return render(request,"index1.html",{'ocount':result1,'cr':result})
def mens_wear(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
    mycursor =conn.cursor()
    mycursor.execute("select * from product_details where category_id=2 ")
    result=mycursor.fetchall()
    d=[]
    for row in result:
        obj=Products()
        obj.product_id=row[0]
        obj.product_name=row[1]
        obj.price=row[2]
        obj.image=row[3]
        obj.prod_size=row[4]
        obj.prod_status=row[5]
        d.append(obj)
    return render(request, 'girlswear.html', {'pro': d})
def mens_wear1(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
    mycursor =conn.cursor()
    mycursor.execute("select * from product_details where category_id=2 ")
    result=mycursor.fetchall()
    d=[]
    for row in result:
        obj=Products()
        obj.product_id=row[0]
        obj.product_name=row[1]
        obj.price=row[2]
        obj.image=row[3]
        obj.prod_size=row[4]
        obj.prod_status=row[5]
        d.append(obj)
    return render(request, 'girlswear1.html', {'pro': d})
def girlswear(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
    mycursor =conn.cursor()
    mycursor.execute("select * from product_details where category_id=1 ")
    result=mycursor.fetchall()
    d=[]
    for row in result:
        obj=Products()
        obj.product_id=row[0]
        obj.product_name=row[1]
        obj.price=row[2]
        obj.image=row[3]
        obj.prod_size=row[4]
        obj.prod_status=row[5]
        d.append(obj)
    return render(request, 'girlswear.html', {'pro': d})
def girlswear1(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
    mycursor =conn.cursor()
    mycursor.execute("select * from product_details where category_id=1 ")
    result=mycursor.fetchall()
    d=[]
    for row in result:
        obj=Products()
        obj.product_id=row[0]
        obj.product_name=row[1]
        obj.price=row[2]
        obj.image=row[3]
        obj.prod_size=row[4]
        obj.prod_status=row[5]
        d.append(obj)
    return render(request, 'girlswear1.html', {'pro': d})
def kidswear(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
    mycursor =conn.cursor()
    mycursor.execute("select * from product_details where category_id=3 ")
    result=mycursor.fetchall()
    d=[]
    for row in result:
        obj=Products()
        obj.product_id=row[0]
        obj.product_name=row[1]
        obj.price=row[2]
        obj.image=row[3]
        obj.prod_size=row[4]
        obj.prod_status=row[5]
        d.append(obj)
    return render(request, 'girlswear.html',{'pro':d})
def kidswear1(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
    mycursor =conn.cursor()
    mycursor.execute("select * from product_details where category_id=3 ")
    result=mycursor.fetchall()
    d=[]
    for row in result:
        obj=Products()
        obj.product_id=row[0]
        obj.product_name=row[1]
        obj.price=row[2]
        obj.image=row[3]
        obj.prod_size=row[4]
        obj.prod_status=row[5]
        d.append(obj)
    return render(request, 'girlswear1.html',{'pro':d})

def add_cart(request,product_id):
    if "username" in request.session:
        uname = request.session['username']        
        x=[]
        if('cartlist' not in request.session):
            x.append(product_id)
            request.session['cartlist']=x                
        else:
            x=list(request.session['cartlist'])
            print('in add cart ',x)
            if(product_id not in x):
                x.append(product_id) 
                request.session['cartlist']=x
        print(x)
        return redirect('shopc')
    else:
        return render(request,'login.html')
def remove(request,product_id):
    if "username" in request.session:
        uname= request.session['username']
        x=list(request.session['cartlist'])
        if(product_id in x):
            x.remove(product_id)
            request.session['cartlist']=x
        print(x)
        return redirect('cart')
    else:
        return render(request,'login.html')


def cart(request):
    if "username" in request.session:
        uname = request.session['username']       
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mmtc"
            )
        mycursor=conn.cursor()
        #getting customer id based on the username
        mycursor.execute("SELECT cust_id FROM customer_reg WHERE username='" + uname + "'")
        cust_id = mycursor.fetchone()[0]
        p=[]
        print('hi')
        if('cartlist' in request.session):
            p=list(request.session['cartlist'])
        print(p)
        d=[]
        if not p:
            return render(request, "cart.html", {"empty": True})
        else:
            print("pid:",p)
            for  aa in p:
                print("loop pid",p)
                mycursor.execute("select * from product_details where product_id='"+str(aa)+"'")
                print(" after select pid", p)
                result=mycursor.fetchall()
                for row in result:
                    obj=Products()
                    obj.product_id=row[0]
                    obj.product_name=row[1]
                    obj.price=row[2]
                    obj.image=row[3]
                    obj.cust_id = cust_id
                    d.append(obj)
            return render(request,"cart.html",{'pro':d})
    else:
        return render(request,'cust_login.html')
def check(request):
    if "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mmtc"
        )
        mycursor = conn.cursor()
        p = []
        print(request.POST['finalsub'])
        if 'cartlist' in request.session:
            p = list(request.session['cartlist'])
        if p:
            mycursor.execute("SELECT cust_id FROM customer_reg WHERE username='" + uname + "'")
            cust_id = mycursor.fetchone()[0]
            d = []
            total_price = 0
            grand_total = 0
            shipping_charge = '10'
            finalsub = str(request.POST['finalsub'])
            print("finalsub:",finalsub)
            finalsubparts = finalsub.split('@')
            pids = finalsubparts[0]
            qs = finalsubparts[1]
            total=finalsubparts[2]
            size=finalsubparts[3]
            stotal=str(total)
            print(pids, qs, total)
            pidsplit=pids.split(",")
            qssplit = qs.split(',')
            sizesplit=size.split(",")
            u = 0
            today=datetime.now()
            print(today)
            b=str(today)
            print(b)
            mycursor.execute("INSERT INTO orders_list (cust_id, total_amount,order_date) VALUES (%s, %s,%s)", (cust_id, 0,b))
            mycursor.execute("SELECT LAST_INSERT_ID()")
            order_id = mycursor.fetchone()[0]
            for aa in pidsplit:
                mycursor.execute("SELECT * FROM product_details WHERE product_id='" + str(aa) + "'")
                result = mycursor.fetchone()
                if result:
                    obj = Products()
                    obj.product_id = result[0]
                    obj.product_name = result[1]
                    obj.price = result[2]
                    obj.cust_id = cust_id
                    obj.order_id = order_id
                    #u=0
                    obj.quantity = int(qssplit[u])
                    obj.size = (sizesplit[u])
                    u += 1
                    obj.total_price = obj.price * obj.quantity
                    #shipping_charge = 10
                    grand_total = int(stotal) + int(shipping_charge)
                    #grand_total += obj.grand_total
                    print(grand_total)
                    d.append(obj)
                    # Insert the cart item with quantity
                    mycursor.execute("INSERT INTO order_details (cust_id,order_id, product_id, quantity, total, size) VALUES (%s, %s, %s, %s, %s, %s)", (cust_id, order_id, obj.product_id, obj.quantity, obj.total_price, obj.size ))
            #conn.commit()
            mycursor.execute("UPDATE orders_list SET total_amount=%s WHERE order_id=%s", (grand_total, order_id))
            conn.commit()
            del request.session['cartlist']
            context = {
                'pro': d,
                'total':total,
                'total_price': total_price,
                'shipping_charge': shipping_charge,
                'grand_total': grand_total
            }
            conn.commit()          
            return render(request,'checkout.html',context)
        else:
            return redirect('cart')   
    else:
        return render(request, 'cust_login.html')
def checkout(request):
    uname=''
    print('im in checkout ')
    if "username" in request.session:
        uname = request.session['username']                  
    else:
        return render(request,'cust_login.html')
    if  request.method=='POST':
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        ) 
        mycursor = conn.cursor()

        # retrieve name from session
        uname = request.session.get('username')

        # retrieve customer ID from customer_reg table
        mycursor.execute("SELECT cust_id FROM customer_reg WHERE username = %s", (uname,))
        cust_id = mycursor.fetchone()[0]
        
        # retrieve post details      
        
        name= request.POST['name']
        print(name)
        phone = request.POST['phone']
        print(phone)
        address = request.POST['address']
        print(address)
        city = request.POST['city']
        print(city)
        state = request.POST['state']
        print(state)
        zcode = request.POST['zcode']
        print(zcode)
        
        query = "INSERT INTO shippingaddress(cust_id, name, phone, address, city, state, zipcode ) VALUES ('"+str(cust_id)+"', '"+name+"', '"+phone+"', '"+address+"', '"+city+"', '"+state+"','"+zcode+"')"
        
        mycursor.execute(query)
        conn.commit()
        return render(request, 'cust_payment.html')    
    
    return render(request, 'checkout.html')  
def cust_payment(request):
    if 'username' in request.session:
        uname=request.session['username']
        if request.method=='POST':
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mmtc"
            )
            mycursor = conn.cursor()
            name=request.POST['name']     
            cvv=request.POST['cvv']
            account_number=request.POST['account_number'] 
            query = "SELECT * FROM banking_details WHERE name=%s AND cvv=%s AND account_number=%s"
            values = (name, cvv, account_number)
            mycursor.execute(query, values)
            result=mycursor.fetchone()
            print(result)
            mycursor.execute("SELECT cust_id FROM customer_reg WHERE username='" + uname + "'")
            cust_id = mycursor.fetchone()[0]
            mycursor.execute(" SELECT order_id from orders_list order by order_id desc limit 1")
            order_id=mycursor.fetchone()[0]
            mycursor.execute("SELECT ship_id from shippingaddress where cust_id='"+str(cust_id)+"' order by ship_id desc limit 1")
            ship_id = mycursor.fetchone()[0]
            if(result!=None):
                alert_message = "CVV and account number matched successfully!"
                status=1
                mycursor.execute("UPDATE orders_list SET status=%s,ship_id=%s WHERE order_id=%s", (status,ship_id,order_id))
                conn.commit()
                return render(request, "ordersuccess.html", {'status': 'success', 'alert_message': alert_message})
            else:
                return render(request, "cust_payment.html")
    else:
        return render(request,"cust_login.html")          
def ordersuccess(request): 
    return render(request,"ordersuccess.html") 

def Ordershistory(request): 
    if 'username' in request.session:
        uname=request.session['username']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mmtc"
            )
        mycursor=conn.cursor()
        mycursor.execute("SELECT cust_id FROM customer_reg WHERE username='" + uname + "'")
        cust_id = mycursor.fetchone()[0]
        mycursor.execute("SELECT order_id,order_date,total_amount,order_status FROM `orders_list` where cust_id='"+str(cust_id)+"' and status ='1' ")
        result=mycursor.fetchall()
        d=[]
        for row in result:
            obj=Orders()
            obj.order_id=row[0]
            obj.order_date=row[1]
            obj.total_amount=row[2]
            obj.order_status=row[3]
            #obj.product_id=row[3]
            d.append(obj)
        return render(request,"Ordershistory.html",{'oh':d})
    else:
        return render(request,"cust_login.html") 

def detailed_orderhistory(request,order_id):
    if 'username' in request.session:
        uname=request.session['username']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mmtc"
            )
        mycursor=conn.cursor()
        mycursor.execute("SELECT cust_id FROM customer_reg WHERE username='" + uname + "'")
        cust_id = mycursor.fetchone()[0]
        mycursor.execute("SELECT pd.product_id,pd.product_name,pd.image,pd.prod_size,pd.description FROM `order_details` od inner join product_details pd on od.product_id=pd.product_id where od.order_id='"+order_id+"'")
        result=mycursor.fetchall()
        d=[]
        for row in result:
            obj=Ohd()
            obj.product_id=row[0]
            obj.product_name=row[1]
            obj.image=row[2]
            obj.prod_size=row[3] 
            obj.description=row[4]
            d.append(obj)
        return render(request,"detailed_orderhistory.html",{'od':d})
    else:
        return render(request,"cust_login.html") 
    
def contact(request):
    if "username" in request.session:
        uname = request.session['username']
        if request.method=='POST':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mmtc"
                )
            mycursor =conn.cursor()
            name=request.POST['name']     
            email=request.POST['email']
            subject=request.POST['subject']
            message=request.POST['message']
            mycursor.execute("SELECT cust_id FROM customer_reg WHERE username='" + uname + "'")
            cust_id = mycursor.fetchone()[0]
            mycursor.execute("INSERT INTO contact(cust_id, name, email, subject, message ) VALUES ('"+str(cust_id)+"', '"+name+"', '"+email+"', '"+subject+"', '"+message+"')" )
            conn.commit()
            messages.success(request, 'Your message has been sent successfully!')
            return render(request, 'contact.html', {'message': 'Your message has been sent successfully!'})
    return render(request, 'contact.html')
def detail(request, product_id):
    if "username" in request.session:
        uname = request.session['username']
        if request.method == 'GET':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mmtc"
            )
            mycursor = conn.cursor()
            mycursor.execute("select * from product_details where product_id = %s", (product_id,))
            result = mycursor.fetchall()
            d = []
            for row in result:
                obj = Products()
                obj.product_id = row[0]
                obj.product_name = row[1]
                obj.price = row[2]
                obj.image = row[3]
                obj.prod_status = row[5]
                obj.category_id = row[6]
                obj.description = row[7]
                d.append(obj)
            conn.close()
            return render(request, "detail.html", {'pro': d})
    else:
        return render(request, 'cust_login.html')
  
def detail1(request,product_id):
        if request.method == 'GET':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mmtc"
                )
            mycursor =conn.cursor()
            mycursor.execute("select * from product_details where product_id = %s", (product_id,))
            result=mycursor.fetchall()
            d=[]
            for row in result:
                obj=Products()
                obj.product_id=row[0]
                obj.product_name=row[1]
                obj.price=row[2]
                obj.image=row[3]
                obj.prod_size=row[4]
                obj.prod_status=row[5]
                obj.category_id=row[6]
                obj.description=row[7]
                d.append(obj) 
        return render(request,"detail1.html",{'pro': d})  
   

def cust_index(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
    )
    mycursor = conn.cursor()
    mycursor.execute("select * from product_details")
    result = mycursor.fetchall()
    d = []
    for row in result:
        obj = Products()
        obj.product_id = row[0]
        obj.product_name = row[1]
        obj.price = row[2]
        obj.image = row[3]
        obj.prod_size = row[4]
        obj.prod_status = row[5]
        obj.category_id = row[6]
        d.append(obj)
    return render(request, 'cust_index.html', {'pro': d})


def customer(request): 
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        ) 
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )

        mycursor =conn.cursor()
        mycursor.execute("select * from customer_reg")
        result=mycursor.fetchall()
        p=[]
        for row in result:
            obj=c_reg()
            obj.cust_id=row[0]
            obj.username=row[1]
            obj.password=row[2]
            obj.phoneno=row[3]
            obj.address=row[4]
            obj.email=row[5]
            p.append(obj)
        return render(request, 'customer.html', {'reg': p})
def order_details(request):
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        ) 
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )

        mycursor =conn.cursor()
        mycursor.execute("SELECT * FROM `order_details` od inner join orders_list ol on ol.order_id=od.order_id where ol.status='1'")
        result=mycursor.fetchall()
        p=[]
        for row in result:
            obj=Od()
            obj.orderdetails_id=row[0]
            obj.cust_id=row[1]
            obj.product_id=row[3]
            obj.quantity=row[4]
            obj.size=row[6]
            p.append(obj)
    return render(request,'order_details.html',{'od': p})
def categories(request):
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        ) 
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
        mycursor =conn.cursor()
        mycursor.execute("select * from product_category")
        result=mycursor.fetchall()
        d=[]
        for row in result:
            obj=Category()
            obj.category_id=row[0]
            obj.category_name=row[1]
            d.append(obj)
    if messages.get_messages(request):
        messages_to_html = [m for m in messages.get_messages(request)]
        return render(request, 'categories.html', {'cat': d, 'messages': messages_to_html})
    else:
        return render(request, 'categories.html', {'cat': d}) 
def del_categories(request,category_id):
    conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mmtc"    
    )
    query=conn.cursor()
    query.execute("DELETE FROM product_category where category_id='"+category_id+"'")
    conn.commit()
    messages.success(request, 'Category deleted successfully.')
    return redirect('categories')
def products(request):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )

        mycursor =conn.cursor()
        mycursor.execute("select * from product_details")
        result=mycursor.fetchall()
        d=[]
        for row in result:
            obj=Products()
            obj.product_id=row[0]
            obj.product_name=row[1]
            obj.price=row[2]
            obj.image=row[3]
            obj.prod_size=row[4]
            obj.prod_status=row[5]
            obj.category_id=row[6]
            obj.description=row[7] 
            d.append(obj)
        if messages.get_messages(request):
            messages_to_html = [m for m in messages.get_messages(request)]
            return render(request, 'products.html', {'pro': d, 'messages': messages_to_html})
        return render(request, 'products.html', {'pro': d})
def del_product(request,product_id):
    conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mmtc"     
    )
    query=conn.cursor()
    query.execute("DELETE FROM product_details where product_id='"+product_id+"'")
    conn.commit()
    messages.success(request, 'Product deleted successfully.')
    return redirect('products')
def edit_products(request,product_id):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'mmtc'
        )
        query = conn.cursor()
        product_name=request.POST['product_name']
        price=request.POST['price']
        #myfile=request.POST['myfile']
        prod_size=request.POST['prod_size']
        prod_status=request.POST['prod_status']
        category_id=request.POST['category_id']
        description=request.POST['description'] 
            
        
        query.execute("update product_details set product_name='"+product_name+"',price='"+price+"',prod_size='"+prod_size+"',prod_status='"+prod_status+"',category_id='"+category_id+"', description='"+description+"'  where product_id='"+product_id+"'")
        conn.commit()
        messages.success(request, 'Product edited successfully.')
        return redirect('products')
    else:
            
        conn= mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mmtc'
        )
        mycursor = conn.cursor()
        mycursor.execute("select * from product_details where product_id='"+product_id+"'")
        result=mycursor.fetchall()
        d=[]
        product_details=None
        for row in result:
            obj=Products()
            obj.product_id=row[0]
            obj.product_name=row[1]
            obj.price=row[2]
            obj.image=row[3]
            obj.prod_size=row[4]
            obj.prod_status=row[5]
            obj.category_id=row[6]
            obj.description=row[7]
            d.append(obj)
        return render(request, 'edit_products.html', {'pd': d})  
          
# dailysheet code
def dailysheet(request):
    # create a connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
    )

    mycursor = conn.cursor()

    # execute a SELECT statement on the database
    mycursor.execute("SELECT od.product_id,ol.order_date,sum(od.quantity) FROM `orders_list` ol inner join order_details od on ol.order_id=od.order_id group by product_id,order_date")

    # fetch the result of the SELECT statement
    result = mycursor.fetchall()

    # create a new cursor object for selecting from dailysheet table
    select_cursor= conn.cursor()
    select_cursor.execute("SELECT product_id, date FROM dailysheet")
    re1 = set(select_cursor.fetchall())

    # create a new cursor object for inserting into dailysheet table
    insert_cursor = conn.cursor()

    # iterate through the query result and insert into dailysheet table if not already exists
    for row in result:
        product_id = row[0]
        order_date = row[1]
        quantity = row[2]
        if (product_id, order_date) not in re1:
            insert_cursor.execute("INSERT INTO dailysheet (product_id, date, outflow) VALUES (%s, %s, %s)", (product_id, order_date, quantity))
            re1.add((product_id, order_date))

    # commit the changes to the database
    conn.commit()

    # create a list of dictionaries for the result data
    d = [{'product_id': row[0], 'order_date': row[1], 'quantity': row[2]} for row in result]
    # create a new cursor object for selecting from dailysheet table
    select_cursor = conn.cursor()

    # execute a SELECT statement on the dailysheet table
    select_cursor.execute("SELECT * FROM dailysheet")

    # fetch the result of the SELECT statement
    result = select_cursor.fetchall()

    # create a list of Dailysheet objects from the query result
    d = []
    for row in result:
        obj = Dailysheet()
        obj.daily_id= row[0]
        obj.product_id = row[1]
        obj.order_date = row[2]
        obj.inflow=row[3]
        obj.outflow = row[4]
        obj.rem=row[5]
        d.append(obj)
        
    #print(d)
    if messages.get_messages(request):
            messages_to_html = [m for m in messages.get_messages(request)]
            return render(request, 'dailysheet.html', {'da': d, 'messages': messages_to_html})

    # return the rendered HTML page with the list of Dailysheet objects
    return render(request, 'dailysheet.html', {'da': d})

@csrf_exempt
def save_stock(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mmtc"
        )
        mycursor = conn.cursor()
        data = json.loads(request.POST.get('fsave'))
        for row in data:
            daily_id = int(row['daily_id'])
            inflow_val = float(row['inflow'])
            rem_val = float(row['remaining'])
            mycursor.execute("UPDATE dailysheet SET inflow=%s, rem=%s WHERE daily_id=%s",
                             (inflow_val, rem_val, daily_id))
            conn.commit()
            messages.success(request, 'Stock details saved successfully.') 

        conn.close()
        return redirect('dailysheet')
    return HttpResponse("This view is only for POST requests.")

       
def orders(request): 
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )
        query = conn.cursor()
        fromdate=request.POST.get('fromdate')
        todate=request.POST.get('todate')
        query.execute('select * from orders_list where order_date between "'+str(fromdate)+'" and "'+str(todate)+'" and status="1"  ')
        searchresult=query.fetchall()
        p=[]
        for row in searchresult:
            obj=Order()
            obj.order_id=row[0]
            obj.cust_id=row[1]
            obj.total_amount=row[2]
            obj.order_date=row[3]
            obj.status=row[4]
            obj.ship_id=row[5]
            obj.order_status=row[6]
            p.append(obj)
        return render(request, 'orders.html', {'o': p}) 
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mmtc"
        )

        mycursor =conn.cursor()
        mycursor.execute("select * from orders_list where status='1' ")
        result=mycursor.fetchall()
        p=[]
        for row in result:
            obj=Order()
            obj.order_id=row[0]
            obj.cust_id=row[1]
            obj.total_amount=row[2]
            obj.order_date=row[3]
            obj.status=row[4]
            obj.ship_id=row[5]
            obj.order_status=row[6]
            p.append(obj)
        if messages.get_messages(request):
            messages_to_html = [m for m in messages.get_messages(request)]
            return render(request, 'orders.html', {'o': p, 'messages': messages_to_html})
        return render(request, 'orders.html', {'o': p})
def edit_order(request, order_id):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'mmtc'
        )
        query = conn.cursor()
        order_status=request.POST['os']     
        
        query.execute("update orders_list set order_status='"+order_status+"'  where order_id='"+order_id+"'")
        conn.commit()
        messages.success(request, 'Status edited successfully.')
        return redirect('orders')
    else:
            
        conn= mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mmtc'
        )
        mycursor = conn.cursor()
        mycursor.execute("select * from orders_list where order_id='"+order_id+"'")
        result = mycursor.fetchall()
        w=[] 
        for row in result:
            obj=Order()
            obj.order_id=row[0]
            obj.cust_id=row[1]
            obj.total_amount=row[2]
            obj.order_date=row[3]
            obj.status=row[4]
            obj.ship_id=row[5]
            #obj.order_status[6]
            w.append(obj)
        #print(e)
        
        return render(request, 'edit_order.html', {'o': w})     

        
def add_categories(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'mmtc'
        )
        query = conn.cursor()
        category_id=request.POST['category_id']
        category_name=request.POST['category_name']     
        query.execute("insert into product_category(category_id,category_name)values('"+category_id+"','"+category_name+"')")
        conn.commit()
        messages.success(request, 'Category added successfully.')

        return redirect('categories')
    
    else:
        return render(request, 'add_categories.html')
def edit_category(request,category_id):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'mmtc'
        )
        query = conn.cursor()
        category_name=request.POST['catname']     
        
        query.execute("update product_category set category_name='"+category_name+"'  where category_id='"+category_id+"'")
        conn.commit()
        messages.success(request, 'Category updated successfully.')
        return redirect('categories')
    else:
            
        conn= mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mmtc'
        )
        mycursor = conn.cursor()
        mycursor.execute("select * from product_category where category_id='"+category_id+"'")
        result = mycursor.fetchall()
        w=[] 
        for row in result:
            obj= Category()
            obj.category_id=row[0]
            obj.category_name=row[1]  
            w.append(obj)
        #print(e)
        
        return render(request, 'edit_category.html', {'cat': w})     

def add_newproduct(request):
    if request.method=='POST' and request.FILES['myfile']:
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'mmtc'
        )
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        query = conn.cursor()
        product_id=request.POST['product_id']
        product_name=request.POST['product_name']     
        price=request.POST['price']
        prod_size=request.POST['prod_size'] 
        prod_status=request.POST['prod_status']  
        category_id=request.POST['category_id']
        description=request.POST['description']
        query.execute("insert into product_details(product_id,product_name,price,image,prod_size,prod_status,category_id,description)values('"+product_id+"','"+product_name+"','"+price+"','"+filename+"','"+prod_size+"','"+prod_status+"','"+category_id+"','"+description+"')")
        conn.commit()
        messages.success(request, 'Product added successfully.')
        return redirect('products')
    
    else:
        return render(request, 'add_newproduct.html')
def edit_orderdetails(request,orderdetails_id): 
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'mmtc'
        )
        query = conn.cursor()
        order_id=request.POST['order_id']  
        product_id=request.POST['product_id']
        quantity=request.POST['quantity']  
        
        query.execute("update order_details set order_id='"+order_id+"',product_id='"+product_id+"',quantity='"+quantity+"'  where orderdetails_id='"+orderdetails_id+"'")
        conn.commit()
        return redirect('order_details')
    else:
            
        conn= mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mmtc'
        )
        mycursor = conn.cursor()
        mycursor.execute("select * from order_details where orderdetails_id='"+orderdetails_id+"'")
        result = mycursor.fetchall()
        w=[] 
        for row in result:
            obj= Od()
            obj.orderdetails_id=row[0]
            obj.order_id=row[1] 
            obj.product_id=row[2]  
            obj.quantity=row[3]   
            w.append(obj)
        #print(e)
        
        return render(request, 'edit_orderdetails.html', {'od': w})  

def cust_profile(request):
    if "username" in request.session:
       uname=request.session['username']
       if request.method=='GET':
        conn= mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mmtc'
        )
        mycursor = conn.cursor()
        mycursor.execute("select * from customer_reg where username='"+uname+"'")
        result = mycursor.fetchall()
        w=[] 
        for row in result:
            obj=c_reg()
            obj.cust_id=row[0]
            obj.username=row[1]
            obj.password=row[2]
            obj.phone=row[3]
            obj.address=row[4]
            obj.email=row[5]
            w.append(obj)

       return render(request, 'cust_profile.html',{"username" : uname,'cr':w})
    else:
        return render(request,'cust_login.html')       

def password_recovery(request):

    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mmtc"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['email']

        mycursor.execute("select password from customer_reg where email='"+email+"'")

        result = mycursor.fetchone()
        pwd=str(result)
        if (result != None):
            # SMTP server configuration
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'yk@gmail.com'
# for App Password enable 2-step verification then u can create app password
            smtp_password = 'nifn qdee fofp kxoe'

# Email content
            subject = 'Password recovery'
            body = 'This is a Password recovery email sent from Matha Manikeshwari Trading Company.'+'Your password as per registration is: '+ pwd[2:len(pwd)-3]
            sender_email = 'yk@gmail.com'
            receiver_email = email

# Create a message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            
            return render(request, 'password_recovery.html', {'status': 'Password sent to given mail ID'})
        else:
            return render(request, 'password_recovery.html', {'status': 'Wrong Username!'})
    else:
        return render(request, 'password_recovery.html')     

def banking_register(request):
    if request.method == 'POST':       
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mmtc"
        ) 
        mycursor = conn.cursor()

        # retrieve name from session
        uname = request.session.get('username')

        # retrieve customer ID from customer_reg table
        mycursor.execute("SELECT cust_id FROM customer_reg WHERE username = %s", (uname,))
        cust_id = mycursor.fetchone()[0]
        
        # retrieve post details      
        
        name= request.POST['name']
        cvv = request.POST['cvv']
        account_number = request.POST['account_number']
        
        # use parameterized query to avoid SQL injection
        query = "INSERT INTO banking_details(cust_id, name,  cvv, account_number) VALUES (%s,  %s, %s, %s)"
        values = (cust_id, name,  cvv, account_number)
        mycursor.execute(query, values)
        conn.commit()

        return render(request,"cust_payment.html")
    else:
        return render(request, "banking_register.html")


