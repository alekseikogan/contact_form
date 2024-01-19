from django.urls import path

from .views import (
    about, AddPage, WomenCategory, contact, WomenHome,
    LoginUser, WomenDetail, RegisterUser, logout_user,
    contact_success)

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('about/', about, name='about'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('post/<slug:post_slug>/', WomenDetail.as_view(), name='post'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout_user'),
    path('succes_contact', contact_success, name='contact_success'),
]
