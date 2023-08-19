from django.urls import path
from . import views


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.decorators.csrf import csrf_exempt




urlpatterns = [

    path('renew_subscription', views.renew_subscription, name='renew_subscription'),
    path('billing_history', views.billing_history, name='billing_history'),
    path('subscription_guide', views.subscription_guide, name='subscription_guide'),
    path('support_ticket', views.support_ticket, name='support_ticket'),
    path('members-details', views.members_details, name='members-details'),
    



    
    path('', views.member_dashboard, name='member_dashboard'),
    path('<int:pk>', views.updateMembersDetails, name='updateMembersDetails'),
    path('members_details', views.members_details, name='members_details'),

    
    path('paymentHistory/', views.paymentHistory, name='paymentHistory'),
    path('complaints', views.complaints, name='complaints'),
    path('notifications', views.notifications, name='notifications'),
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







