from django.urls import path
from .views import oauth_callback, auth_connect, create_contact, get_contacts, get_contact_by_email, get_contact_details_with_fields

urlpatterns = [
    path("auth/connect/", auth_connect, name="oauth_connect"),
    path("oauth/callback/", oauth_callback, name="oauth_callback"),
    path('create-contact/', create_contact, name="create_contact"),
    path('get-contact-details/<str:contact_id>/', get_contact_details_with_fields, name="get_contact_details"),
    path('get-contact-id/' , get_contact_by_email, name='get-contact-id'),

    
    #additional
    path('get-contacts/', get_contacts, name="get_contacts"),


]