from django.urls import path 
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('infectious/', views.infectiousDisease, name='infectious'),
    path('dengue/', views.dengueDisease, name='dengue'),
    path('history-try/', views.history, name='history-try')
    ]