from django.urls import path
from App import views,incoming_data

urlpatterns = [
    path('destination_account',views.AccountDestinationAPI.as_view()),
    path('account',views.AccountAPI.as_view()),
    path('destination', views.DestinationAPI.as_view()),
    path('server/incoming_data', incoming_data.data_handler),
]