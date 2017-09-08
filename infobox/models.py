# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Property(models.Model):
  label = models.CharField(max_length=50)
  identifier = models.CharField(max_length=50)
  frecuency = models.PositiveIntegerField()
