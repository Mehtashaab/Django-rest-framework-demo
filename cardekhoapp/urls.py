from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views




# Create an instance of the DefaultRouter class
router = DefaultRouter()

# Register a ViewSet with the router
# The first argument 'howroom' is the base name of the URL
# The second argument views.Showroom_Viewset is the ViewSet class
# The third argument 'basename' is an optional parameter to specify the base name of the URL
# In this case, we're setting the base name to 'howroom'
router.register('showroom', views.Showroom_Viewset, basename='showroom')



urlpatterns = [
    path('list',views.car_list_view,name="car_list"),
    path('<int:pk>',views.car_detail,name='car_detail'),

    path('',include(router.urls)),
    #path('showroom',views.Showroom_View.as_view(),name='Showroom_Views'),
    #path('showroom/<int:pk>',views.Showroom_details.as_view(),name='Showroom_details'),
    path('review',views.ReviewList.as_view(),name='review_list'),
    path('review/<int:pk>',views.ReviewDetails.as_view(),name='review_details'),
    
]
