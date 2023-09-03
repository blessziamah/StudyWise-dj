from django.urls import path
from . import views
from django.urls import re_path as url
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.home, name='home'),
	path('accounts/login/', views.login_user, name='login'),
	path('accounts/signup/', views.register_user, name='signup'),
	path("logout/", views.logout_user, name='logout'),
	path('account-info/', views.account_page, name='account-info'),
	path('upload_audio/', views.process_audio, name='upload_audio'),
    path('process_audio/', views.process_audio, name='process_audio'),


	url(r'^login/accounts/password_reset/$',
		auth_views.PasswordResetView.as_view(template_name='soundwise/password/password_reset_form.html'),
		name='password_reset'),
	url(r'^accounts/password_reset_done/$',
		auth_views.PasswordResetDoneView.as_view(template_name='soundwise/password/password_reset_done.html'),
		name='password_reset_done'),
	url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
		auth_views.PasswordResetConfirmView.as_view(template_name='soundwise/password/password_reset_confirm.html'),
		name='password_reset_confirm'),
	url(r'^accounts/reset/done/$',
		auth_views.PasswordResetCompleteView.as_view(template_name='soundwise/password/password_reset_complete.html'),
		name='password_reset_complete'),

	path("account/password_change/", views.changePassword, name='changePassword'),

]
