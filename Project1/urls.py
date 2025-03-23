from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('food/', include('FoodApp.urls')),
    path('register/', user_views.register, name='register'),
    path('login/',auth_view.LoginView.as_view(template_name ="users/login.html") ,name='login'),
    # By default the login will redirect to "accounts/filter" after completion of seuccessfull login to override it we have to make changes in the settings.py.
    path('logout/', auth_view.LogoutView.as_view(template_name ="users/logout.html"), name='logout')
]
