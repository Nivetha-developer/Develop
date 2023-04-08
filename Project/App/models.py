from django.db import models
import uuid

# Create your models here.

class AccountMaster(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True)
    app_secret_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    website = models.URLField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.account_name

class Destination(models.Model):
    account = models.ForeignKey(AccountMaster, on_delete=models.CASCADE)
    url = models.URLField(null=False)
    http_method = models.CharField(max_length=10,null=False)
    # http_method = models.CharField(choices=(('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')), max_length=10)
    headers = models.JSONField(null=False)

    def __str__(self):
        return self.url
