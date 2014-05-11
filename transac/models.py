from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    name = models.CharField(max_length=20)
    pdfdoc = models.FileField(upload_to='user_transactions/')
    uploader = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class TransactionView(models.Model):
    trans = models.ForeignKey(Transaction)
    viewer = models.ForeignKey(User)
    shared_by = models.IntegerField(default=0)
    def __str__(self):
        return self.trans.name
