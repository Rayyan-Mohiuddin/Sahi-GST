from django.contrib import admin
from django.urls import path, include, re_path
from invoices import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/session/', views.session), path('api/health/', views.health),
    path('api/reviews/', views.reviews), path('api/reviews/<uuid:ident>/', views.detail),
    path('api/reviews/report/', views.all_reports),
    path('api/reviews/<uuid:ident>/image/', views.review_image),
    path('api/reviews/<uuid:ident>/report/', views.review_report),
    path('api/parse/', views.parse), path('api/extract/', views.extract),
    re_path(r'^(?P<path>.*)$', views.frontend),
]
