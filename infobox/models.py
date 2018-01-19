# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Property(models.Model):
    identifier = models.CharField(max_length=1024)
    frecuency = models.PositiveIntegerField()

    def get_frecuency(self):
        return self.frecuency


class PageRank(models.Model):
    entity = models.CharField(max_length=1024, db_index=True)
    page_rank = models.DecimalField(max_digits=25, decimal_places=20)

    def get_page_rank(self):
        return self.page_rank
