import re
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_user_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    
    if UserModel.objects.filter(email=email).exists():
        raise ValidationError({"message":'Email chosen! Choose another email'})
    
    if UserModel.objects.filter(username=username).exists():
        raise ValidationError({"message":'Username chosen! Choose another username'})
    ##
    if not password or len(password) < 8:
        raise ValidationError({"message":'choose another password, min 8 characters'})
    
    if not password or len(password) > 30:
        raise ValidationError({"message":'choose another password, max 30 characters'})
    ##
    if not email:
        raise ValidationError({"message":'email is required'})
    
    if not username:
        raise ValidationError({"message":'username is required'})
    
    return data

def custom_ref_code_validation(ref_code: str):
  
    #if len(ref_code) != 12:
        #raise ValidationError({"message":'invalid referrer code'})
      
    
    if not re.match(r'^[a-zA-Z0-9_]*$', ref_code):
        raise ValidationError({"message":'invalid referrer code'})

    return ref_code

def custom_conf_pass_validation(password: str, confirm_password:str):
  
    if password != confirm_password:
        raise ValidationError({"message":"Password do not match."})

    return confirm_password
