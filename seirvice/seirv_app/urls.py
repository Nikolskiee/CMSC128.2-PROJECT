from django.urls import path 
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('infectious/', views.infectiousDisease, name='infectious'),
    path('infectious/<pk>', views.infectiousDisease, name='infectious-history'),
    path('dengue/', views.dengueDisease, name='dengue'),
    path('dengue/<pk>', views.dengueDisease, name='dengue-history'),
    path('history-try/', views.history, name='history-try'),
    ]