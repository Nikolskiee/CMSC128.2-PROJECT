from django.urls import path 
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('demo/', views.demo_plot_view, name='plotly-demo'),
    path('dengue-plot/', views.plot_dengue, name='plot-dengue'),
    path('seirv-seir-plot/', views.plot_seirv_seir, name='plot-seirv-seir')
]