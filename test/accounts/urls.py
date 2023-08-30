from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    
    path('', views.home, name='home'),
    
    
    




    
    
    path('costumUser/', views.costumUser, name='costumUser'),
    path('updateCostumUser/<int:pk>/', views.updateCostumUser, name='updateCostumUser'),


    # ---------------  Members  -----------------------------
    path('members', views.members, name='members'),
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
    path('addTickets/', views.addTickets, name='addTickets'),
    path('updateTickets/<int:pk>/', views.updateTickets, name='updateTickets'),
    path('removeTickets/<str:pk>/', views.removeTickets, name="removeTickets"),
    # -------------  End of Tickets--------------------------

    # ---------------  Equipment  -----------------------------
    path('equipment/', views.equipment, name='equipment'),
    path('addEquipment/', views.addEquipment, name='addEquipment'),
    path('updateEquipment/<int:pk>', views.updateEquipment, name='updateEquipment'),
    path('removeEquipment/<str:pk>', views.removeEquipment, name="removeEquipment"),
    # -------------  End of Equipment--------------------------

    path('staff/', views.staff, name='staff'),
    



    

    
]   