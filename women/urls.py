from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (AddPage, LoginUser, RegisterUser, WomenCategory,
                    WomenDetail, WomenHome, about, contact, contact_success,
                    logout_user)

urlpatterns = [
    path('', cache_page(30)(WomenHome.as_view()), name='home'),
    path('post/<slug:post_slug>/', WomenDetail.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('about/', about, name='about'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('succes_contact', contact_success, name='contact_success'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout_user'),
]
