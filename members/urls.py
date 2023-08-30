from django.urls import path
from . import views


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.decorators.csrf import csrf_exempt




urlpatterns = [
    

    path('change_subscription', views.change_subscription, name='change_subscription'),
    path('billing_history', views.billing_history, name='billing_history'),
    path('subscription_guide', views.subscription_guide, name='subscription_guide'),
   
    path('members-details', views.members_details, name='members-details'),
    path('update-members', views.updateMembersDetails, name='updateMembersDetails'),
    path('error-page', views.errors, name='error-page'),
   
    



    
    path('', views.member_dashboard, name='member_dashboard'),
    path('<int:pk>', views.updateMembersDetails, name='updateMembersDetails'),
    

    
    
    path('complaints', views.complaints, name='complaints'),
    path('notifications', views.notifications, name='notifications'),
    path('view_notifications/<str:pk>/', views.viewNotifications, name='view_notifications'),
    path('subscription', views.subscription, name='subscription'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('payment/', views.call_back_url, name='payment'),

  
    
    # ------------------------------------------------------------------------------
    path('password_reset_request', views.password_reset_request, name='password_reset_request'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
    # ------------------------------------------------------------------------------
    
    
]   







