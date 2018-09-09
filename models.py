# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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
    id = models.IntegerField()
    role = models.TextField(blank=True, null=True)
    bat = models.TextField(blank=True, null=True)
    bowl = models.TextField(blank=True, null=True)
    pca = models.FloatField(db_column='PCA', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    ahprank = models.FloatField(db_column='Ahprank', blank=True, null=True)  # Field name made lowercase.
    ahpclosenessrank = models.FloatField(db_column='Ahpclosenessrank', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'batsmen'


class Bowler(models.Model):
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    wkts = models.FloatField(db_column='Wkts', blank=True, null=True)  # Field name made lowercase.
    ave = models.FloatField(db_column='Ave', blank=True, null=True)  # Field name made lowercase.
    econ = models.FloatField(db_column='Econ', blank=True, null=True)  # Field name made lowercase.
    sr = models.FloatField(db_column='SR', blank=True, null=True)  # Field name made lowercase.
    wickettaker = models.FloatField(db_column='WicketTaker', blank=True, null=True)  # Field name made lowercase.
    totalovers = models.FloatField(blank=True, null=True)
    matches = models.FloatField(db_column='Matches', blank=True, null=True)  # Field name made lowercase.
    role = models.TextField(blank=True, null=True)
    bat = models.TextField(blank=True, null=True)
    bowl = models.TextField(blank=True, null=True)
    pca = models.FloatField(db_column='PCA', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    ahprank = models.FloatField(db_column='Ahprank', blank=True, null=True)  # Field name made lowercase.
    ahpclosenessrank = models.FloatField(db_column='Ahpclosenessrank', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'bowler'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MainTeam(models.Model):
    counter = models.IntegerField()
    total = models.IntegerField()
    arr = models.TextField()  # This field type is a guess.
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'main_team'


class MainUserselect(models.Model):
    team = models.CharField(max_length=1)
    batsman_id = models.IntegerField(blank=True, null=True)
    bowler = models.ForeignKey(Bowler, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'main_userselect'
