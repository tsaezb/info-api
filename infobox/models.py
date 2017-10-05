# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Property(models.Model):
    identifier = models.CharField(max_length=50)
    frecuency = models.PositiveIntegerField()

    def get_frecuency(self):
        return self.frecuency
