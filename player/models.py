from django.db import models
from .choices import *
from main.models import User
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns



class Bowlers(models.Model):
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    wkts = models.FloatField(db_column='Wkts', blank=True, null=True)  # Field name made lowercase.
    ave = models.FloatField(db_column='Ave', blank=True, null=True)  # Field name made lowercase.
    econ = models.FloatField(db_column='Econ', blank=True, null=True)  # Field name made lowercase.
    sr = models.FloatField(db_column='SR', blank=True, null=True)  # Field name made lowercase.
    totalovers = models.FloatField(blank=True, null=True)
    matches = models.FloatField(db_column='Matches', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(unique=True, null=False, primary_key=True)
    Playing_Role = models.TextField(choices=ROLE_CHOICES, default='Select from')
    bat = models.TextField(blank=True, null=True)
    #bat = models.TextField(choices=ROLE_CHOICES, default='RED')
    bowl = models.TextField(blank=True, null=True)
    ahp_closeness_ratio = models.FloatField(db_column='ahp_closeness_ratio', blank=True, null=True)
    ahprank = models.FloatField(db_column='ahprank', blank=True, null=True, verbose_name='AHP Rank')
    pcarank = models.FloatField(db_column='pcarank', blank=True, null=True, verbose_name='PCA Rank')
    users = models.ManyToManyField(User, through='main.UserSelect')
    # this is to show names of fields instead of objects

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bowlers'

    def get_absolute_url(self):
        return reverse('bowler-detail', args=[str(self.id)])
