# from django.db import models
# from django.core.validators import RegexValidator
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models

# class MyUserManager(BaseUserManager):

#     def create_user(self, username, email,first_name,last_name, password, **kwags):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not username:
#             raise ValueError('Users must have a username')
#         if not first_name:
#             raise ValueError('Users must have a firstname')
#         if not last_name:
#             raise ValueError('Users must have a lastname')

#         user = self.model(
#             username=username,
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#         )

#         user.is_active  = True
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email,first_name,last_name, password):
#         user = self.create_user(username=username,email=email, password=password,first_name=first_name,last_name=last_name)

#         user.is_staff = True
#         user.is_superuser = True
#         user.set_password(password)
#         user.save()
#         return user 

# class User(AbstractBaseUser, PermissionsMixin):

#     alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')
#     username    = models.CharField(unique=True, max_length=20, validators=[alphanumeric])
#     email       = models.EmailField(verbose_name='email address', unique=True, max_length=244)
#     first_name  = models.CharField(max_length=30, null=True, blank=True)
#     last_name   = models.CharField(max_length=50, null=True, blank=True)
#     is_active   = models.BooleanField(default=True, null=False)
#     is_staff    = models.BooleanField(default=False, null=False)


#     objects = MyUserManager()

#     USERNAME_FIELD  = 'email'
#     REQUIRED_FIELDS = ['username','last_name','first_name']

#     def get_full_name(self):
#         fullname = self.first_name+" "+self.last_name
#         return self.fullname

#     def get_short_name(self):
#         return self.username

#     def str(self):
#         return self.email

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

class MyUserManager(BaseUserManager):
    def create_user(self, nom, prenom, numero_de_telephone, password, **kwargs):

        if not nom:
            raise ValueError('Users must have a last name')
        if not prenom:
            raise ValueError('Users must have a first name')
        if not numero_de_telephone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            nom=nom,
            prenom=prenom,
            numero_de_telephone=numero_de_telephone,
            **kwargs
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, numero_de_telephone, password):
        user = self.create_user(
            nom=nom,
            prenom=prenom,
            numero_de_telephone=numero_de_telephone,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 

class User(AbstractBaseUser, PermissionsMixin):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')
    
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    matricule_de_voiture = models.CharField(max_length=20, null=True, blank=True)
    numero_de_telephone = models.CharField(max_length=15, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'numero_de_telephone'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def get_short_name(self):
        return self.prenom


