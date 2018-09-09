from django.db import models
from main.models import User
from .choices import *
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


class Bowlers(models.Model):
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    wkts = models.FloatField(db_column='Wkts', blank=True, null=True)  # Field name made lowercase.
    ave = models.FloatField(db_column='Ave', blank=True, null=True)  # Field name made lowercase.
    econ = models.FloatField(db_column='Econ', blank=True, null=True)  # Field name made lowercase.
    sr = models.FloatField(db_column='SR', blank=True, null=True)  # Field name made lowercase.
    wickettaker = models.FloatField(db_column='WicketTaker', blank=True, null=True)  # Field name made lowercase.
    totalovers = models.FloatField(blank=True, null=True)
    matches = models.FloatField(db_column='Matches', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    role = models.TextField(blank=True, null=True, verbose_name='Playing Role', choices=ROLE_CHOICES)
    bat = models.TextField(blank=True, null=True)
    bowl = models.TextField(blank=True, null=True)
    pca = models.FloatField(db_column='PCA', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True, verbose_name='PCA Rank')  # Field name made lowercase.
    ahprank = models.FloatField(db_column='Ahprank', blank=True, null=True, verbose_name='AHP Rank')  # Field name made lowercase.
    ahpclosenessrank = models.FloatField(db_column='Ahpclosenessrank', blank=True, null=True)  # Field name made lowercase.
    users = models.ManyToManyField(User, through='main.UserSelect')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'bowler'

    def get_absolute_url(self):
        return reverse('bowler-detail', args=[str(self.id)])


class Batsmen(models.Model):
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    inningsplayed = models.FloatField(db_column='InningsPlayed', blank=True, null=True)  # Field name made lowercase.
    runs = models.FloatField(db_column='Runs', blank=True, null=True)  # Field name made lowercase.
    ave = models.FloatField(db_column='Ave', blank=True, null=True)  # Field name made lowercase.
    sr = models.FloatField(db_column='SR', blank=True, null=True)  # Field name made lowercase.
    dotball = models.FloatField(blank=True, null=True)
    hardhitter = models.FloatField(db_column='HardHitter', blank=True, null=True)  # Field name made lowercase.
    finisher = models.FloatField(db_column='Finisher', blank=True, null=True)  # Field name made lowercase.
    hf = models.FloatField(db_column='HF', blank=True, null=True)  # Field name made lowercase.
    fifty = models.FloatField(db_column='Fifty', blank=True, null=True)  # Field name made lowercase.
    zeros = models.FloatField(db_column='Zeros', blank=True, null=True)  # Field name made lowercase.
    centuries = models.FloatField(db_column='Centuries', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    role = models.TextField(blank=True, null=True, verbose_name='Playing Role', choices=ROLE_CHOICES)
    bat = models.TextField(blank=True, null=True)
    bowl = models.TextField(blank=True, null=True)
    pca = models.FloatField(db_column='PCA', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True, verbose_name='PCA Rank')  # Field name made lowercase.
    ahprank = models.FloatField(db_column='Ahprank', blank=True, null=True, verbose_name='AHP Rank')  # Field name made lowercase.
    ahpclosenessrank = models.FloatField(db_column='Ahpclosenessrank', blank=True, null=True)  # Field name made lowercase.
    users = models.ManyToManyField(User, through='main.UserSelect')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'batsmen'

    def get_absolute_url(self):
        return reverse('batsman-detail', args=[str(self.id)])
