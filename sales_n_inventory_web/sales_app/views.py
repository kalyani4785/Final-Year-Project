import datetime
from itertools import product
from multiprocessing.spawn import old_main_modules
from turtle import heading
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth
# from firebase_admin import db
import pyrebase

#Your web app's Firebase configuration
#For Firebase JS SDK v7.20.0 and later, measurementId is optional
firebaseConfig = {
  "apiKey": "AIzaSyBDUx18WYWkbf4v6Xq3oFwZ5FW_p3bC0e4",
  "authDomain": "sales-n-inventory-system-ssvk.firebaseapp.com",
  "databaseURL": "https://sales-n-inventory-system-ssvk-default-rtdb.firebaseio.com",
  "projectId": "sales-n-inventory-system-ssvk",
  "storageBucket": "sales-n-inventory-system-ssvk.appspot.com",
  "messagingSenderId": "370292214222",
  "appId": "1:370292214222:web:4e0427bfc135c92bfc039f",
  "measurementId": "G-5ZSB4CBB0W"
}

# Use a service account (path of file inside _init_ folder)
cred = credentials.Certificate('D:\Final-Year-Project-main\sales_n_inventory_web\_init_sdk/sales-n-inventory-system-ssvk-firebase-adminsdk-ndio1-b8dd43f87f.json')

firebase_admin.initialize_app(cred)
db = firestore.client()
#---------------ends here->

# Create your views here.

#--------------------------------------------------------->
# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()





def index(request):
    return render(request,"Index.html",{'user':authe.current_user})
 




def signIn(request):
    if authe.current_user==None:
      return render(request,"Login.html",{'user':authe.current_user})
    else:
      return render(request,"Home.html",{'user':authe.current_user})
 




def postsignIn(request):
    if authe.current_user==None:
      email=request.POST.get('email')
      pasw=request.POST.get('pass')
      try:
          # if there is no error then signin the user with given email and password
          user=authe.sign_in_with_email_and_password(email,pasw)
      except:
          message="Invalid Credentials! Please Check your email or password."
          return render(request,"Login.html",{"message":message, 'user':authe.current_user})
      session_id=user['idToken']
      # request.session['uid']=str(session_id)
      return render(request,"Home.html",{"email":email, 'user':authe.current_user})
    else:
      return render(request,"Home.html",{'user':authe.current_user})





def logout(request):
    try:
        # del request.session['uid']
        authe.current_user=None
        print("logged out success")
    except:
        pass
    return render(request,"Login.html",{'user':authe.current_user})





def signUp(request):
    return render(request,"Registration.html",{'user':authe.current_user})





def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
     except:
        return render(request, "Registration.html",{'user':authe.current_user})
     return render(request,"Login.html",{'user':authe.current_user})





def reset(request):
	return render(request, "Reset.html",{'user':authe.current_user})





def postReset(request):
	email = request.POST.get('email')
	try:
		authe.send_password_reset_email(email)
		message = "An email to reset password is successfully sent to your registered email."
		return render(request, "Reset.html", {"msg":message, 'user':authe.current_user})
	except:
		message = "Something went wrong, Please check the email you provided is registered or not."
		return render(request, "Reset.html", {"msg":message, 'user':authe.current_user})





def aboutUs(request):
  return render(request, "aboutUs.html", {'user':authe.current_user})





# Sales Dashboard ---------------------------------------->

def newBill(request):
  if authe.current_user==None:
    return render(request,"Login.html",{'user':authe.current_user})
  else:
    if request.method == 'POST':
      print("\n\n\n\n\nPOST method\n\n\n\n\n\n")
      print(request.POST)
      dicti=request.POST
      length=(len(dicti)-2) // 5
      item_name=[]
      brand=[]
      price_per_item=[]
      quantity=[]
      amount=[]
      print(length)

      for i in range(length):
        idx=str(i+1)

        item_name.append(request.POST['item_name'+idx])
        brand.append(request.POST['brand'+idx])
        price_per_item.append(request.POST['price_per_item'+idx])
        quantity.append(request.POST['quantity'+idx])
        amount.append(request.POST['amount'+idx])

      customer_mobile=request.POST["mobile"]

      # print(item_name)
      bill_total=0
      for i in range(len(amount)):
        bill_total+=int(amount[i])

      dataFromForm = {
        'bill_date': datetime.datetime.now(),
        'items': item_name,
        'brands': brand,
        'rates': price_per_item,
        'quantities': quantity,
        'amounts': amount,
        'total_paid': bill_total,
        'customer_mobile': customer_mobile
        }


      # send form data to sales_db     

      db.collection(u'sales_db').document(authe.current_user['email']).collection('sales_info').add(dataFromForm)

      # update inventory_db //updating the item quantity after sale -->
      
      products_data=getInStock()
      l=len(products_data)
      print("**************************************",products_data,l)

      for i in range(length):

        doc = db.collection('inventory_db').document(authe.current_user['email']).collection('products').document(item_name[i]).get()
        product=doc.to_dict()
        print(product)

        old_quantity=product.get("quantity")
        new_quantity=old_quantity-int(quantity[i])
        print(new_quantity)

        db.collection(u'inventory_db').document(authe.current_user['email']).collection('products').document(item_name[i]).set({
          u'quantity': new_quantity
          }, merge=True)      


      return render(request,"payment.html",{'user':authe.current_user, 'tot':bill_total})
    else:
      data=getInStock()
      l=len(data)
      return render(request,"newBill.html",{'user':authe.current_user, 'data':data,'length':l})





def in_Stock(request):
  if authe.current_user==None:
    return render(request,"Login.html",{'user':authe.current_user})
  else:
    data=getInStock()
    l=len(data)
    return render(request,"in_stock.html",{'user':authe.current_user, 'data':data,'length':l})





# Firebase FireStore Related ----------------------------->

#To get products in-stock:
def getInStock():
  collections = db.collection('inventory_db').document(authe.current_user['email']).collection('products').stream()
  data=[]
  for doc in collections:
    d=doc.to_dict()
    if d['quantity']>0:
      data.append(dict(d))
  return(data)


#To get previous bills in sales_db:
def getBills():
  collections = db.collection('sales_db').document(authe.current_user['email']).collection('sales_info').order_by(
    u'bill_date', direction=firestore.Query.DESCENDING).stream()
  data=[]
  for doc in collections:
    d=doc.to_dict()
    data.append(dict(d))
  return(data)


# show Previous Bills ----------------------------->

def showPreviousBills(request):
  if authe.current_user==None:
    return render(request,"Login.html",{'user':authe.current_user})
  else:
    if request.method == 'POST':
      bill_index=request.POST['sno']
      bill_index=int(bill_index)

      data=getBills()
      bill_info=data[bill_index-1]
      print(bill_info)

      items=bill_info.get('items')
      brands=bill_info.get('brands')
      rates=bill_info.get('rates')
      quantities=bill_info.get('quantities')
      amounts=bill_info.get('amounts')

      dataComb=[]
      for i in range(len(items)):
        t=[]
        t.append(items[i])
        t.append(brands[i])
        t.append(rates[i])
        t.append(quantities[i])
        t.append(amounts[i])
        dataComb.append(t)

      return render(request,"bill_details.html",{'user':authe.current_user, 'bill_info':bill_info, 'dataComb':dataComb})

    else:  
      data=getBills()
      l=len(data)
      return render(request,"previousBills.html",{'user':authe.current_user, 'data':data,'length':l})


  

