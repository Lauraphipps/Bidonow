from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('test/secure/', views.secure_page)
]
