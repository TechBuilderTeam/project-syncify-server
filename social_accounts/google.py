from google.auth.transport import requests
from google.oauth2 import id_token
from accounts.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class Google():
    @staticmethod
    def validate(access_token):
        try:
            idinfo = id_token.verify_oauth2_token(access_token, requests.Request(), settings.GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            return idinfo['sub']
        except ValueError:
            raise AuthenticationFailed('Invalid token.')
        
def login_social_user(email,password):
    user=authenticate(email=email,password=password)
    token=user.tokens()  
    return {
        'email':user.email,
        'full_name':user.get_full_name,
        'access_token':str(token.get('access_token')),
        'refresh_token':str(token.get('refresh_token')),
    }
        
def register_social_user(provider,email,first_name,last_name):
    user=User.objects.filter(email=email)
    if user.exists():
        if provider==user[0].auth_provider:
            result=login_social_user(email,settings.SOCIAL_AUTH_PASSWORD)
            return result
        else:
            raise AuthenticationFailed(
                detail=f'Please contineu login with {user[0].auth_provider}'
            )
    else:
        new_user={
            'email':email,
            'first_name':first_name,
            'last_name':last_name,
            'password':settings.SOCIAL_AUTH_PASSWORD,
            'auth_provider':provider,
        }
        register_user=User.objects.create_user(**new_user)
        register_user.is_verified=True
        register_user.save()
        result=login_social_user(register_user.email,settings.SOCIAL_AUTH_PASSWORD)
        return result