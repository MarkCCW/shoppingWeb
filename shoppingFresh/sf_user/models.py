from django.db import models

class UserInfo(models.Model):
    username = models.CharField(max_length=20)
    userpwd = models.CharField(max_length=40)
    useremail = models.CharField(max_length=30)
    userreceiver = models.CharField(max_length=20, default='')
    useraddress = models.CharField(max_length=100, default='')
    userpostalcode = models.CharField(max_length=5, default='')
    userphone = models.CharField(max_length=10, default='')