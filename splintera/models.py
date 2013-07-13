from django.db import models
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger(__name__)

class GroupKey(models.Model):
    #id = models.AutoField(primary_key=True) added automatically
    key = models.CharField(max_length=32)
    group = models.OneToOneField(Group)