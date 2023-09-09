# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class LoggingList(models.Model):
    service = models.OneToOneField('Service', models.DO_NOTHING, primary_key=True)
    click = models.IntegerField()
    scroll = models.IntegerField()
    stay_time = models.IntegerField()
    payment = models.IntegerField()
    gender = models.IntegerField()
    search_world = models.IntegerField()
    platform = models.IntegerField()
    inflow = models.IntegerField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'logging_list'


class Recomand(models.Model):
    service = models.OneToOneField('Service', models.DO_NOTHING, primary_key=True)
    target = models.CharField(max_length=20)
    recomand_type = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'recomand'


class Service(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    owner = models.ForeignKey('User', models.DO_NOTHING)
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    secret_key = models.CharField(max_length=40)
    enabled = models.IntegerField()
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'service'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    pw = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=80)
    gender = models.IntegerField()
    phone = models.CharField(max_length=13)
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'
