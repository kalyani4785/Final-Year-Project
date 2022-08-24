from django.urls import path, include
from . import views
urlpatterns = [
    # Here we are assigning the path of our url
    path('', views.index),
    path('login', views.signIn, name="login"),
    path('postsignIn/', views.postsignIn),
    path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="log"),
    path('postsignUp/', views.postsignUp),
    path('reset/', views.reset),
    path('postReset/', views.postReset),
    path('about/', views.aboutUs),
    path('newBill/', views.newBill),
    path('inStock/', views.in_Stock),
    path('newBill/newBill/', views.newBill),
    path('bills/',views.showPreviousBills)
]