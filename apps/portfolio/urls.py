from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.PortfolioListView.as_view(), name='list'),
    path('category/<slug:slug>/', views.PortfolioCategoryView.as_view(), name='category'),
    path('<slug:slug>/', views.PortfolioDetailView.as_view(), name='detail'),
]