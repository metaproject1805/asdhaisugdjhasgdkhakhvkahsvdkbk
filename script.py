import os
import django 


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metatask.settings")

django.setup()


from profiles.models import Profile

print("i am now working")