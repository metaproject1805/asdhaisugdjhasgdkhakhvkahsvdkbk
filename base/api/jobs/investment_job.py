import os
import django 


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metatask.settings")

django.setup()
 


from profiles.models import Profile
from base.utils.functions import create_user_notification


def accumulate_investment():
  users_with_an_active_investment = Profile.objects.filter(investment__payment_status="Active")
  for user in users_with_an_active_investment:
    if user.investment.days_remaining <= 0:
      user.balance += user.investment.price
      user_notification=create_user_notification(
        type="Success", 
        title="Package Expiration Notice", 
        message="""
        Your investment package has expired. Your capital has been added to your balance, and the investment package has been deleted.
        you can now withdraw your capital. Thank you
        """
        )
      user.notification.add(user_notification)
      user.investment.delete()
      user.investment = None
      user.save()
      
    else:
      user.investment.days_remaining -= 1
      if user.investment.level == 2:
        user.balance += 1
      else:
        daily_earning_percentage = user.investment.daily_earning / 100
        adding_up = daily_earning_percentage * user.investment.price
        user.balance += adding_up
      user.investment.save()
      user.save()
    
    
    
# accumulate_investment()