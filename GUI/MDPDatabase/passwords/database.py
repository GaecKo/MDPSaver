from .models import Password
from se

def add_password(site, username, encrypted_password):
    password = Password(site=site, username=username, encrypted_password=encrypted_password)
    password.save()
