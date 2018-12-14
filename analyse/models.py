# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	phone = models.BigIntegerField()
	name = models.CharField(max_length=200)
	first_message = models.CharField(max_length=3000)
	pos_message = models.CharField(max_length=3000)
	neg_message = models.CharField(max_length=3000)