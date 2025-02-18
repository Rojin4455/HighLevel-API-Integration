
from django.http import JsonResponse
import json
import requests
from django.shortcuts import redirect
from decouple import config

CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
REDIRECT_URI = "https://saasyway.com"
TOKEN_URL = "https://services.leadconnectorhq.com/oauth/token"
SCOPE = "contacts.readonly%20contacts.write%20locations/customFields.readonly%20locations/customFields.write"
LOCATION_ID = "T5Cfw9OugGIZURmhkFW1"



def auth_connect(request):
    auth_url = ("https://marketplace.leadconnectorhq.com/oauth/chooselocation?response_type=code&"
                f"redirect_uri={REDIRECT_URI}&"
                f"client_id={CLIENT_ID}&"
                f"scope={SCOPE}"
                )
    return redirect(auth_url)



def oauth_callback(request):
    authorization_code = request.GET.get("code")

    if not authorization_code:
        return JsonResponse({"error": "Authorization code not found"}, status=400)

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": 'http://localhost:8000/oauth/callback/',
        "code": authorization_code,
    }

    response = requests.post(TOKEN_URL, data=data)

    print("Request Sent To:", TOKEN_URL)
    print("Request Data:", data)
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Text:", response.text[:500])

    try:
        response_data = response.json()
        
        request.session['access_token'] = response_data.get('access_token')
        request.session['refresh_token'] = response_data.get('refresh_token')
        request.session['token_type'] = response_data.get('token_type')
        request.session['expires_in'] = response_data.get('expires_in')
        
        from datetime import datetime
        request.session['token_timestamp'] = datetime.now().timestamp()
        
        request.session.modified = True
        
        return JsonResponse({
            "message": "Authentication successful",
            "access_token": response_data.get('access_token'),
            "token_stored": True
        })
        
    except requests.exceptions.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON response from API",
            "status_code": response.status_code,
            "response_text": response.text[:500]
        }, status=500)





def create_contact(request):
    ACCESS_TOKEN = request.session.get('access_token')

    url = "https://services.leadconnectorhq.com/contacts/"
    print("ass", ACCESS_TOKEN)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }

    data = {
        "firstName": "justin",
        "lastName": "john",
        "email": "justin@example.com",
        "locationId": LOCATION_ID
    }

    print("Sending data:", data)
    response = requests.post(url, json=data, headers=headers)
    
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

    return JsonResponse(response.json())




    

def get_contact_by_email(request):
    ACCESS_TOKEN = request.session.get('access_token')
    email = request.GET.get('email')
    print("email: ", email)
    
    url = "https://services.leadconnectorhq.com/contacts/"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }
    
    params = {
        "query": email,
        "locationId": LOCATION_ID
    }
    
    response = requests.get(url, headers=headers, params=params)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)
    
    try:
        response_data = response.json()
        contacts = response_data.get('contacts', [])
        
        if contacts:
            contact_id = contacts[0].get('id')
            return JsonResponse({"contact_id": contact_id})
        return JsonResponse({"error": "Contact not found"}, status=404)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)









def get_contacts(request):
    ACCESS_TOKEN = request.session.get('access_token')
    

    url = "https://services.leadconnectorhq.com/contacts/"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }




    params = {
        "locationId": LOCATION_ID
    }

    response = requests.get(url, headers=headers, params=params)
    print("Response Status Code-------------:", response.status_code)
    print("Response Text-----------------:", response.text)

    return JsonResponse(response.json())




def update_custom_field(request, contact_id):
    ACCESS_TOKEN = request.session.get('access_token')


    url = f"https://services.leadconnectorhq.com/contacts/{contact_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }

    
    data = {
        "customFields": [
            {
                "id": "api_test_field",
                "name": "API Test Field",
                "value": "The Field Value Changed"
            }
        ]
    }

    response = requests.put(url, json=data, headers=headers)
    print("Update Response Status Code:--------", response.status_code)
    print("Update Response Text:", response.text)

    try:
        response_data = response.json()
        
        verification_response = requests.get(url, headers=headers)
        verification_data = verification_response.json()

        return JsonResponse({
            "message": "Custom field update attempted",
            "update_response": response_data,
            "current_contact_data": verification_data
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


def get_details_with_custom_fields(request,contact_id):
    ACCESS_TOKEN = request.session.get('access_token')

    url = f"https://services.leadconnectorhq.com/contacts/{contact_id}"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }
    
    response = requests.get(url, headers=headers)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)
    
    try:
        contact_data = response.json()
        print()
        print()
        print()
        print("contact data:      ----------------------->", contact_data)
        print()
        print()
        print()
        

        custom_fields = contact_data.get('contact', {}).get('customFields', [])



        return JsonResponse({
            "contact_id": contact_id,
            "custom_fields": custom_fields,
            "full_contact_data": contact_data
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)