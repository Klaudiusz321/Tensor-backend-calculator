from django.urls import path
from . import views

urlpatterns = [
    path('calculate', views.calculate_view, name='calculate'),
    # Tymczasowo wyłączamy endpoint visualize
    # path('visualize', views.visualize_view, name='visualize'),
]
