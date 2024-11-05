import uuid
import random
import os
from profiles.models import UserNotification
from decimal import Decimal


def create_user_notification(title, message, type="Success",):
    notification = UserNotification.objects.create(type=type, title=title, message=message)
    return notification



def generate_ref_code():
    code = str(uuid.uuid4()).replace("_", "")[:12]
    return code


def load_words_from_file(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

def generate_phase_code():
    words = load_words_from_file("phases.txt")
    return random.choice(words)





# def remove_five_percent(amount):
#     deduction = amount * 0.05
#     updated_amount = amount - deduction
#     return updated_amount


def remove_five_percent(amount, percentage = 5): # Ensure the amount is a Decimal
    percentage = Decimal((percentage / 100)) * Decimal(amount)
    return round(percentage, 2)