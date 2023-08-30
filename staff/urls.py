from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
<<<<<<< HEAD
    path('', views.landing, name='landing'),
    path('', views.home, name='home'),
    path('login', views.loginUser, name='login'),
    path('register', views.registerUser, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('paymentHistory/', views.paymentHistory, name='paymentHistory'),
    path('complaints', views.complaints, name='complaints'),
    path('notifications', views.notifications, name='notifications'),
    
    






    path('subscription', views.subscription, name='subscription'),
    
    path('payment/', views.call_back_url, name='payment'),
    path('subscribe', views.subscribe, name='subscribe'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    
    path('costumUser/', views.costumUser, name='costumUser'),
    path('updateCostumUser/<int:pk>/', views.updateCostumUser, name='updateCostumUser'),

    # ------------------------------------------------------------------------------
    path('member_dashboard', views.member_dashboard, name='member_dashboard'),
    path('<int:pk>', views.updateMembersDetails, name='updateMembersDetails'),
    path('members_details', views.members_details, name='members_details'),
    # ------------------------------------------------------------------------------



    # ------------------------------------------------------------------------------
    path('password_reset_request', views.password_reset_request, name='password_reset_request'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
    # ------------------------------------------------------------------------------


    # ---------------  Members  -----------------------------
    path('members', views.members, name='members'),
=======
    
    path('', views.home, name='home'),
    path('costumUser/', views.costumUser, name='costumUser'),
    path('updateCostumUser/<int:pk>/', views.updateCostumUser, name='updateCostumUser'),

    # ---------------  Members  -----------------------------
    path('staff_members/', views.staff_members, name='staff_members'),
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
    path('updateMembers/<int:pk>', views.updateMembers, name='updateMembers'),
    path('addMembers', views.addMembers, name='addMembers'),
    path('suspendMembers/<int:pk>', views.suspendMembers, name='suspendMembers'),
    path('resumeMembers/<int:pk>', views.resumeMembers, name='resumeMembers'),
    # -------------  End of Members--------------------------

    # ---------------  Slots  -----------------------------
    path('slots/', views.slots, name='slots'),
    path('addSlots/', views.addSlots, name='addSlots'),
    path('updateSlots/<int:pk>/', views.updateSlots, name='updateSlots'),
    path('removeSlots/<str:pk>/', views.removeSlots, name="removeSlots"),
    # -------------  End of Slots--------------------------
    
<<<<<<< HEAD

=======
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
    # ---------------  Horses  -----------------------------
    path('horses/', views.horses, name='horses'),
    path('addHorses/', views.addHorses, name='addHorses'),
    path('updateHorses/<int:pk>/', views.updateHorses, name='updateHorses'),
    path('removeHorses/<str:pk>/', views.removeHorses, name="removeHorses"),
    # -------------  End of Horses--------------------------

<<<<<<< HEAD

     # ---------------  Services  -----------------------------
=======
    # ---------------  Services  -----------------------------
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
    path('services/', views.services, name='services'),
    path('addServices/', views.addServices, name='addServices'),
    path('updateServices/<int:pk>/', views.updateServices, name='updateServices'),
    path('removeServices/<str:pk>/', views.removeServices, name="removeServices"),
    # -------------  End of Services--------------------------

    # ---------------  Tickets  -----------------------------
    path('tickets/', views.tickets, name='tickets'),
<<<<<<< HEAD
    path('addTickets/', views.addTickets, name='addTickets'),
    path('updateTickets/<int:pk>/', views.updateTickets, name='updateTickets'),
    path('removeTickets/<str:pk>/', views.removeTickets, name="removeTickets"),
=======
    path('printTickets/<int:pk>/', views.printTickets, name='printTickets'),
     path('printed/<int:pk>/', views.printed.as_view(), name='printed'),
    
    path('addTickets/', views.addTickets, name='addTickets'),
    path('members_history/', views.members_history, name='members_history'),
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
    # -------------  End of Tickets--------------------------

    # ---------------  Equipment  -----------------------------
    path('equipment/', views.equipment, name='equipment'),
    path('addEquipment/', views.addEquipment, name='addEquipment'),
<<<<<<< HEAD
    path('updateEquipment/<int:pk>', views.updateEquipment, name='updateEquipment'),
    path('removeEquipment/<str:pk>', views.removeEquipment, name="removeEquipment"),
    # -------------  End of Equipment--------------------------

    path('staff/', views.staff, name='staff'),
    

    path('test', views.test, name='test'),


    path('profile', views.profile, name='profile'),
    path('updateProfile', views.updateProfile, name='updateProfile'),



    
=======
    path('updateEquipment/<int:pk>/', views.updateEquipment, name='updateEquipment'),
    path('removeEquipment/<str:pk>/', views.removeEquipment, name="removeEquipment"),
    # -------------  End of Equipment--------------------------
    

    path('staff_notification/', views.staff_notification, name='staff_notification'),
    path('add_notifications/', views.add_notifications, name='add_notifications'),
    path('update_notifications/<str:pk>/', views.update_notifications, name='update_notifications'),
    path('remove_notifications/<str:pk>/', views.remove_notifications, name='remove_notifications'),


    path('polo_schedule/', views.polo_schedule, name='polo_schedule'),

    
    
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2

    
]   