# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Positions(models.Model):
    shortcd = models.CharField(max_length=12, unique=True, primary_key=True)
    qty = models.IntegerField(default=0)
    mark = models.FloatField(default=0.0)
    tradeprice = models.FloatField(default=0.0)
    pnl_open = models.FloatField(default=0.0)

    def __str__(self):
        return self.shortcd

