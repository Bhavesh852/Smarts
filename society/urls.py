from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    path('', views.index , name = "societyhome"),
    path("contact/", views.contact, name="societycontact"),
    path("about/", views.about, name="societycontact"),
    path("signup/", views.handlesignup, name="societysignup"),
    path("login/", views.handlelogin, name="societylogin"),
    path("logout/", views.handlelogout, name="societylogout"),
    path("home/", views.home, name="societyhome"),
    path("complaint/", views.complaint, name="societycomplaint"),
    path("makevote/", views.makevote, name='societymakevote'),
    path("maintenance/", views.maintenance, name='so_maintenance'),
    path("paybill/<mynum>", views.paybill, name='so_paybill'),
    path("recentbil/<myflat>", views.recentbil, name='so_recentbil'),
    path("rbilview/<int:rmt_id>", views.rbilview, name='bilview'),
    path("visitor/", views.visitor, name='visitor')
   

]
