from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<contacted>/thanks/i-will-get-back-to-you-shortly/', views.index, name='index-contacted'),
    path('submit-review/', views.submit_review, name='submit-review'),
    path('contact-me/', views.contact_me, name='contact-me'),
    path('thank-you/really-it-means-a-lot/i-owe-you-a-coffee/let-me-know-when-you-are-free/', views.index, name='thank-you'),
    path('projects/', views.projects, name='projects'),
]