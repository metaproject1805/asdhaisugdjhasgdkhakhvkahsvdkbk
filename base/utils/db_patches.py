from django.db.backends.mysql.base import DatabaseWrapper

# Patch the display_name method to accept 0 positional arguments.
def display_name_patched(self):
    return "MySQL"

DatabaseWrapper.display_name = display_name_patched