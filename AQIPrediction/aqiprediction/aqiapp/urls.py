from django.urls import path
from . import views

app_name = "aqiapp"

urlpatterns = [

    path('', views.predict, name='prediction_page'),
    path('aqiapp/', views.predict_chances, name='submit_prediction'),
    path('aqiapp/', views.view_results, name='results'),
]
