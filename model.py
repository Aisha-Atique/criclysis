# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Bowler(models.Model):
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    wkts = models.FloatField(db_column='Wkts', blank=True, null=True)  # Field name made lowercase.
    ave = models.FloatField(db_column='Ave', blank=True, null=True)  # Field name made lowercase.
    econ = models.FloatField(db_column='Econ', blank=True, null=True)  # Field name made lowercase.
    sr = models.FloatField(db_column='SR', blank=True, null=True)  # Field name made lowercase.
    wickettaker = models.FloatField(db_column='WicketTaker', blank=True, null=True)  # Field name made lowercase.
    totalovers = models.FloatField(blank=True, null=True)
    matches = models.FloatField(db_column='Matches', blank=True, null=True)  # Field name made lowercase.
    id = models.FloatField(primary_key=True)
    role = models.TextField(blank=True, null=True)
    bat = models.TextField(blank=True, null=True)
    bowl = models.TextField(blank=True, null=True)
    pca = models.FloatField(db_column='PCA', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    ahprank = models.FloatField(db_column='Ahprank', blank=True, null=True)  # Field name made lowercase.
    ahpclosenessrank = models.FloatField(db_column='Ahpclosenessrank', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bowler'
