from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('import/', views.import_transactions, name='import'),
    path('clear-transactions/', views.clear_transactions, name='clear_transactions'),
]
