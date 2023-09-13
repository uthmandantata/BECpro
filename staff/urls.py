from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    
    path('', views.home, name='home'),
    path('costumUser/', views.costumUser, name='costumUser'),
    path('updateCostumUser/<int:pk>/', views.updateCostumUser, name='updateCostumUser'),

    # ---------------  Members  -----------------------------
    path('staff_members/', views.staff_members, name='staff_members'),
    path('updateMembers/<int:pk>', views.updateMembers, name='updateMembers'),
    path('addMembers', views.addMembers, name='addMembers'),
    path('suspendMembers/<int:pk>', views.suspendMembers, name='suspendMembers'),
    path('resumeMembers/<int:pk>', views.resumeMembers, name='resumeMembers'),
    # -------------  End of Members--------------------------

    
    
    # ---------------  Horses  -----------------------------
    path('horses/', views.horses, name='horses'),
    path('addHorses/', views.addHorses, name='addHorses'),
    path('updateHorses/<int:pk>/', views.updateHorses, name='updateHorses'),
    path('removeHorses/<str:pk>/', views.removeHorses, name="removeHorses"),
    # -------------  End of Horses--------------------------

    # ---------------  Services  -----------------------------
    path('services/', views.services, name='services'),
    path('addServices/', views.addServices, name='addServices'),
    path('updateServices/<int:pk>/', views.updateServices, name='updateServices'),
    path('removeServices/<str:pk>/', views.removeServices, name="removeServices"),
    # -------------  End of Services--------------------------

    # ---------------  Tickets  -----------------------------
    path('tickets/', views.tickets, name='tickets'),
    path('printTickets/<int:pk>/', views.printTickets, name='printTickets'),
     path('printed/<int:pk>/', views.printed.as_view(), name='printed'),
    
    path('addTickets/', views.addTickets, name='addTickets'),
    path('members_history/', views.members_history, name='members_history'),
    # -------------  End of Tickets--------------------------

    # ---------------  Equipment  -----------------------------
    path('equipment/', views.equipment, name='equipment'),
    path('addEquipment/', views.addEquipment, name='addEquipment'),
    path('updateEquipment/<int:pk>/', views.updateEquipment, name='updateEquipment'),
    path('removeEquipment/<str:pk>/', views.removeEquipment, name="removeEquipment"),
    # -------------  End of Equipment--------------------------
    

    path('staff_notification/', views.staff_notification, name='staff_notification'),
    path('add_notifications/', views.add_notifications, name='add_notifications'),
    path('update_notifications/<str:pk>/', views.update_notifications, name='update_notifications'),
    path('remove_notifications/<str:pk>/', views.remove_notifications, name='remove_notifications'),


    path('polo_schedule/', views.polo_schedule, name='polo_schedule'),

    
    

    
]   