from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

import uuid

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, userid, password, **kwargs):
        user = self.model(
            login_id=userid,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid=None, password=None, **extra_fields):
        superuser = self.create_user(
            login_id=userid,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser):
    USER_GENDER_LABEL = [
        (1, "MEN"),
        (2, "WOMEN"),
    ]

    userid = models.CharField(primary_key=True, max_length=30, verbose_name='userid')
    password = models.CharField(max_length=100, verbose_name='password')
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=80)
    gender = models.IntegerField(choices=USER_GENDER_LABEL)
    phone = models.CharField(max_length=13)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'userid'
    password = 'pw'
    
    REQUIRED_FIELDS = ['name', 'gender', 'phone']

    objects = UserManager

    class Meta:
        managed = False
        db_table = 'user'


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey('User', models.DO_NOTHING)
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    secret_key = models.CharField(max_length=40)
    enabled = models.IntegerField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'service'


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
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'logging_list'


class Recomand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    target = models.CharField(max_length=20)
    recomand_type = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'recomand'