from django.urls import path
from .views import ProjectList,ApplicationDetails

urlpatterns = [
    path('proj/', ProjectList.as_view(), name='Project-list'),
    path('apps/<str:projid>/',ApplicationDetails.as_view(),name='Apps-list')
]
