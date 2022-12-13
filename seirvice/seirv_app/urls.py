from django.urls import path 
from .import views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import MyPasswordResetForm

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('signup/', views.signup, name='signup'),
        path('logout/', views.signout, name="logout"),
    path('login/', views.signin, name='login'),
    path('forgotpassword/', PasswordResetView.as_view(
        template_name = 'passchange.html',
		form_class = MyPasswordResetForm
	), name = 'reset_password'),
    
    path('forgotpassword_sent/', PasswordResetView.as_view(
        template_name = 'forgotsent.html'), name = 'password_reset_done'),
    
    path('forgotpassword/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name = 'passconfirm.html'), name = 'password_reset_confirm'),
    path('forgotpassword_complete/', PasswordResetCompleteView.as_view(
        template_name = 'forgotdone.html'), name = 'password_reset_complete'),
    path('infectious/', views.infectiousDisease, name='infectious'),
    path('infectious/<pk>', views.infectiousDisease, name='infectious-history'),
    path('dengue/', views.dengueDisease, name='dengue'),
    path('dengue/<pk>', views.dengueDisease, name='dengue-history'),
    path('download/<disease>/<pk>', views.download_pdf, name='download_pdf')
    ]