from django.urls import path
from .views import *

urlpatterns = [
    path("auth/connect/", auth_connect, name="oauth_connect"),
    path("oauth/callback/", oauth_callback, name="oauth_callback"),
    path('create-contact/', create_contact, name="create_contact"),
    path('get-contact-details/<str:contact_id>/', get_details_with_custom_fields, name="get_contact_details"),

    path('get-contact-id/' , get_contact_by_email, name='get-contact-id'),
    path('contacts/<str:contact_id>/update/', update_custom_field, name='update_custom_field'),
    
    path('get-contacts/', get_contacts, name="get_contacts"),


]