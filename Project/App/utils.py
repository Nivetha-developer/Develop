from App.models import *

def get_account_from_app_secret_token(app_secret_token):
    try:
        account = AccountMaster.objects.get(app_secret_token=app_secret_token)
        return account
    except AccountMaster.DoesNotExist:
        return None