from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('success/', views.LeadSuccessView.as_view(), name='success'),
]