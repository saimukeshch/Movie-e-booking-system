from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('login/', views.login_view, name='login_view'),
    path('registration_success', views.registration_success, name="registration_success"),
    path('resetpassword_email', views.resetpassword_email, name="resetpassword_email"),
    path('resetpassword_success',views.resetpassword_success, name = "resetpassword_success"),
    path('user-profile', views.user_profile, name="user-profile"),
    path('editprofile', views.editprofile, name="editprofile"),
    path('schedule_movie', views.schedule_movie, name="schedule_movie"),
    path('admin-send-promo', views.send_promo, name="send_promo"),
    path('logoutpage', views.logoutpage, name="logoutpage"),
    path('registration', views.registration, name="registration"),
    path('addmovie',views.addmovie,name = 'addmovie' ),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('activation_success', views.activation_success, name="activation_success"),
    path('forgotpassword/<username>/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword', views.resetpassword, name='resetpassword'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('search', views.search, name='search'),
    path('admin-promo', views.adminPromo, name='admin-promo'),
    path('booking', views.booking, name='booking'),
    path('seatselect', views.seatselect, name='seatselect'),
    path('add-card', views.addCard, name='add-card'),
    path('orderedit', views.orderedit, name='orderedit'),
    path('checkout', views.checkout, name='checkout'),
    path('orderconfirm', views.orderconfirm, name='orderconfirm')

]
