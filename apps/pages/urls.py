from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about-us/', views.AboutView.as_view(), name='about'),
    path('legal/<slug:slug>/', views.LegalDetailView.as_view(), name='legal'),
    path('terms/', views.LegalDetailView.as_view(), {'slug': 'terms'}, name='terms'),
    path('privacy/', views.LegalDetailView.as_view(), {'slug': 'privacy'}, name='privacy'),
]