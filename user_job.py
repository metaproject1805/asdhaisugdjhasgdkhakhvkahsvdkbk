import os
import django 


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metatask.settings")

django.setup()


from profiles.models import Profile
from base.utils.functions import create_user_notification

def daily_profile_update():
  users_with_an_active_package = Profile.objects.filter(active_package__payment_status="Active")
  for user in users_with_an_active_package:
    if user.active_package.days_remaining <= 0:
      user.balance += user.active_package.price
      user_notification=create_user_notification(
        type="Success", 
        title="Package Expiration Notice", 
        message="""
        Your investment package has expired. Your capital has been added to your balance, and the investment package has been deleted.
        you can now withdraw your capital. Thank you
        """
        )
      user.notification.add(user_notification)
      user.active_package.delete()
      user.investment = None
      user.save()
      
    else:
      user.active_package.days_remaining -= 1
      user.video_watched_count = 0
      user.video_watched.clear()
      user.active_package.save()
      user.save()
    
# schedule.every(10).seconds.do(daily_profile_update)    
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
    
# daily_profile_update()


# while True:
#     schedule.run_pending()


daily_profile_update()