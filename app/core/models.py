"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Here we define the UserManager based on the BaseUserManager class provided \
# by Django
class UserManager(BaseUserManager):
    """Manager for users"""
    # Here we define a method to create a user
    # We provide the minimum things require to make a user: an email and \
    # a password
    # We set password to None so that is can be provided optionally
    # Password is usually provided, but can be excluded to make an unusable \
    # user (wouldn't be able to log in)
    # Our **extra_fields parameter is used to provide keyword arguments
    # Allows you to attribute new fields to the model without changing \
    # the method
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        # Here we use self.model to make a user bc our Manager class makes \
        # it so that it calls the User class since that's what it's assigned
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # This method sets password for our user that encrypts through a \
        # hashing mechanism
        user.set_password(password)
        # Method saves our user using self._db just in case you use \
        # multiple db
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

# We start our custom user model by making a class User that takes in \
# AbstractBaseUser contains the functionality for the authorization system
# PermissionsMixin contains the functionality for the permissions & fields
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    # Here we use the django EmailField to validate emails
    email= models.EmailField(max_length=255, unique=True)
    # This is a simple CharField that allows us to input any character
    name= models.CharField(max_length=255)
    # This is a simple function to register user as active by default
    is_active = models.BooleanField(default=True)
    # This is a function to determine if someone can log into Django admin
    is_staff = models.BooleanField(default=True)

    # This line is how youu assign a User manager in django
    objects = UserManager()

    USERNAME_FIELD = 'email'
