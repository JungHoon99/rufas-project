from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Permission

import uuid

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, phone, gender, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            username=username,
            phone=phone,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USER_GENDER_LABEL = [
        (1, "MEN"),
        (2, "WOMEN"),
    ]

    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=13, null=False)
    date_of_birth = models.DateField()
    gender = models.IntegerField(choices=USER_GENDER_LABEL, default=1)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class main_service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    secret_key = models.CharField(max_length=40)
    enabled = models.IntegerField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class loggingList(models.Model):
    service = models.OneToOneField(main_service, models.DO_NOTHING, primary_key=True)
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
        managed = True


class Recomand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    service = models.ForeignKey(main_service, on_delete=models.CASCADE)
    target = models.CharField(max_length=20)
    recomand_type = models.CharField(max_length=30)

    class Meta:
        managed = True
