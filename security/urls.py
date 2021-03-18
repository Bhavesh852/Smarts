from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings

urlpatterns = [
   
    path('', views.index, name='securitydashboard'),
    path('login/', views.securityLogin, name='securityLogin'),
   	path("logout/", views.handlelogout, name="securitylogout"),
   	path('home/', views.home, name='securityhome'),
   	
   	path('complain/', views.complain, name='securitycomplain'),
   	path('view/<int:myid>', views.view, name='complain_view'),
    path("reply/<int:comid>", views.reply, name="reply_complaint"),
   	path('delete/<int:myid>', views.delete, name='complain_delete'),
   	
   	path('voting/', views.voting, name='securityvoting'),
   	path('group/', views.group_add, name='vote_group'),
   	path('listgroup/', views.listgroup, name='listgroup'),
   	path('groupview/<myid>', views.groupview, name='groupview'),
    path('delete_group/<int:myid>', views.delete_group, name='delete_group'),
    path('makevote/', views.makevote, name='makevote'),
    path('startingvote/', views.startingvote, name='startingvote'),
    path('endvoting/<msg>', views.endvoting, name='endvoting'),

    path('votecount/<voter>', views.votecount, name='votecount'),
    path('v_result/', views.v_result, name='vote_result'),
    path('erase/<msg>', views.erase, name='erase_votes'),

    path('main/', views.main, name='maintenance'),
    path('billgenerat/', views.billgenerat, name='billgenerat'),
    path('billform/<flat>', views.billform, name='billform'),
    path('bilgen/', views.bilgenrated, name='bilgenrated'),
    path('billview/', views.billview, name='bilview'),
    path('bill/<int:mt_id>', views.bill, name='bill'),
    path('bilupdate/<int:main_id>', views.bilupdate, name='billupdate'),
    path('recents/', views.recent, name='recent'),
    path('recentview/', views.recentview, name='recentview'),
    path('recentbilview/<int:rmt_id>', views.recentbilview, name='recentbilview'),

    path('visit/', views.visit, name='visitors_info')
    # path("handlerequest/", views.handlerequest, name="HandleRequest")

]
