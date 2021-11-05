from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password, isStaff=False, isAdmin=False):
        if not email:
            raise ValueError("Users must have an email")

        if not password:
            raise ValueError("Users must have an password")

        userObj = self.model(email=self.normalize_email(email))

        userObj.set_password(password)
        userObj.staff = isStaff
        userObj.admin = isAdmin
        userObj.save(using=self._db)

        return userObj

    def create_staffuser(self, email, password):
        user = self.create_user(email, password, isStaff=True)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password, isStaff=True, isAdmin=True)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    avatar = models.ImageField(default="users/user.png", upload_to="users/")
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Profile of user {self.user}"
