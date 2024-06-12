from django.urls import path
from . import views

urlpatterns = [
    path('list',views.car_list_view,name="car_list"),
    path('<int:pk>',views.car_detail,name='car_detail'),
    path('showroom',views.Showroom_View.as_view(),name='Showroom_Views'),
    path('showroom/<int:pk>',views.Showroom_details.as_view(),name='Showroom_details')
]
